#!/bin/bash

# Excel Compare Tool 시작 스크립트

echo "🚀 Excel Compare Tool 시작중..."

# Backend 시작
echo "📦 Backend 서버 시작..."
cd backend
if [ ! -d "venv" ]; then
    echo "Python 가상환경 생성중..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# Frontend 시작
echo "🎨 Frontend 서버 시작..."
cd ../frontend
if [ ! -d "node_modules" ]; then
    echo "Node modules 설치중..."
    npm install
fi

npm start &
FRONTEND_PID=$!

echo "✅ 시작 완료!"
echo ""
echo "📌 접속 주소: http://localhost:3000"
echo "📌 종료하려면 Ctrl+C를 누르세요"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"

# Ctrl+C 처리
trap "echo '종료중...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

# 프로세스 대기
wait