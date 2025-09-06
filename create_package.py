#!/usr/bin/env python3
"""
Excel Compare Tool 패키지 생성기
ZIP 패키지 + 자동 설치 스크립트 생성
"""
import zipfile
import os
from pathlib import Path
import shutil

def create_package():
    print("📦 Excel Compare Tool 패키지 생성중...")
    
    # 패키지에 포함할 파일들
    files_to_include = {
        # Backend 파일들
        "backend/app/main.py": "backend/app/main.py",
        "backend/requirements.txt": "backend/requirements.txt",
        
        # Frontend 파일들  
        "frontend/package.json": "frontend/package.json",
        "frontend/tsconfig.json": "frontend/tsconfig.json",
        "frontend/public/index.html": "frontend/public/index.html",
        "frontend/public/manifest.json": "frontend/public/manifest.json",
        "frontend/public/robots.txt": "frontend/public/robots.txt",
        "frontend/src/App.tsx": "frontend/src/App.tsx",
        "frontend/src/App.css": "frontend/src/App.css",
        "frontend/src/index.tsx": "frontend/src/index.tsx",
        "frontend/src/index.css": "frontend/src/index.css",
        "frontend/.gitignore": "frontend/.gitignore",
        
        # 실행 스크립트들
        "run.py": "run.py",
        "manager.py": "manager.py",
        "start.sh": "start.sh",
        "stop.sh": "stop.sh",
        "README.md": "README.md",
    }
    
    # ZIP 파일 생성
    with zipfile.ZipFile("ExcelCompare_Package.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for src_file, dest_file in files_to_include.items():
            if Path(src_file).exists():
                zipf.write(src_file, dest_file)
                print(f"  ✓ {src_file}")
        
        # 설치 스크립트 추가
        installer_script = '''#!/usr/bin/env python3
"""
Excel Compare Tool 자동 설치 및 실행
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🚀 Excel Compare Tool 자동 설치")
    print("=" * 40)
    
    # 현재 디렉토리에 압축 해제되어 있다고 가정
    if not Path("run.py").exists():
        print("❌ 파일이 올바르게 압축 해제되지 않았습니다.")
        return
    
    # 실행
    subprocess.run([sys.executable, "run.py"])

if __name__ == "__main__":
    main()
'''
        zipf.writestr("install_and_run.py", installer_script)
        
        # 사용 설명서
        readme_content = '''# Excel Compare Tool

## 🚀 빠른 시작

1. 이 ZIP 파일을 압축 해제
2. 터미널에서 다음 명령어 실행:

```bash
python3 install_and_run.py
```

또는

```bash  
python3 run.py
```

## 📋 필수 요구사항

- Python 3.8+
- Node.js 16+
- npm

## 🔗 주소

- 웹 인터페이스: http://localhost:3000
- API 문서: http://localhost:8000/docs

## 🛑 종료

- Ctrl+C 또는 터미널 창 닫기
'''
        zipf.writestr("INSTALL.md", readme_content)
    
    print(f"\n✅ 패키지 생성 완료: ExcelCompare_Package.zip")
    print(f"📁 크기: {os.path.getsize('ExcelCompare_Package.zip') / 1024:.1f}KB")

if __name__ == "__main__":
    create_package()