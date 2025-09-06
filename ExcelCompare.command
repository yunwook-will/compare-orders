#!/bin/bash

# 현재 스크립트 경로 찾기
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Terminal 앱에서 실행
osascript -e 'tell application "Terminal"
    do script "cd '"$DIR"' && ./start.sh"
    activate
end tell'