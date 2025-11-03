# 보안 가이드

## 🔒 임상문서 보안 요구사항

임상시험 문서(프로토콜, IB, SAP)는 다음과 같은 민감한 정보를 포함합니다:

- 신약 개발 정보 (영업 비밀)
- 임상시험 설계 (경쟁사 민감 정보)
- 환자 선정 기준
- 통계 분석 방법
- 규제 제출 전 문서

## ⚠️ 절대 하지 말아야 할 것

### ❌ 클라우드 서비스에 업로드 금지

**사용하면 안 되는 서비스**:
- GitHub Codespaces ❌
- Google Colab ❌
- AWS/Azure 공용 인스턴스 ❌
- 외부 AI 서비스 (ChatGPT, Claude 등) ❌
- 파일 공유 서비스 (Dropbox, WeTransfer 등) ❌

**이유**:
1. 데이터가 서드파티 서버에 저장됨
2. 클라우드 제공자가 데이터 접근 가능
3. 규제 위반 (GCP, HIPAA, GDPR 등)
4. 영업 비밀 유출 위험
5. 회사 보안 정책 위반

## ✅ 안전한 사용 방법

### 권장 방법 1: 회사 내부 서버 (최고 보안) ⭐⭐⭐

```
┌─────────────────────────────────────────┐
│     회사 내부 네트워크 (격리됨)           │
│                                         │
│  ┌──────────┐         ┌─────────────┐  │
│  │ 내부서버  │ ←─────→ │  직원 PC    │  │
│  │ (Python) │         │  (브라우저)  │  │
│  └──────────┘         └─────────────┘  │
│       ↑                                │
│   데이터는                              │
│   여기서만 처리                          │
└─────────────────────────────────────────┘
         ↓
    인터넷 연결 없음
    외부 전송 없음
```

**설정 방법**:
1. IT 부서에 내부 서버 설치 요청
2. 방화벽으로 외부 통신 차단
3. VPN으로만 접근 허용

### 권장 방법 2: Docker 격리 환경 ⭐⭐

```bash
# 완전 격리 모드 (인터넷 차단)
docker run -d \
  --name clinical-review \
  --network none \
  -p 127.0.0.1:8501:8501 \
  --security-opt no-new-privileges \
  --cap-drop ALL \
  --read-only \
  --tmpfs /tmp \
  clinical-review:latest
```

**장점**:
- ✅ 컨테이너 완전 격리
- ✅ 외부 네트워크 차단
- ✅ localhost(127.0.0.1)로만 접근
- ✅ 임시 데이터만 메모리 사용

### 권장 방법 3: 로컬 실행 (개인 PC)

```bash
# 인터넷 연결 없이 실행 가능
python cli.py review document.pdf --type protocol
```

**조건**:
- PC에 로컬 파일 저장 허용됨
- Python 설치 가능
- 오프라인 실행 가능

## 🛡️ 보안 체크리스트

### 배포 전 확인사항

- [ ] 내부 네트워크에서만 접근 가능한가?
- [ ] 외부 인터넷 연결이 차단되었는가?
- [ ] 파일 업로드 후 자동 삭제되는가?
- [ ] 로그에 민감한 정보가 기록되지 않는가?
- [ ] HTTPS 사용하는가? (프로덕션)
- [ ] 접근 제어(인증)가 설정되었는가?
- [ ] IT 보안팀 승인을 받았는가?

### 운영 중 확인사항

- [ ] 정기적으로 로그 검토
- [ ] 비정상 접근 모니터링
- [ ] 업데이트 및 패치 적용
- [ ] 백업 및 복구 계획
- [ ] 접근 권한 정기 검토

## 🔐 추가 보안 강화

### 1. 인증 추가

Streamlit 앱에 Basic Auth 추가:

```python
# .streamlit/config.toml
[server]
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

환경변수로 비밀번호 설정:

```python
import os
import streamlit as st

def check_password():
    """Simple password check"""
    password = st.text_input("비밀번호", type="password")
    if password == os.getenv("APP_PASSWORD"):
        return True
    elif password:
        st.error("잘못된 비밀번호")
    return False

if not check_password():
    st.stop()
```

### 2. HTTPS 사용 (프로덕션)

```bash
streamlit run web_app.py \
  --server.sslCertFile=/path/to/cert.pem \
  --server.sslKeyFile=/path/to/key.pem
```

### 3. 로그 최소화

```python
# config.toml
[logger]
level = "error"  # info/debug 대신
```

### 4. IP 제한

방화벽 또는 nginx로 특정 IP만 허용:

```nginx
location / {
    allow 192.168.1.0/24;  # 회사 내부 IP만
    deny all;
    proxy_pass http://localhost:8501;
}
```

### 5. 세션 타임아웃

```python
# Streamlit 앱에 추가
import time
SESSION_TIMEOUT = 3600  # 1시간

if 'last_activity' not in st.session_state:
    st.session_state.last_activity = time.time()

if time.time() - st.session_state.last_activity > SESSION_TIMEOUT:
    st.error("세션이 만료되었습니다.")
    st.stop()
```

## 📋 규제 준수

### GCP (Good Clinical Practice)

- ✅ 데이터 무결성 (Data Integrity)
- ✅ 감사 추적 (Audit Trail) - 로그 기록
- ✅ 접근 제어 (Access Control)
- ✅ 전자 서명 (해당시)

### 21 CFR Part 11 (FDA)

전자 기록 관련 규제 준수 필요시:
- 전자 서명
- 감사 추적
- 시스템 검증

### GDPR / 개인정보보호법

환자 정보 포함 시:
- 개인정보 암호화
- 접근 로그 기록
- 데이터 최소화

## 🚨 보안 사고 대응

### 의심되는 경우

1. **즉시 서비스 중단**
   ```bash
   docker-compose down
   # 또는
   kill <process_id>
   ```

2. **IT 보안팀 연락**

3. **로그 보존**
   ```bash
   docker logs clinical-review > incident_log.txt
   ```

4. **영향 범위 조사**

## 📞 문의

보안 관련 문제 발견 시:
- GitHub Issues (민감하지 않은 내용만)
- 회사 IT 보안팀
- 이메일: [보안 담당자 이메일]

## 📚 참고 자료

- ICH GCP Guidelines
- FDA 21 CFR Part 11
- GDPR Documentation
- ISO 27001 (정보보안)
- 회사 내부 보안 정책
