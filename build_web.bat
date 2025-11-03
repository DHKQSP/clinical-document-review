@echo off
REM Windows용 웹 앱 버전 빌드 스크립트

echo ============================================================
echo 임상문서 검토 도구 - 웹 앱 버전 빌드
echo ============================================================
echo.

REM PyInstaller 설치 확인
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller가 설치되지 않았습니다. 설치 중...
    pip install pyinstaller
)

echo.
echo 웹 앱 버전 빌드 시작...
echo 주의: 이 빌드는 시간이 걸릴 수 있습니다 (5-10분)
echo.

pyinstaller clinical-review-web.spec

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
echo 생성된 파일: dist\ClinicalReview-Web.exe
echo.
echo 사용 방법:
echo   1. dist\ClinicalReview-Web.exe를 더블클릭
echo   2. 자동으로 브라우저가 열립니다
echo   3. 브라우저에서 PDF 업로드하고 검토
echo.
pause
