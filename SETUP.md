# 엑셀 비교 도구 설치 및 실행 가이드

## 필요 사항
- Node.js 18+ 
- Python 3.10+
- 또는 Docker & Docker Compose

## 방법 1: 로컬 실행

### Backend 설정
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Backend가 http://localhost:8000 에서 실행됩니다.

### Frontend 설정
```bash
cd frontend
npm install
npm start
```
Frontend가 http://localhost:3000 에서 실행됩니다.

## 방법 2: Docker 실행
```bash
docker-compose up --build
```

## 사용 방법

1. 브라우저에서 http://localhost:3000 접속
2. 두 개의 엑셀 파일 업로드
3. "비교 분석 시작" 버튼 클릭
4. 결과 확인:
   - 요약 통계
   - 배송비 차이
   - 금액 합계 비교
   - 열 비교
5. CSV로 결과 다운로드

## 주요 기능

### 비교 분석
- 주문번호별 배송비 합계 비교
- 금액 필드 합계 차이 분석
- 열 구조 비교
- 차이점 하이라이트

### UI 특징
- Drag & Drop 파일 업로드
- 실시간 비교 결과 표시
- 탭 형식의 결과 보기
- 차트 시각화 (추가 가능)

## 확장 가능한 기능

1. **상세 비교 옵션**
   - 특정 열 선택 비교
   - 날짜 범위 필터
   - 상품코드별 분석

2. **시각화 개선**
   - 차트 추가 (Recharts 활용)
   - 히트맵으로 차이점 표시

3. **데이터 저장**
   - SQLite DB로 히스토리 저장
   - 비교 결과 재확인 기능

4. **성능 최적화**
   - 대용량 파일 처리
   - 백그라운드 작업 큐 (Celery)

## 문제 해결

### CORS 오류
Backend의 `main.py`에서 CORS 설정 확인:
```python
allow_origins=["http://localhost:3000"]
```

### 파일 업로드 오류
- 파일 크기 제한 확인 (기본 10MB)
- 엑셀 파일 형식 확인 (.xlsx, .xls)

### 한글 인코딩 문제
CSV 다운로드 시 `utf-8-sig` 인코딩 사용