# 실행 파일(.exe) 빌드 가이드

Python 설치 없이 실행 가능한 독립 실행 프로그램 만들기

## 🎯 왜 .exe로 만드나요?

- ✅ Python 설치 불필요
- ✅ 사용자가 바로 실행 가능
- ✅ 회사 컴퓨터에 배포하기 쉬움
- ✅ USB에 넣어서 이동 가능
- ✅ 더블클릭으로 실행

## 📦 2가지 버전

### 1. CLI 버전 (명령줄)
- **파일 크기**: ~50MB
- **장점**: 가볍고 빠름, 스크립트 자동화 가능
- **사용법**: 명령 프롬프트에서 실행
- **추천**: 개발자, 반복 작업

### 2. 웹 앱 버전 (브라우저)
- **파일 크기**: ~150-200MB
- **장점**: 사용하기 쉬움, GUI 인터페이스
- **사용법**: 더블클릭 → 브라우저 자동 열림
- **추천**: 일반 사용자, 비개발자

---

## 🛠️ 빌드 방법

### 필요 사항
- Python 3.8 이상
- PyInstaller

### 방법 1: 자동 빌드 (간편) ⭐

**Windows에서:**

```bash
# CLI 버전만 빌드
build_cli.bat

# 웹 앱 버전만 빌드
build_web.bat

# 또는 Python 스크립트 사용
python build_exe.py
```

**Linux/Mac에서:**

```bash
# PyInstaller 설치
pip install pyinstaller

# CLI 버전
pyinstaller clinical-review.spec

# 웹 앱 버전
pyinstaller clinical-review-web.spec
```

### 방법 2: 수동 빌드 (고급)

```bash
# 1. PyInstaller 설치
pip install pyinstaller

# 2. CLI 버전 빌드
pyinstaller --name=ClinicalReview \
    --onefile \
    --add-data="config:config" \
    --add-data="src:src" \
    --hidden-import=pdfplumber \
    cli.py

# 3. 웹 앱 버전 빌드
pyinstaller --name=ClinicalReview-Web \
    --onefile \
    --add-data="config:config" \
    --add-data="src:src" \
    --add-data="web_app.py:." \
    --hidden-import=streamlit \
    --hidden-import=pdfplumber \
    --collect-all=streamlit \
    web_launcher.py
```

---

## 📂 빌드 결과

빌드 완료 후 다음 위치에 파일이 생성됩니다:

```
dist/
├── ClinicalReview.exe        (CLI 버전)
└── ClinicalReview-Web.exe    (웹 앱 버전)
```

---

## 🚀 배포 방법

### 1. USB 드라이브로 배포

```
USB:/
└── ClinicalReview/
    ├── ClinicalReview.exe        (또는)
    ├── ClinicalReview-Web.exe
    └── README.txt                (사용 설명)
```

사용자는 USB에서 직접 실행 가능!

### 2. 네트워크 공유 폴더

```
\\company-server\shared\ClinicalReview\
├── ClinicalReview.exe
└── ClinicalReview-Web.exe
```

직원들이 공유 폴더에서 복사해서 사용

### 3. 이메일 배포

**주의**: 회사 보안 정책 확인!
- .exe 파일은 이메일 차단될 수 있음
- .zip으로 압축 후 전송 권장

### 4. 내부 소프트웨어 저장소

회사 IT 부서의 소프트웨어 배포 시스템 이용

---

## 📖 사용 방법

### CLI 버전 사용법

```bash
# 도움말
ClinicalReview.exe --help

# 문서 검토
ClinicalReview.exe review protocol.pdf --type protocol

# 문서 정보
ClinicalReview.exe info document.pdf

# 텍스트 검색
ClinicalReview.exe search document.pdf --pattern "version"
```

### 웹 앱 버전 사용법

1. **실행**: `ClinicalReview-Web.exe` 더블클릭
2. **대기**: 자동으로 브라우저가 열립니다
3. **업로드**: PDF 파일 드래그 앤 드롭
4. **검토**: "검토 시작" 버튼 클릭
5. **다운로드**: 결과 보고서 다운로드

**종료**: 콘솔 창 닫기

---

## ⚙️ 고급 옵션

### 파일 크기 줄이기

**UPX 압축 사용**:
```bash
# UPX 다운로드: https://upx.github.io/
pyinstaller --upx-dir=C:\upx clinical-review.spec
```

**특정 모듈 제외**:
```python
# .spec 파일에서 excludes 설정
excludes=[
    'matplotlib',
    'IPython',
    'tkinter',
]
```

### 아이콘 추가

```bash
# .ico 파일 준비
pyinstaller --icon=icon.ico clinical-review.spec
```

### 디지털 서명 (Windows)

회사 코드 서명 인증서 사용:
```bash
signtool sign /f certificate.pfx /p password ClinicalReview.exe
```

---

## 🐛 문제 해결

### 문제 1: "Failed to execute script"

**원인**: 필요한 파일이 포함되지 않음

**해결**:
```bash
# --add-data로 필요한 파일 명시
pyinstaller --add-data "config:config" clinical-review.spec
```

### 문제 2: "ImportError: No module named ..."

**원인**: 숨겨진 import가 감지되지 않음

**해결**:
```bash
# --hidden-import로 명시
pyinstaller --hidden-import=pdfplumber clinical-review.spec
```

### 문제 3: 파일 크기가 너무 큼

**원인**: 불필요한 라이브러리 포함

**해결**:
```python
# .spec 파일에서 excludes 추가
excludes=['matplotlib', 'numpy.distutils']
```

### 문제 4: 실행 시 Windows Defender 경고

**원인**: 서명되지 않은 .exe 파일

**해결**:
1. IT 부서에 코드 서명 인증서 요청
2. 또는 사용자에게 "실행 허용" 안내
3. 회사 백신 예외 목록에 추가

---

## 📊 성능 비교

| 버전 | 파일 크기 | 시작 시간 | 사용 난이도 | 메모리 |
|------|-----------|-----------|-------------|--------|
| CLI  | ~50MB     | 1-2초     | 중급        | ~100MB |
| 웹앱 | ~150MB    | 3-5초     | 초급        | ~200MB |

---

## 🔒 보안 고려사항

### 빌드 환경
- 깨끗한 가상환경에서 빌드
- 악성 코드 스캔 실행
- 체크섬(hash) 기록

### 배포 시
- 디지털 서명 추가 (가능한 경우)
- SHA256 해시 제공
- 안전한 채널로 배포

### 사용자 안내
```
SHA256: [파일의 해시값]
이 값을 확인하여 파일이 변조되지 않았는지 검증하세요.
```

---

## 📝 배포 체크리스트

빌드 및 배포 전 확인:

- [ ] 모든 기능이 정상 작동하는가?
- [ ] 테스트 문서로 검증했는가?
- [ ] 파일 크기가 적당한가?
- [ ] 바이러스 스캔 완료했는가?
- [ ] 사용 설명서를 작성했는가?
- [ ] IT 부서 승인을 받았는가?
- [ ] 버전 번호를 명시했는가?
- [ ] 체크섬을 기록했는가?

---

## 🎁 사용자 배포 패키지 예시

```
ClinicalReview-v1.0.0/
├── ClinicalReview.exe          (또는 ClinicalReview-Web.exe)
├── README.txt                  (사용 설명)
├── 예제_프로토콜.pdf            (테스트용, 선택사항)
├── 문제해결.txt                 (FAQ)
└── SHA256.txt                  (파일 해시)
```

**README.txt 예시**:
```
임상문서 자동 검토 도구 v1.0.0

사용 방법:
1. ClinicalReview.exe를 더블클릭
2. PDF 파일 업로드
3. 문서 타입 선택 (Protocol/IB/SAP)
4. "검토 시작" 클릭
5. 결과 확인 및 다운로드

문의: [담당자 이메일]
```

---

## 🔄 업데이트 배포

새 버전 빌드 시:

1. **버전 관리**
   ```python
   # src/__init__.py
   __version__ = "1.1.0"
   ```

2. **변경 사항 기록**
   ```
   CHANGELOG.md
   v1.1.0 (2025-01-15)
   - 새 기능 추가
   - 버그 수정
   ```

3. **재빌드**
   ```bash
   python build_exe.py
   ```

4. **배포**
   - 기존 파일 백업
   - 새 버전 배포
   - 사용자에게 공지

---

## 💡 팁

### 빠른 테스트
```bash
# 빌드 후 즉시 테스트
dist\ClinicalReview.exe --version
```

### 디버그 모드
```python
# .spec 파일에서
debug=True,
console=True,  # 콘솔 표시로 오류 확인
```

### 크로스 플랫폼
```bash
# Linux/Mac에서도 빌드 가능
# 단, 각 OS에서 별도로 빌드 필요
# Windows에서 빌드 → Windows용 .exe만 생성
```

---

## 🎓 학습 자료

- PyInstaller 공식 문서: https://pyinstaller.org/
- Python 패키징 가이드: https://packaging.python.org/
- 코드 서명: https://docs.microsoft.com/windows/win32/seccrypto/

---

**빌드 및 배포 성공을 기원합니다!** 🎉
