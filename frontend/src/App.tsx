import React, { useState } from 'react';
import { Upload, Button, Card, Table, Tabs, Alert, Spin, Row, Col, Statistic } from 'antd';
import { UploadOutlined, FileSearchOutlined, DownloadOutlined } from '@ant-design/icons';
import type { UploadFile } from 'antd/es/upload/interface';
import './App.css';

interface ComparisonResult {
  summary: {
    totalRows1: number;
    totalRows2: number;
    totalOrders1: number;
    totalOrders2: number;
    commonOrders: number;
    differentOrders: number;
  };
  differences: {
    shippingFee: ShippingDifference[];
    amounts: AmountDifference[];
  };
  columnComparison: {
    common: string[];
    onlyInFile1: string[];
    onlyInFile2: string[];
  };
  exclusiveOrders: {
    onlyInFile1: ExclusiveOrder[];
    onlyInFile2: ExclusiveOrder[];
  };
}

interface ExclusiveOrder {
  orderNo: string;
  customerName: string;
  productCount: number;
  totalAmount: number;
  products: string;
}

interface ShippingDifference {
  orderNo: string;
  customerName: string;
  shippingFee1: number;
  shippingFee2: number;
  difference: number;
  productCount1: number;
  productCount2: number;
}

interface AmountDifference {
  field: string;
  sum1: number;
  sum2: number;
  difference: number;
}

const App: React.FC = () => {
  const [file1, setFile1] = useState<UploadFile | null>(null);
  const [file2, setFile2] = useState<UploadFile | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ComparisonResult | null>(null);

  const handleCompare = async () => {
    if (!file1 || !file2) {
      alert('두 파일을 모두 선택해주세요.');
      return;
    }

    setLoading(true);
    
    const formData = new FormData();
    formData.append('file1', file1 as any);
    formData.append('file2', file2 as any);

    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/compare`, {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('비교 중 오류 발생:', error);
      alert('파일 비교 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const shippingColumns = [
    {
      title: '주문번호',
      dataIndex: 'orderNo',
      key: 'orderNo',
    },
    {
      title: '수취인',
      dataIndex: 'customerName',
      key: 'customerName',
    },
    {
      title: '파일1 배송비',
      dataIndex: 'shippingFee1',
      key: 'shippingFee1',
      render: (value: number) => `${value.toLocaleString()}원`,
    },
    {
      title: '파일2 배송비',
      dataIndex: 'shippingFee2',
      key: 'shippingFee2',
      render: (value: number) => `${value.toLocaleString()}원`,
    },
    {
      title: '차이',
      dataIndex: 'difference',
      key: 'difference',
      render: (value: number) => (
        <span style={{ color: value > 0 ? 'red' : value < 0 ? 'blue' : 'black' }}>
          {value > 0 ? '+' : ''}{value.toLocaleString()}원
        </span>
      ),
    },
  ];

  const amountColumns = [
    {
      title: '항목',
      dataIndex: 'field',
      key: 'field',
    },
    {
      title: '파일1 합계',
      dataIndex: 'sum1',
      key: 'sum1',
      render: (value: number) => `${value.toLocaleString()}원`,
    },
    {
      title: '파일2 합계',
      dataIndex: 'sum2',
      key: 'sum2',
      render: (value: number) => `${value.toLocaleString()}원`,
    },
    {
      title: '차이',
      dataIndex: 'difference',
      key: 'difference',
      render: (value: number) => (
        <span style={{ color: value > 0 ? 'red' : value < 0 ? 'blue' : 'black' }}>
          {value > 0 ? '+' : ''}{value.toLocaleString()}원
        </span>
      ),
    },
  ];

  const exclusiveOrderColumns = [
    {
      title: '주문번호',
      dataIndex: 'orderNo',
      key: 'orderNo',
    },
    {
      title: '수취인',
      dataIndex: 'customerName',
      key: 'customerName',
    },
    {
      title: '상품수',
      dataIndex: 'productCount',
      key: 'productCount',
    },
    {
      title: '총 판매액',
      dataIndex: 'totalAmount',
      key: 'totalAmount',
      render: (value: number) => `${value.toLocaleString()}원`,
    },
    {
      title: '상품코드',
      dataIndex: 'products',
      key: 'products',
      ellipsis: true,
    },
  ];

  return (
    <div className="App" style={{ padding: '20px' }}>
      <h1>엑셀 주문 내역 비교 도구</h1>
      
      <Row gutter={16} style={{ marginBottom: '20px' }}>
        <Col span={12}>
          <Card title="파일 1">
            <Upload
              beforeUpload={(file) => {
                setFile1(file);
                return false;
              }}
              maxCount={1}
              accept=".xlsx,.xls"
            >
              <Button icon={<UploadOutlined />}>파일 선택</Button>
            </Upload>
            {file1 && <p>{file1.name}</p>}
          </Card>
        </Col>
        <Col span={12}>
          <Card title="파일 2">
            <Upload
              beforeUpload={(file) => {
                setFile2(file);
                return false;
              }}
              maxCount={1}
              accept=".xlsx,.xls"
            >
              <Button icon={<UploadOutlined />}>파일 선택</Button>
            </Upload>
            {file2 && <p>{file2.name}</p>}
          </Card>
        </Col>
      </Row>

      <Button
        type="primary"
        size="large"
        icon={<FileSearchOutlined />}
        onClick={handleCompare}
        disabled={!file1 || !file2}
        loading={loading}
        style={{ marginBottom: '20px' }}
      >
        비교 분석 시작
      </Button>

      {loading && <Spin size="large" tip="파일을 분석하고 있습니다..." />}

      {result && (
        <>
          <Card title="비교 결과 요약" style={{ marginBottom: '20px' }}>
            <Row gutter={16}>
              <Col span={6}>
                <Statistic title="파일1 총 행수" value={result.summary.totalRows1} />
              </Col>
              <Col span={6}>
                <Statistic title="파일2 총 행수" value={result.summary.totalRows2} />
              </Col>
              <Col span={6}>
                <Statistic title="공통 주문수" value={result.summary.commonOrders} />
              </Col>
              <Col span={6}>
                <Statistic 
                  title="차이나는 주문수" 
                  value={result.summary.differentOrders}
                  valueStyle={{ color: result.summary.differentOrders > 0 ? '#cf1322' : '#3f8600' }}
                />
              </Col>
            </Row>
          </Card>

          <Tabs defaultActiveKey="1">
            <Tabs.TabPane tab="배송비 차이" key="1">
              <Table
                columns={shippingColumns}
                dataSource={result.differences.shippingFee}
                rowKey="orderNo"
                pagination={{ pageSize: 10 }}
              />
            </Tabs.TabPane>
            
            <Tabs.TabPane tab="금액 합계 비교" key="2">
              <Table
                columns={amountColumns}
                dataSource={result.differences.amounts}
                rowKey="field"
                pagination={false}
              />
            </Tabs.TabPane>
            
            <Tabs.TabPane tab="고유 주문번호" key="3">
              <Card>
                <h3>파일1에만 있는 주문 ({result.exclusiveOrders?.onlyInFile1?.length || 0}개)</h3>
                {result.exclusiveOrders?.onlyInFile1?.length > 0 ? (
                  <Table
                    columns={exclusiveOrderColumns}
                    dataSource={result.exclusiveOrders.onlyInFile1}
                    rowKey="orderNo"
                    pagination={{ pageSize: 10 }}
                    style={{ marginBottom: '30px' }}
                  />
                ) : (
                  <Alert message="파일1에만 있는 고유 주문이 없습니다." type="info" style={{ marginBottom: '30px' }} />
                )}
                
                <h3>파일2에만 있는 주문 ({result.exclusiveOrders?.onlyInFile2?.length || 0}개)</h3>
                {result.exclusiveOrders?.onlyInFile2?.length > 0 ? (
                  <Table
                    columns={exclusiveOrderColumns}
                    dataSource={result.exclusiveOrders.onlyInFile2}
                    rowKey="orderNo"
                    pagination={{ pageSize: 10 }}
                  />
                ) : (
                  <Alert message="파일2에만 있는 고유 주문이 없습니다." type="info" />
                )}
              </Card>
            </Tabs.TabPane>
            
            <Tabs.TabPane tab="열 비교" key="4">
              <Card>
                <h3>공통 열 ({result.columnComparison.common.length}개)</h3>
                <p>{result.columnComparison.common.join(', ')}</p>
                
                {result.columnComparison.onlyInFile1.length > 0 && (
                  <>
                    <h3>파일1에만 있는 열</h3>
                    <Alert
                      message={result.columnComparison.onlyInFile1.join(', ')}
                      type="warning"
                    />
                  </>
                )}
                
                {result.columnComparison.onlyInFile2.length > 0 && (
                  <>
                    <h3>파일2에만 있는 열</h3>
                    <Alert
                      message={result.columnComparison.onlyInFile2.join(', ')}
                      type="info"
                    />
                  </>
                )}
              </Card>
            </Tabs.TabPane>
          </Tabs>

          <Button
            icon={<DownloadOutlined />}
            style={{ marginTop: '20px' }}
            onClick={() => {
              // CSV 다운로드 구현
              console.log('Download CSV');
            }}
          >
            결과 다운로드 (CSV)
          </Button>
        </>
      )}
    </div>
  );
};

export default App;