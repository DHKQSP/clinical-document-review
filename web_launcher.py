"""
Web App Launcher - 브라우저에서 자동으로 웹 앱 실행

.exe로 빌드되면 더블클릭으로 웹 앱이 브라우저에서 열립니다.
"""

import sys
import os
import subprocess
import webbrowser
import time
from pathlib import Path
import socket


def find_free_port():
    """사용 가능한 포트 찾기"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def main():
    """웹 앱 실행 및 브라우저 열기"""

    # 실행 파일의 경로 찾기
    if getattr(sys, 'frozen', False):
        # PyInstaller로 빌드된 경우
        application_path = Path(sys._MEIPASS)
    else:
        # 일반 Python 스크립트 실행
        application_path = Path(__file__).parent

    # 환경 변수 설정
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'

    # Streamlit 설정 파일 생성
    streamlit_dir = Path.home() / '.streamlit'
    streamlit_dir.mkdir(exist_ok=True)

    config_path = streamlit_dir / 'config.toml'
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write("""
[server]
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
serverAddress = "localhost"

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
""")

    # 포트 찾기
    port = find_free_port()

    print("=" * 60)
    print("임상문서 자동 검토 도구")
    print("=" * 60)
    print(f"\n🚀 웹 서버 시작 중... (포트: {port})")
    print("📱 잠시 후 브라우저가 자동으로 열립니다...")
    print("\n종료하려면 이 창을 닫으세요.")
    print("=" * 60 + "\n")

    # Streamlit 실행
    web_app_path = application_path / 'web_app.py'

    # 웹 서버 프로세스 시작
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(web_app_path),
        f"--server.port={port}",
        "--server.address=localhost",
        "--server.headless=true"
    ]

    # 프로세스 시작
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # 서버가 준비될 때까지 대기
    time.sleep(3)

    # 브라우저 열기
    url = f"http://localhost:{port}"
    print(f"🌐 브라우저 열기: {url}\n")
    webbrowser.open(url)

    # 서버 실행 유지
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\n\n⏹️  서버 종료 중...")
        process.terminate()
        process.wait()
        print("✅ 종료 완료")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        input("\nEnter 키를 눌러 종료...")
