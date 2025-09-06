#!/bin/bash

echo "🛑 Excel Compare Tool 종료중..."

# Backend 프로세스 종료 (uvicorn)
echo "Backend 서버 종료..."
pkill -f "uvicorn app.main:app"

# Frontend 프로세스 종료 (React)
echo "Frontend 서버 종료..."
pkill -f "react-scripts start"

# Node 프로세스 정리
pkill -f "node.*react"

echo "✅ 모든 서버가 종료되었습니다."