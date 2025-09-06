#!/usr/bin/env python3
"""
Excel Compare Tool - 실행 파일 빌드
PyInstaller를 사용하여 단일 실행 파일 생성
"""
import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """PyInstaller 설치"""
    print("📦 PyInstaller 설치 중...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller 설치 완료")
        return True
    except subprocess.CalledProcessError:
        print("❌ PyInstaller 설치 실패")
        return False

def create_spec_file():
    """PyInstaller 스펙 파일 생성"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('frontend', 'frontend'),
        ('backend', 'backend'),
    ],
    hiddenimports=[
        'uvicorn',
        'fastapi',
        'pandas', 
        'openpyxl',
        'numpy'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ExcelCompareTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    coerce_to_data_targeting=True,
    icon=None,
)
'''
    
    with open("ExcelCompareTool.spec", "w") as f:
        f.write(spec_content)
    
    print("✅ 스펙 파일 생성 완료")

def build_executable():
    """실행 파일 빌드"""
    print("🔨 실행 파일 빌드 중... (시간이 걸릴 수 있습니다)")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller", 
            "--onefile",
            "--name=ExcelCompareTool",
            "--add-data=frontend:frontend",
            "--add-data=backend:backend", 
            "--hidden-import=uvicorn",
            "--hidden-import=fastapi",
            "--hidden-import=pandas",
            "--hidden-import=openpyxl",
            "run.py"
        ])
        
        print("✅ 빌드 완료!")
        
        # 결과 파일 확인
        if sys.platform == "win32":
            exe_file = "dist/ExcelCompareTool.exe"
        else:
            exe_file = "dist/ExcelCompareTool"
            
        if Path(exe_file).exists():
            size_mb = os.path.getsize(exe_file) / (1024 * 1024)
            print(f"📁 생성된 파일: {exe_file} ({size_mb:.1f}MB)")
            print(f"📋 사용법: ./{exe_file}")
        else:
            print("❌ 실행 파일이 생성되지 않았습니다.")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 빌드 실패: {e}")

def main():
    print("=" * 50)
    print("🔨 Excel Compare Tool 실행 파일 빌더")
    print("=" * 50)
    
    # PyInstaller 설치
    if not install_pyinstaller():
        return
    
    # 빌드 실행
    build_executable()
    
    print("\n" + "=" * 50)
    print("📝 배포 안내:")
    print("1. dist/ 폴더의 실행 파일을 복사")
    print("2. 대상 컴퓨터에서 실행")
    print("3. Python/Node.js 설치 불필요!")
    print("=" * 50)

if __name__ == "__main__":
    main()