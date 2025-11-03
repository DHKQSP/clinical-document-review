# Docker를 사용한 안전한 실행

## Docker 사용의 장점

✅ **완전히 격리된 환경**
- 컨테이너 내부에서만 동작
- 호스트 시스템과 분리
- 외부 네트워크 차단 가능

✅ **재현 가능한 환경**
- 어디서나 동일하게 동작
- 의존성 충돌 없음

✅ **보안 강화**
- 최소 권한으로 실행
- 읽기 전용 파일 시스템 가능
- 네트워크 격리

## 설치 및 실행

### 1. Docker 설치

**Windows**:
- Docker Desktop 설치: https://www.docker.com/products/docker-desktop

**Linux**:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### 2. 이미지 빌드

```bash
# 프로젝트 디렉토리에서
docker build -t clinical-review:latest .
```

### 3. 컨테이너 실행

**방법 A: Docker 명령어**
```bash
docker run -d \
  --name clinical-review \
  -p 8501:8501 \
  --security-opt no-new-privileges \
  --cap-drop ALL \
  clinical-review:latest
```

**방법 B: Docker Compose (권장)**
```bash
docker-compose up -d
```

### 4. 브라우저에서 접속

```
http://localhost:8501
```

### 5. 중지 및 제거

```bash
# 중지
docker-compose down

# 또는
docker stop clinical-review
docker rm clinical-review
```

## 네트워크 격리 (최고 보안)

외부 인터넷 차단된 완전 격리 모드:

```bash
docker run -d \
  --name clinical-review \
  -p 8501:8501 \
  --network none \
  --security-opt no-new-privileges \
  --cap-drop ALL \
  --read-only \
  --tmpfs /tmp \
  clinical-review:latest
```

이렇게 하면:
- ❌ 외부 인터넷 접근 불가
- ❌ 다른 컨테이너와 통신 불가
- ✅ 로컬호스트(127.0.0.1)로만 접근 가능
- ✅ 완전히 격리된 환경

## 회사 환경에서 사용

### 내부 서버에 배포

```bash
# 서버에서 실행
docker-compose up -d

# 다른 컴퓨터에서 브라우저로 접속
http://<서버IP>:8501
```

### 보안 강화 설정

```yaml
# docker-compose.override.yml
version: '3.8'

services:
  clinical-review:
    # 외부 인터넷 차단
    networks:
      - isolated

    # CPU/메모리 제한
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G

    # 로그 제한
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  isolated:
    internal: true
```

## 문제 해결

### 포트 충돌

다른 포트 사용:
```bash
docker run -p 8080:8501 clinical-review:latest
```

### 로그 확인

```bash
docker logs clinical-review
```

### 컨테이너 내부 접근

```bash
docker exec -it clinical-review /bin/bash
```

## IT 부서 제공 정보

**보안 담당자에게 제공할 정보**:

1. **외부 통신**: 없음 (완전 격리 가능)
2. **데이터 저장**: 임시 메모리만 사용, 영구 저장 없음
3. **포트**: 8501 (변경 가능)
4. **권한**: 최소 권한으로 실행
5. **격리**: Docker 컨테이너로 완전 격리
6. **감사**: 모든 활동 로그 기록 가능
