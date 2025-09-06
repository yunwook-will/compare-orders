#!/usr/bin/env python3
"""
Excel Compare Tool Manager - 시작/종료 관리
"""
import subprocess
import sys
import os
import signal
from pathlib import Path

def show_menu():
    print("\n" + "=" * 50)
    print("📊 Excel Compare Tool Manager")
    print("=" * 50)
    print("1. 시작 (Start)")
    print("2. 종료 (Stop)")
    print("3. 상태 확인 (Status)")
    print("4. 나가기 (Exit)")
    print("=" * 50)

def start_app():
    """애플리케이션 시작"""
    print("\n🚀 애플리케이션을 시작합니다...")
    script_path = Path(__file__).parent / "run.py"
    subprocess.run([sys.executable, str(script_path)])

def stop_app():
    """애플리케이션 종료"""
    print("\n🛑 애플리케이션을 종료합니다...")
    
    # Backend 종료
    try:
        subprocess.run(["pkill", "-f", "uvicorn app.main:app"], capture_output=True)
        print("  ✓ Backend 서버 종료")
    except:
        pass
    
    # Frontend 종료
    try:
        subprocess.run(["pkill", "-f", "react-scripts start"], capture_output=True)
        print("  ✓ Frontend 서버 종료")
    except:
        pass
    
    print("✅ 모든 서비스가 종료되었습니다.")

def check_status():
    """서비스 상태 확인"""
    print("\n📊 서비스 상태 확인중...")
    
    # Backend 상태
    backend_check = subprocess.run(["pgrep", "-f", "uvicorn app.main:app"], 
                                  capture_output=True, text=True)
    if backend_check.stdout:
        print("  ✅ Backend: 실행중 (PID: {})".format(backend_check.stdout.strip()))
    else:
        print("  ❌ Backend: 중지됨")
    
    # Frontend 상태
    frontend_check = subprocess.run(["pgrep", "-f", "react-scripts start"], 
                                   capture_output=True, text=True)
    if frontend_check.stdout:
        print("  ✅ Frontend: 실행중 (PID: {})".format(frontend_check.stdout.strip()))
    else:
        print("  ❌ Frontend: 중지됨")
    
    if backend_check.stdout and frontend_check.stdout:
        print("\n📌 서비스 주소: http://localhost:3000")

def main():
    while True:
        show_menu()
        choice = input("\n선택하세요 (1-4): ")
        
        if choice == "1":
            start_app()
        elif choice == "2":
            stop_app()
        elif choice == "3":
            check_status()
        elif choice == "4":
            print("\n👋 종료합니다.")
            break
        else:
            print("\n⚠️ 잘못된 선택입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 종료합니다.")
        sys.exit(0)