@echo off
REM Windows용 CLI 버전 빌드 스크립트

echo ============================================================
echo 임상문서 검토 도구 - CLI 버전 빌드
echo ============================================================
echo.

REM PyInstaller 설치 확인
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller가 설치되지 않았습니다. 설치 중...
    pip install pyinstaller
)

echo.
echo CLI 버전 빌드 시작...
echo.

pyinstaller clinical-review.spec

if errorlevel 1 (
    echo.
    echo ❌ 빌드 실패!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ✅ 빌드 완료!
echo ============================================================
echo.
echo 생성된 파일: dist\ClinicalReview.exe
echo.
echo 사용 방법:
echo   1. dist\ClinicalReview.exe를 원하는 위치에 복사
echo   2. 명령 프롬프트에서 실행:
echo      ClinicalReview.exe review document.pdf --type protocol
echo.
pause
