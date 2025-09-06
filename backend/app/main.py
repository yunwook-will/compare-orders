from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import io
import tempfile
import os

app = FastAPI(title="Excel Compare API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 개발 서버
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExcelComparator:
    def __init__(self, file1_path: str, file2_path: str):
        self.df1 = pd.read_excel(file1_path, sheet_name=0)
        self.df2 = pd.read_excel(file2_path, sheet_name=0)
    
    def get_summary(self) -> Dict[str, int]:
        """파일 요약 정보"""
        orders1 = set(self.df1['주문번호'].astype(str).unique())
        orders2 = set(self.df2['주문번호'].astype(str).unique())
        common_orders = orders1 & orders2
        
        return {
            'totalRows1': len(self.df1),
            'totalRows2': len(self.df2),
            'totalOrders1': len(orders1),
            'totalOrders2': len(orders2),
            'commonOrders': len(common_orders),
            'differentOrders': len(orders1 ^ orders2)
        }
    
    def get_column_comparison(self) -> Dict[str, List[str]]:
        """열 비교"""
        cols1 = set(self.df1.columns)
        cols2 = set(self.df2.columns)
        
        return {
            'common': sorted(list(cols1 & cols2)),
            'onlyInFile1': sorted(list(cols1 - cols2)),
            'onlyInFile2': sorted(list(cols2 - cols1))
        }
    
    def get_exclusive_orders(self) -> Dict[str, List[Dict[str, Any]]]:
        """각 파일에만 있는 고유 주문번호 찾기"""
        orders1 = set(self.df1['주문번호'].astype(str).unique())
        orders2 = set(self.df2['주문번호'].astype(str).unique())
        
        only_in_file1 = orders1 - orders2
        only_in_file2 = orders2 - orders1
        
        result = {
            'onlyInFile1': [],
            'onlyInFile2': []
        }
        
        # 파일1에만 있는 주문
        for order_no in only_in_file1:
            df_order = self.df1[self.df1['주문번호'].astype(str) == order_no]
            if not df_order.empty:
                first_row = df_order.iloc[0]
                result['onlyInFile1'].append({
                    'orderNo': order_no,
                    'customerName': first_row.get('수취인명', ''),
                    'productCount': len(df_order),
                    'totalAmount': float(df_order['판매액'].sum()) if '판매액' in df_order.columns else 0,
                    'products': ', '.join(df_order['상품코드'].tolist()) if '상품코드' in df_order.columns else ''
                })
        
        # 파일2에만 있는 주문
        for order_no in only_in_file2:
            df_order = self.df2[self.df2['주문번호'].astype(str) == order_no]
            if not df_order.empty:
                first_row = df_order.iloc[0]
                result['onlyInFile2'].append({
                    'orderNo': order_no,
                    'customerName': first_row.get('수취인명', ''),
                    'productCount': len(df_order),
                    'totalAmount': float(df_order['판매액'].sum()) if '판매액' in df_order.columns else 0,
                    'products': ', '.join(df_order['상품코드'].tolist()) if '상품코드' in df_order.columns else ''
                })
        
        return result
    
    def get_shipping_differences(self) -> List[Dict[str, Any]]:
        """배송비 차이 분석"""
        # 주문번호별 배송비 합계
        shipping1 = self.df1.groupby('주문번호')['배송비'].sum().reset_index()
        shipping1.columns = ['orderNo', 'shippingFee1']
        
        shipping2 = self.df2.groupby('주문번호')['배송비'].sum().reset_index()
        shipping2.columns = ['orderNo', 'shippingFee2']
        
        # 병합
        merged = pd.merge(shipping1, shipping2, on='orderNo', how='outer')
        merged['shippingFee1'] = merged['shippingFee1'].fillna(0)
        merged['shippingFee2'] = merged['shippingFee2'].fillna(0)
        merged['difference'] = merged['shippingFee1'] - merged['shippingFee2']
        
        # 차이가 있는 주문만
        diff_orders = merged[merged['difference'] != 0].copy()
        
        # 고객명 추가
        result = []
        for _, row in diff_orders.iterrows():
            order_no = row['orderNo']
            
            # 고객명과 상품 수 가져오기
            customer_name = ""
            product_count1 = 0
            product_count2 = 0
            
            df1_order = self.df1[self.df1['주문번호'] == order_no]
            if not df1_order.empty:
                customer_name = df1_order.iloc[0]['수취인명']
                product_count1 = len(df1_order)
            
            df2_order = self.df2[self.df2['주문번호'] == order_no]
            if not df2_order.empty:
                if not customer_name:
                    customer_name = df2_order.iloc[0]['수취인명']
                product_count2 = len(df2_order)
            
            result.append({
                'orderNo': str(order_no),
                'customerName': customer_name,
                'shippingFee1': float(row['shippingFee1']),
                'shippingFee2': float(row['shippingFee2']),
                'difference': float(row['difference']),
                'productCount1': product_count1,
                'productCount2': product_count2
            })
        
        return sorted(result, key=lambda x: abs(x['difference']), reverse=True)
    
    def get_amount_differences(self) -> List[Dict[str, Any]]:
        """금액 필드 차이 분석"""
        amount_fields = ['판매액', '배송비', '공급단가', '공급가액']
        result = []
        
        for field in amount_fields:
            if field in self.df1.columns and field in self.df2.columns:
                sum1 = self.df1[field].sum()
                sum2 = self.df2[field].sum()
                
                result.append({
                    'field': field,
                    'sum1': float(sum1),
                    'sum2': float(sum2),
                    'difference': float(sum1 - sum2)
                })
        
        return result
    
    def export_differences_to_csv(self) -> bytes:
        """차이점을 CSV로 내보내기"""
        shipping_diff = self.get_shipping_differences()
        df = pd.DataFrame(shipping_diff)
        
        output = io.StringIO()
        df.to_csv(output, index=False, encoding='utf-8-sig')
        return output.getvalue().encode('utf-8-sig')

@app.get("/")
def read_root():
    return {"message": "Excel Compare API", "version": "1.0.0"}

@app.post("/api/compare")
async def compare_excel_files(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    """두 엑셀 파일을 비교"""
    
    # 파일 확장자 검증
    for file in [file1, file2]:
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail=f"엑셀 파일만 지원됩니다: {file.filename}")
    
    # 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp1:
        content1 = await file1.read()
        tmp1.write(content1)
        tmp1_path = tmp1.name
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp2:
        content2 = await file2.read()
        tmp2.write(content2)
        tmp2_path = tmp2.name
    
    try:
        # 비교 실행
        comparator = ExcelComparator(tmp1_path, tmp2_path)
        
        result = {
            'summary': comparator.get_summary(),
            'columnComparison': comparator.get_column_comparison(),
            'differences': {
                'shippingFee': comparator.get_shipping_differences(),
                'amounts': comparator.get_amount_differences()
            },
            'exclusiveOrders': comparator.get_exclusive_orders()
        }
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # 임시 파일 삭제
        os.unlink(tmp1_path)
        os.unlink(tmp2_path)

@app.post("/api/export-csv")
async def export_differences_csv(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    """비교 결과를 CSV로 다운로드"""
    
    # 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp1:
        content1 = await file1.read()
        tmp1.write(content1)
        tmp1_path = tmp1.name
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp2:
        content2 = await file2.read()
        tmp2.write(content2)
        tmp2_path = tmp2.name
    
    try:
        comparator = ExcelComparator(tmp1_path, tmp2_path)
        csv_content = comparator.export_differences_to_csv()
        
        return StreamingResponse(
            io.BytesIO(csv_content),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=comparison_result.csv"}
        )
    
    finally:
        os.unlink(tmp1_path)
        os.unlink(tmp2_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)