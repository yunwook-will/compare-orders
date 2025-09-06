# Excel Compare Tool

주문 내역 엑셀 파일을 비교하고 분석하는 웹 애플리케이션

## 기능

- 두 엑셀 파일 업로드 및 비교
- 차이점 시각화 (차트, 테이블)
- 주문별, 상품별, 금액별 분석
- 결과 다운로드 (CSV, Excel)

## 프로젝트 구조

```
excel-compare-app/
├── frontend/                # React 프론트엔드
│   ├── src/
│   │   ├── components/     # UI 컴포넌트
│   │   ├── pages/         # 페이지 컴포넌트
│   │   ├── services/      # API 통신
│   │   └── utils/         # 유틸리티 함수
│   └── package.json
├── backend/                # FastAPI 백엔드
│   ├── app/
│   │   ├── api/          # API 엔드포인트
│   │   ├── core/         # 비교 로직
│   │   └── models/       # 데이터 모델
│   └── requirements.txt
└── docker-compose.yml     # Docker 설정 (선택사항)
```

## 기술 스택

- **Frontend**: React, TypeScript, Ant Design, Recharts
- **Backend**: FastAPI, Python, Pandas, OpenPyXL
- **Database**: SQLite (선택사항, 히스토리 저장용)

## 설치 및 실행

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## 주요 기능 상세

1. **파일 업로드**: Drag & Drop 지원
2. **비교 분석**: 
   - 전체 요약 통계
   - 열 비교
   - 행별 상세 비교
   - 금액 차이 분석
3. **시각화**:
   - 차이점 하이라이트
   - 통계 차트
   - 필터링 및 정렬
4. **내보내기**: CSV, Excel 형식 지원