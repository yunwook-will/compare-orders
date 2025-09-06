#!/bin/bash

# macOS 앱 번들 생성 스크립트

APP_NAME="Excel Compare"
APP_DIR="$HOME/Desktop/$APP_NAME.app"

echo "📱 Mac 앱 생성중..."

# 앱 디렉토리 구조 생성
mkdir -p "$APP_DIR/Contents/MacOS"
mkdir -p "$APP_DIR/Contents/Resources"

# 실행 스크립트 생성
cat > "$APP_DIR/Contents/MacOS/Excel Compare" << 'EOF'
#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT_PATH="$(dirname "$(dirname "$(dirname "$0")")")/run.py"

# Terminal에서 실행
osascript -e 'tell application "Terminal"
    do script "python3 '"$SCRIPT_PATH"'"
    activate
end tell'
EOF

chmod +x "$APP_DIR/Contents/MacOS/Excel Compare"

# Info.plist 생성
cat > "$APP_DIR/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Excel Compare</string>
    <key>CFBundleIdentifier</key>
    <string>com.example.excelcompare</string>
    <key>CFBundleName</key>
    <string>Excel Compare</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleIconFile</key>
    <string>icon</string>
</dict>
</plist>
EOF

echo "✅ 앱이 데스크톱에 생성되었습니다: $APP_DIR"
echo "더블클릭하여 실행하세요!"