#!/usr/bin/env python3
"""
Excel Compare Tool - 자동 배포 및 설치기
사용법: python3 deploy.py
"""
import os
import sys
import urllib.request
import zipfile
import tempfile
import subprocess
import json
from pathlib import Path

GITHUB_REPO = "excel-compare-tool"  # 실제 repo 이름으로 변경 필요
DOWNLOAD_URL = f"https://github.com/yourusername/{GITHUB_REPO}/archive/main.zip"

def print_banner():
    print("=" * 60)
    print("📊 Excel Compare Tool - 자동 설치기")
    print("=" * 60)

def check_requirements():
    """필수 프로그램 설치 확인 및 안내"""
    print("🔍 필수 프로그램 확인 중...")
    
    missing = []
    
    # Python 확인
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"  ✅ Python: {result.stdout.strip()}")
    except:
        missing.append("Python 3.8+")
    
    # Node.js 확인
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        print(f"  ✅ Node.js: {result.stdout.strip()}")
    except:
        missing.append("Node.js 16+")
    
    # npm 확인
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        print(f"  ✅ npm: {result.stdout.strip()}")
    except:
        missing.append("npm")
    
    if missing:
        print(f"\n❌ 다음 프로그램들을 먼저 설치해주세요:")
        for item in missing:
            print(f"   - {item}")
        print("\n설치 가이드:")
        print("  Python: https://python.org/downloads")
        print("  Node.js: https://nodejs.org/download")
        return False
    
    return True

def create_embedded_app():
    """모든 파일을 포함한 단일 Python 스크립트 생성"""
    
    # 현재 프로젝트의 모든 파일 내용을 Base64로 인코딩
    import base64
    
    embedded_data = {}
    
    # Frontend 파일들
    frontend_files = [
        "package.json",
        "tsconfig.json",
        "public/index.html",
        "public/manifest.json",
        "src/App.tsx",
        "src/App.css", 
        "src/index.tsx",
        "src/index.css"
    ]
    
    # Backend 파일들
    backend_files = [
        "requirements.txt",
        "app/main.py"
    ]
    
    print("📦 파일들을 패키징 중...")
    
    for file_path in frontend_files:
        full_path = Path("frontend") / file_path
        if full_path.exists():
            with open(full_path, 'rb') as f:
                content = f.read()
                embedded_data[f"frontend/{file_path}"] = base64.b64encode(content).decode()
    
    for file_path in backend_files:
        full_path = Path("backend") / file_path
        if full_path.exists():
            with open(full_path, 'rb') as f:
                content = f.read()
                embedded_data[f"backend/{file_path}"] = base64.b64encode(content).decode()
    
    # 단일 실행 파일 생성
    launcher_code = f'''#!/usr/bin/env python3
"""
Excel Compare Tool - 포터블 실행기
모든 파일이 포함된 단일 실행 파일입니다.
"""
import os
import sys
import base64
import tempfile
import subprocess
import webbrowser
import time
import json
from pathlib import Path

# 임베드된 데이터
EMBEDDED_DATA = {json.dumps(embedded_data, indent=2)}

def extract_files():
    """임베드된 파일들을 임시 디렉토리에 추출"""
    temp_dir = Path(tempfile.mkdtemp(prefix="excel_compare_"))
    
    print(f"📂 임시 디렉토리: {{temp_dir}}")
    
    for file_path, content_b64 in EMBEDDED_DATA.items():
        full_path = temp_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = base64.b64decode(content_b64)
        with open(full_path, 'wb') as f:
            f.write(content)
    
    return temp_dir

def run_application():
    """애플리케이션 실행"""
    print("🚀 Excel Compare Tool 시작...")
    
    # 파일 추출
    work_dir = extract_files()
    
    try:
        # Backend 설정
        backend_dir = work_dir / "backend"
        os.chdir(backend_dir)
        
        print("📦 Backend 의존성 설치...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
        
        # Backend 시작
        print("🔧 Backend 서버 시작...")
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"
        ])
        
        # Frontend 설정
        frontend_dir = work_dir / "frontend"
        os.chdir(frontend_dir)
        
        print("📦 Frontend 의존성 설치 (시간이 걸릴 수 있습니다)...")
        subprocess.run(["npm", "install"])
        
        # Frontend 시작
        print("🎨 Frontend 서버 시작...")
        frontend_process = subprocess.Popen(["npm", "start"])
        
        print("\\n" + "=" * 50)
        print("✅ Excel Compare Tool 실행 완료!")
        print("📌 브라우저: http://localhost:3000")
        print("🛑 종료: Ctrl+C")
        print("=" * 50)
        
        # 브라우저 열기
        time.sleep(8)
        webbrowser.open("http://localhost:3000")
        
        # 종료 대기
        try:
            backend_process.wait()
        except KeyboardInterrupt:
            print("\\n🛑 종료 중...")
            backend_process.terminate()
            frontend_process.terminate()
            print("✅ 종료 완료")
    
    except Exception as e:
        print(f"❌ 오류: {{e}}")
    
    finally:
        # 임시 파일 정리 (선택사항)
        import shutil
        try:
            shutil.rmtree(work_dir)
        except:
            pass

if __name__ == "__main__":
    print("=" * 50)
    print("📊 Excel Compare Tool v1.0")
    print("=" * 50)
    
    # 필수 프로그램 확인
    missing = []
    try:
        subprocess.run([sys.executable, "--version"], check=True, capture_output=True)
    except:
        missing.append("Python")
    
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
    except:
        missing.append("Node.js")
    
    if missing:
        print("❌ 다음을 먼저 설치해주세요:")
        for item in missing:
            print(f"   - {{item}}")
        sys.exit(1)
    
    run_application()
'''
    
    # 실행 파일 저장
    with open("ExcelCompare_Portable.py", "w", encoding="utf-8") as f:
        f.write(launcher_code)
    
    print("✅ 포터블 실행 파일 생성 완료: ExcelCompare_Portable.py")
    return "ExcelCompare_Portable.py"

def main():
    print_banner()
    
    if not check_requirements():
        return
    
    print("\\n📦 배포용 파일을 생성합니다...")
    
    # 포터블 앱 생성
    portable_file = create_embedded_app()
    
    print("\\n" + "=" * 60)
    print("🎉 배포 준비 완료!")
    print("=" * 60)
    print(f"📄 생성된 파일: {portable_file}")
    print("\\n📋 사용 방법:")
    print(f"1. '{portable_file}' 파일을 다른 컴퓨터로 복사")
    print(f"2. 'python3 {portable_file}' 실행")
    print("\\n✅ 단일 파일로 모든 기능이 포함되어 있습니다!")

if __name__ == "__main__":
    main()