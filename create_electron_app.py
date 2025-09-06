#!/usr/bin/env python3
"""
Excel Compare Tool - Electron 앱 생성기
완전히 독립적인 데스크톱 애플리케이션 생성
"""
import os
import json
import subprocess
from pathlib import Path

def create_electron_structure():
    """Electron 앱 구조 생성"""
    print("📱 Electron 앱 구조 생성 중...")
    
    app_dir = Path("electron-app")
    app_dir.mkdir(exist_ok=True)
    
    # package.json
    package_json = {
        "name": "excel-compare-tool",
        "version": "1.0.0", 
        "description": "Excel 파일 비교 도구",
        "main": "main.js",
        "scripts": {
            "start": "electron .",
            "build": "electron-builder",
            "dist": "electron-builder --publish=never"
        },
        "devDependencies": {
            "electron": "^27.0.0",
            "electron-builder": "^24.6.0"
        },
        "build": {
            "appId": "com.example.excelcompare",
            "productName": "Excel Compare Tool",
            "directories": {
                "output": "dist"
            },
            "files": [
                "**/*",
                "!node_modules",
                "!src",
                "!dist"
            ],
            "mac": {
                "category": "public.app-category.productivity"
            },
            "win": {
                "target": "nsis"
            },
            "linux": {
                "target": "AppImage"
            }
        }
    }
    
    with open(app_dir / "package.json", "w") as f:
        json.dump(package_json, f, indent=2)
    
    # main.js (Electron 메인 프로세스)
    main_js = '''const { app, BrowserWindow, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

let mainWindow;
let backendProcess;
let frontendProcess;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true
        },
        icon: path.join(__dirname, 'icon.png')
    });

    // 스플래시 화면 표시
    mainWindow.loadFile('loading.html');
    
    // 서버 시작
    startServers();
}

function startServers() {
    console.log('Starting servers...');
    
    // Python 백엔드 시작
    const backendPath = path.join(__dirname, 'backend');
    backendProcess = spawn('python3', [
        '-m', 'uvicorn', 'app.main:app', '--port', '8000'
    ], { 
        cwd: backendPath,
        stdio: 'pipe'
    });
    
    // Frontend 시작 (빌드된 정적 파일 서빙)
    setTimeout(() => {
        mainWindow.loadURL('http://localhost:3000');
    }, 5000);
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    // 서버 프로세스 종료
    if (backendProcess) {
        backendProcess.kill();
    }
    if (frontendProcess) {
        frontendProcess.kill();
    }
    
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
'''
    
    with open(app_dir / "main.js", "w") as f:
        f.write(main_js)
    
    # loading.html
    loading_html = '''<!DOCTYPE html>
<html>
<head>
    <title>Excel Compare Tool</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .loader {
            text-align: center;
        }
        .spinner {
            border: 4px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top: 4px solid #fff;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="loader">
        <div class="spinner"></div>
        <h2>Excel Compare Tool</h2>
        <p>서버를 시작하는 중입니다...</p>
    </div>
</body>
</html>'''
    
    with open(app_dir / "loading.html", "w") as f:
        f.write(loading_html)
    
    print("✅ Electron 앱 구조 생성 완료")
    return app_dir

def build_electron_app():
    """Electron 앱 빌드"""
    app_dir = create_electron_structure()
    
    print("📦 Electron 의존성 설치 중...")
    subprocess.run(["npm", "install"], cwd=app_dir)
    
    print("🔨 Electron 앱 빌드 중...")
    subprocess.run(["npm", "run", "dist"], cwd=app_dir)
    
    print("✅ Electron 앱 빌드 완료!")
    print(f"📁 결과물: {app_dir}/dist/")

if __name__ == "__main__":
    print("=" * 50)
    print("📱 Excel Compare Tool - Electron 앱 빌더")
    print("=" * 50)
    
    try:
        build_electron_app()
    except Exception as e:
        print(f"❌ 오류: {e}")