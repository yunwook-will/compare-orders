# Excel Compare Tool

주문 내역 엑셀 파일을 비교하고 분석하는 웹 애플리케이션

## 🚀 빠른 시작

```bash
python3 run.py              # 원클릭 실행 (백엔드 + 프론트엔드 자동 시작)
```

브라우저에서 http://localhost:3000 에 자동으로 접속됩니다.

## ✅ 현재 구현된 기능

- **파일 업로드**: 두 엑셀 파일 Drag & Drop 업로드
- **배송비 차이 분석**: 주문번호별 배송비 합계 비교 및 차이점 표시
- **금액 합계 비교**: 판매액, 배송비, 공급단가, 공급가액 필드별 합계 비교
- **고유 주문번호 탭**: 각 파일에만 있는 고유 주문 목록 표시 (상품수, 총액, 상품코드 포함)
- **열 구조 비교**: 공통 열과 각 파일 고유 열 분석
- **요약 통계**: 전체 행수, 주문수, 공통/차이 주문 개수

## 📁 프로젝트 구조

```
excel-compare-app/
├── frontend/                # React 프론트엔드
│   ├── src/
│   │   ├── App.tsx         # 메인 애플리케이션 컴포넌트
│   │   ├── App.css         # 스타일시트
│   │   └── index.tsx       # React 진입점
│   ├── public/             # 정적 파일
│   └── package.json
├── backend/                # FastAPI 백엔드
│   ├── app/
│   │   └── main.py        # API 엔드포인트 + Excel 비교 로직
│   └── requirements.txt
├── run.py                  # 원클릭 실행 스크립트
├── manager.py              # 대화형 관리 도구
└── 배포 스크립트들/         # 다양한 패키징 옵션
```

## 🛠 기술 스택

- **Frontend**: React, TypeScript, Ant Design
- **Backend**: FastAPI, Python, Pandas, OpenPyXL
- **배포**: Docker, PyInstaller, Electron 옵션 제공

## 💻 설치 및 실행 옵션

### 방법 1: 원클릭 실행 (추천)
```bash
python3 run.py              # 모든 설정 자동화
python3 manager.py          # 대화형 관리 (시작/중지/상태확인)
```

### 방법 2: 개별 실행
```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (새 터미널)
cd frontend
npm install
npm start
```

### 방법 3: Docker
```bash
docker-compose up --build
```

## 📊 사용 방법

1. **파일 업로드**: 두 엑셀 파일을 드래그 앤 드롭으로 업로드
2. **비교 시작**: "비교 분석 시작" 버튼 클릭
3. **결과 확인**: 4개 탭에서 상세 분석 결과 확인
   - **배송비 차이**: 주문별 배송비 차이점과 수취인 정보
   - **금액 합계 비교**: 판매액, 배송비 등 필드별 총 합계 비교
   - **고유 주문번호**: 각 파일에만 있는 고유 주문 목록
   - **열 비교**: 공통 열과 각 파일 고유 열 분석

## 📋 지원하는 엑셀 형식

Excel 파일은 다음 열을 포함해야 합니다:
- `주문번호` (필수): 비교의 기준점
- `배송비`: 배송비 차이 분석용
- `판매액`, `공급단가`, `공급가액`: 금액 비교용
- `수취인명`, `상품코드`: 상세 정보 표시용

## 🔮 향후 계획 및 할일

### 차트 및 시각화
- [ ] Recharts를 활용한 차이점 시각화 차트
- [ ] 금액 차이 히트맵 표시
- [ ] 트렌드 분석 그래프

### 데이터 처리 개선
- [ ] 필터링 및 정렬 기능 추가
- [ ] 행별 상세 비교 기능 (현재는 주문별만)
- [ ] 대용량 파일 처리 최적화

### 내보내기 기능
- [ ] CSV 다운로드 실제 구현 (현재 placeholder)
- [ ] Excel 형식 내보내기
- [ ] PDF 보고서 생성

### 데이터 저장
- [ ] SQLite 데이터베이스 연동
- [ ] 비교 히스토리 저장 및 조회
- [ ] 즐겨찾기 및 북마크 기능

### 사용성 개선
- [ ] 다국어 지원 (현재 한국어만)
- [ ] 테마 설정 (다크 모드)
- [ ] 사용자 설정 저장

### 배포 및 운영
- [ ] 웹 호스팅 버전
- [ ] 데스크톱 앱 완성 (Electron)
- [ ] 모바일 반응형 UI