# 웹 인터페이스 사용 가이드

## 웹 앱 실행 방법

### 1. Streamlit 설치

```bash
pip install streamlit
# 또는
pip install -r requirements_web.txt
```

### 2. 웹 앱 실행

```bash
streamlit run web_app.py
```

### 3. 브라우저에서 접속

자동으로 브라우저가 열립니다. 또는 다음 주소로 접속:
- http://localhost:8501

## 사용 방법

1. **문서 업로드**: PDF 파일을 드래그 앤 드롭 또는 선택
2. **문서 타입 선택**: Protocol, IB, SAP 중 선택
3. **검토 시작**: "검토 시작" 버튼 클릭
4. **결과 확인**: 웹 페이지에서 결과 확인
5. **보고서 다운로드**: HTML 또는 텍스트 보고서 다운로드

## 네트워크에서 접근

같은 네트워크의 다른 컴퓨터에서 접근하려면:

```bash
streamlit run web_app.py --server.address 0.0.0.0
```

그 후 다른 컴퓨터에서:
```
http://<서버IP>:8501
```

## 포트 변경

기본 포트(8501)를 변경하려면:

```bash
streamlit run web_app.py --server.port 8080
```

## 회사 환경에서 사용

### 옵션 1: 로컬 서버에서 실행

회사 서버나 개발 머신에서 실행하고, 브라우저로 접속

### 옵션 2: 클라우드 배포

- **Streamlit Community Cloud** (무료): https://streamlit.io/cloud
- **Heroku**: https://www.heroku.com/
- **AWS/Azure**: 회사 클라우드 인프라 사용

### 옵션 3: Docker 컨테이너

Docker가 허용된 환경이라면 컨테이너로 실행 가능

## 보안 고려사항

- 모든 처리는 서버 메모리에서만 발생
- 업로드된 파일은 임시 저장 후 자동 삭제
- 외부 네트워크 통신 없음
- HTTPS 설정 권장 (프로덕션 환경)

## 문제 해결

### "Address already in use" 에러

다른 포트 사용:
```bash
streamlit run web_app.py --server.port 8502
```

### 방화벽 문제

회사 방화벽에서 포트 허용 필요 (IT 부서 문의)

### 느린 성능

큰 PDF 파일은 처리 시간이 오래 걸릴 수 있습니다.
