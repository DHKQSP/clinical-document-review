"""
Build executable files for Windows
Python 설치 없이 실행 가능한 .exe 파일 생성

실행 방법:
    pip install pyinstaller
    python build_exe.py
"""

import subprocess
import sys
import os
from pathlib import Path


def build_cli():
    """CLI 버전 빌드"""
    print("=" * 60)
    print("CLI 버전 빌드 시작...")
    print("=" * 60)

    cmd = [
        "pyinstaller",
        "--name=ClinicalReview",
        "--onefile",  # 단일 파일로 생성
        "--icon=icon.ico" if Path("icon.ico").exists() else "",
        "--add-data=config;config",  # config 폴더 포함
        "--add-data=src;src",  # src 폴더 포함
        "--hidden-import=pdfplumber",
        "--hidden-import=yaml",
        "--hidden-import=click",
        "--hidden-import=jinja2",
        "--hidden-import=tabulate",
        "--hidden-import=colorama",
        "--hidden-import=tqdm",
        "--collect-all=pdfplumber",
        "--noconfirm",
        "cli.py"
    ]

    # Remove empty strings
    cmd = [c for c in cmd if c]

    subprocess.run(cmd, check=True)
    print("\n✅ CLI 버전 빌드 완료: dist/ClinicalReview.exe")


def build_web():
    """웹 앱 버전 빌드"""
    print("\n" + "=" * 60)
    print("웹 앱 버전 빌드 시작...")
    print("=" * 60)

    cmd = [
        "pyinstaller",
        "--name=ClinicalReview-Web",
        "--onefile",
        "--windowed",  # 콘솔창 숨김
        "--icon=icon.ico" if Path("icon.ico").exists() else "",
        "--add-data=config;config",
        "--add-data=src;src",
        "--add-data=.streamlit;.streamlit",  # Streamlit 설정
        "--hidden-import=streamlit",
        "--hidden-import=pdfplumber",
        "--hidden-import=yaml",
        "--hidden-import=jinja2",
        "--hidden-import=tabulate",
        "--collect-all=streamlit",
        "--collect-all=pdfplumber",
        "--noconfirm",
        "web_launcher.py"
    ]

    # Remove empty strings
    cmd = [c for c in cmd if c]

    subprocess.run(cmd, check=True)
    print("\n✅ 웹 앱 버전 빌드 완료: dist/ClinicalReview-Web.exe")


def main():
    """메인 빌드 함수"""
    print("\n🏗️  임상문서 검토 도구 실행 파일 빌드\n")

    # PyInstaller 설치 확인
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller가 설치되지 않았습니다.")
        print("다음 명령어로 설치하세요:")
        print("  pip install pyinstaller")
        sys.exit(1)

    # 빌드 옵션 선택
    print("빌드할 버전을 선택하세요:")
    print("  1. CLI 버전만 (빠르고 가벼움)")
    print("  2. 웹 앱 버전만 (사용하기 쉬움)")
    print("  3. 둘 다 빌드")

    choice = input("\n선택 (1/2/3): ").strip()

    if choice == "1":
        build_cli()
    elif choice == "2":
        build_web()
    elif choice == "3":
        build_cli()
        build_web()
    else:
        print("❌ 잘못된 선택입니다.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("✅ 빌드 완료!")
    print("=" * 60)
    print("\n생성된 파일 위치: dist/ 폴더")
    print("\n배포 방법:")
    print("  1. dist/ 폴더의 .exe 파일을 복사")
    print("  2. 사용자에게 전달")
    print("  3. Python 설치 없이 바로 실행 가능!")


if __name__ == "__main__":
    main()
