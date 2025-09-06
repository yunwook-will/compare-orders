#!/usr/bin/env python3
"""
Excel Compare Tool - 원클릭 실행기
"""
import subprocess
import os
import sys
import time
import webbrowser
from pathlib import Path

def print_banner():
    print("=" * 50)
    print("📊 Excel Compare Tool")
    print("=" * 50)

def check_requirements():
    """필수 프로그램 확인"""
    print("✅ 필수 프로그램 확인중...")
    
    # Python 확인
    try:
        subprocess.run(["python3", "--version"], capture_output=True, check=True)
        print("  ✓ Python3 설치됨")
    except:
        print("  ✗ Python3가 필요합니다")
        return False
    
    # Node 확인
    try:
        subprocess.run(["node", "--version"], capture_output=True, check=True)
        print("  ✓ Node.js 설치됨")
    except:
        print("  ✗ Node.js가 필요합니다")
        return False
    
    return True

def setup_backend():
    """Backend 설정 및 실행"""
    print("\n📦 Backend 준비중...")
    backend_path = Path(__file__).parent / "backend"
    os.chdir(backend_path)
    
    # 가상환경 생성
    venv_path = backend_path / "venv"
    if not venv_path.exists():
        print("  Python 가상환경 생성중...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
    
    # pip 설치
    pip_cmd = str(venv_path / "bin" / "pip") if os.name != 'nt' else str(venv_path / "Scripts" / "pip")
    print("  패키지 설치중...")
    subprocess.run([pip_cmd, "install", "-q", "-r", "requirements.txt"])
    
    # uvicorn 실행
    python_cmd = str(venv_path / "bin" / "python") if os.name != 'nt' else str(venv_path / "Scripts" / "python")
    print("  Backend 서버 시작...")
    backend_process = subprocess.Popen([python_cmd, "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"])
    
    return backend_process

def setup_frontend():
    """Frontend 설정 및 실행"""
    print("\n🎨 Frontend 준비중...")
    frontend_path = Path(__file__).parent / "frontend"
    os.chdir(frontend_path)
    
    # npm install
    if not (frontend_path / "node_modules").exists():
        print("  Node modules 설치중 (처음 실행시 시간이 걸립니다)...")
        subprocess.run(["npm", "install"])
    
    # npm start
    print("  Frontend 서버 시작...")
    frontend_process = subprocess.Popen(["npm", "start"])
    
    return frontend_process

def main():
    print_banner()
    
    # 필수 프로그램 확인
    if not check_requirements():
        print("\n❌ 필수 프로그램을 먼저 설치해주세요")
        sys.exit(1)
    
    backend_process = None
    frontend_process = None
    
    try:
        # Backend 실행
        backend_process = setup_backend()
        time.sleep(3)  # Backend 시작 대기
        
        # Frontend 실행
        frontend_process = setup_frontend()
        
        print("\n" + "=" * 50)
        print("✅ Excel Compare Tool 실행 완료!")
        print("=" * 50)
        print("\n📌 브라우저에서 자동으로 열립니다...")
        print("📌 주소: http://localhost:3000")
        print("\n🔴 종료 방법:")
        print("   1. 이 터미널에서 Ctrl+C 누르기")
        print("   2. 또는 이 터미널 창을 닫기")
        print("=" * 50)
        
        # 브라우저 자동 열기
        time.sleep(5)
        webbrowser.open("http://localhost:3000")
        
        # 프로세스 대기
        backend_process.wait()
        frontend_process.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 종료 신호 받음...")
        print("서버를 종료하는 중입니다...")
        
        if backend_process:
            backend_process.terminate()
            backend_process.wait(timeout=5)
            print("  ✓ Backend 서버 종료됨")
            
        if frontend_process:
            frontend_process.terminate()
            frontend_process.wait(timeout=5)
            print("  ✓ Frontend 서버 종료됨")
            
        print("\n✅ 정상적으로 종료되었습니다!")
        print("다시 실행하려면: python3 run.py")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        sys.exit(1)

if __name__ == "__main__":
    main()