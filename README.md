# 임상문서 자동 검토 도구

> 프로토콜, IB, SAP 문서를 로컬에서 안전하게 자동 검토하는 도구

## 🔒 보안 우선 설계

**모든 문서는 로컬에서만 처리됩니다.** 어떠한 데이터도 외부 서버로 전송되지 않으며, 민감한 임상문서를 안전하게 검토할 수 있습니다.

- ✅ 완전 로컬 처리 - 외부 업로드 없음
- ✅ 오픈소스 라이브러리 사용
- ✅ 선택적 로컬 LLM 통합 (Ollama)

## 📋 지원 문서 타입

1. **Protocol (프로토콜)**
   - ICH-GCP 기반 검토 항목
   - 연구 목적, 설계, 대상자 선정, 평가변수 등 확인

2. **Investigator's Brochure (IB, 임상시험자 자료집)**
   - 시험약 정보 완전성 검토
   - 비임상/임상 자료, 안전성 정보 확인

3. **Statistical Analysis Plan (SAP, 통계분석계획서)**
   - 통계 분석 방법론 검토
   - 표본크기, 분석군, 통계검정 방법 확인

## 🚀 빠른 시작

### 1. 필수 요구사항

- Python 3.8 이상
- PDF 문서 (현재는 PDF만 지원)

### 2. 설치

```bash
# 저장소 클론
git clone <repository-url>
cd clinical-document-review

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 3. 기본 사용법

```bash
# 프로토콜 검토
python cli.py review protocol.pdf --type protocol

# IB 검토 (HTML + 텍스트 보고서 생성)
python cli.py review ib_document.pdf --type ib --format both

# SAP 검토 (출력 경로 지정)
python cli.py review sap.pdf --type sap --output reports/my_sap_report.html
```

## 📖 상세 사용법

### 문서 검토

```bash
python cli.py review <문서경로> --type <타입> [옵션]
```

**필수 인자:**
- `문서경로`: 검토할 PDF 파일 경로
- `--type, -t`: 문서 타입 (`protocol`, `ib`, `sap`)

**선택 옵션:**
- `--output, -o`: 보고서 저장 경로 (기본: `reports/<파일명>_report.html`)
- `--format, -f`: 보고서 형식 (`html`, `text`, `both`) (기본: `html`)

**예시:**

```bash
# 프로토콜 검토 - HTML 보고서 생성
python cli.py review documents/protocol_v2.pdf --type protocol

# IB 검토 - HTML과 텍스트 보고서 모두 생성
python cli.py review documents/ib.pdf --type ib --format both

# SAP 검토 - 특정 경로에 저장
python cli.py review sap_final.pdf --type sap -o output/sap_review.html
```

### 문서 정보 확인

```bash
python cli.py info <문서경로>
```

문서의 메타데이터, 페이지 수, 발견된 섹션 등을 표시합니다.

```bash
python cli.py info protocol.pdf
```

### 텍스트 검색

```bash
python cli.py search <문서경로> --pattern <정규표현식>
```

문서에서 특정 패턴을 검색합니다.

```bash
# 버전 번호 검색
python cli.py search protocol.pdf --pattern "version.*\d+"

# 날짜 검색
python cli.py search protocol.pdf --pattern "\d{4}-\d{2}-\d{2}"
```

### 검토 항목 목록 확인

```bash
python cli.py list-checks
```

모든 문서 타입에 대한 검토 항목 목록을 표시합니다.

## 📊 검토 항목

### Protocol 검토 항목 (총 8개 섹션)

1. **필수 정보**: 제목, 버전, 일자, 의뢰자
2. **연구 목적 및 설계**: 주요/부차적 목적, 연구설계, 대상자 수
3. **대상자 선정 기준**: 선정/제외/중단 기준
4. **치료 및 투여**: 용량, 투여경로, 기간, 병용약물
5. **평가 및 절차**: 평가변수, 방문일정
6. **안전성**: 이상반응 보고, SAE, 안전성 모니터링
7. **통계 분석**: 분석계획, 분석군
8. **윤리적 고려사항**: IRB, 동의서, 개인정보보호

### IB 검토 항목 (총 8개 섹션)

1. **필수 정보**: 제목, 버전, 의뢰자
2. **요약**: 시험약 요약, 화학명
3. **물리화학적 특성**: 물리화학 특성, 제형
4. **비임상 자료**: 약리, 약동학, 독성
5. **임상 자료**: 임상약리, PK/PD, 유효성
6. **안전성 정보**: 이상반응, SAE, 금기사항, 약물상호작용
7. **특수 집단**: 임신/수유, 소아/노인, 신장애/간장애
8. **참고문헌 및 부록**

### SAP 검토 항목 (총 11개 섹션)

1. **필수 정보**: 제목, 버전, 통계담당자
2. **연구 목적 및 가설**: 목적, 통계적 가설
3. **평가변수**: 주요/부차 평가변수 정의
4. **표본 크기**: 산출근거, 검정력, 효과크기
5. **분석 대상군**: ITT, PP, 안전성 분석군
6. **통계 방법**: 통계검정, 신뢰구간, 다중비교
7. **결측치 처리**: 결측치 처리 방법
8. **중간분석**: 중간분석, 조기중단 규칙
9. **하위그룹 분석**: 하위그룹, 층화요인
10. **안전성 분석**: 이상반응 분석, 코딩사전
11. **통계 소프트웨어**: 사용 소프트웨어, 표/그림 목록

## 📁 프로젝트 구조

```
clinical-document-review/
├── cli.py                      # CLI 메인 진입점
├── requirements.txt            # Python 의존성
├── README.md                   # 본 문서
├── config/                     # 검토 체크리스트 설정
│   ├── protocol_checklist.yaml
│   ├── ib_checklist.yaml
│   └── sap_checklist.yaml
├── src/
│   ├── parsers/               # 문서 파싱 모듈
│   │   ├── base_parser.py
│   │   └── pdf_parser.py
│   ├── reviewers/             # 문서 검토 모듈
│   │   ├── base_reviewer.py
│   │   ├── protocol_reviewer.py
│   │   ├── ib_reviewer.py
│   │   └── sap_reviewer.py
│   ├── reports/               # 보고서 생성 모듈
│   │   ├── html_report.py
│   │   └── text_report.py
│   └── llm/                   # 로컬 LLM 통합 (선택사항)
│       └── ollama_client.py
└── reports/                   # 생성된 보고서 저장 (자동 생성)
```

## 🤖 로컬 LLM 통합 (선택사항)

더 고급 분석을 원한다면 [Ollama](https://ollama.ai)를 사용하여 로컬 LLM을 통합할 수 있습니다.

### Ollama 설치 및 설정

```bash
# 1. Ollama 설치 (https://ollama.ai)

# 2. 모델 다운로드
ollama pull llama2

# 3. Ollama 실행 확인
ollama list
```

### LLM 기능 사용 (개발 중)

```python
from src.llm import OllamaClient

client = OllamaClient(model="llama2")

# LLM이 실행 중인지 확인
if client.is_available():
    # 문서 요약
    summary = client.summarize_document(document_text)

    # 섹션 분석
    analysis = client.analyze_section(section_text, "Study Objectives", "Protocol")
```

**참고:** LLM 통합은 선택사항이며, 기본 검토 기능은 LLM 없이도 완전히 작동합니다.

## 🔧 커스터마이징

### 검토 체크리스트 수정

`config/` 폴더의 YAML 파일을 수정하여 검토 항목을 커스터마이징할 수 있습니다.

```yaml
# config/protocol_checklist.yaml 예시
sections:
  custom_section:
    name: "사용자 정의 섹션"
    checks:
      - id: "custom_001"
        category: "커스텀"
        description: "확인하고 싶은 항목"
        keywords: ["키워드1", "키워드2"]
        severity: "critical"  # critical, major, minor
```

### 새로운 문서 타입 추가

1. `config/`에 새 체크리스트 YAML 파일 생성
2. `src/reviewers/`에 새 리뷰어 클래스 생성
3. `cli.py`의 `REVIEWERS` 딕셔너리에 추가

## 📈 보고서 예시

### HTML 보고서

생성된 HTML 보고서에는 다음이 포함됩니다:

- 📊 검토 요약 및 통과율
- 🎯 중요도별 이슈 (Critical/Major/Minor)
- 📋 섹션별 상세 검토 결과
- 🔍 발견/누락 키워드
- 💡 개선 권장사항

브라우저에서 보고서를 열어 확인:

```bash
# 보고서 생성 후
firefox reports/protocol_report.html
# 또는
chrome reports/protocol_report.html
```

### 텍스트 보고서

텍스트 보고서는 터미널에서 바로 확인하거나 이메일로 공유하기 좋습니다:

```bash
cat reports/protocol_report.txt
```

## 🔐 보안 고려사항

1. **완전 로컬 처리**: 모든 문서 처리가 로컬에서 이루어집니다
2. **외부 전송 없음**: 네트워크 연결 불필요 (LLM 기능 제외)
3. **데이터 보존**: 원본 문서는 수정되지 않습니다
4. **보고서 저장**: 생성된 보고서는 로컬 `reports/` 폴더에만 저장됩니다

### .gitignore 설정

민감한 문서가 실수로 Git에 커밋되지 않도록 `.gitignore`에 포함되어 있습니다:

```
*.pdf
*.docx
test_documents/
reports/
```

## ⚠️ 제한사항

1. **문서 형식**: 현재 PDF만 지원 (DOCX 지원 예정)
2. **언어**: 영어 및 한글 키워드 기반 검색
3. **자동화 한계**: 규칙 기반 검토이므로 전문가의 최종 검토 필요
4. **OCR 미지원**: 스캔된 이미지 PDF는 지원하지 않음 (텍스트 추출 가능한 PDF만)

## 🤝 기여 방법

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 라이선스

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋 FAQ

**Q: 스캔된 PDF도 검토할 수 있나요?**
A: 아니요, 현재는 텍스트가 추출 가능한 PDF만 지원합니다. OCR 기능은 향후 추가 예정입니다.

**Q: 인터넷 연결이 필요한가요?**
A: 기본 검토 기능은 인터넷 연결이 필요 없습니다. Ollama LLM 기능을 사용하려면 로컬에서 Ollama가 실행 중이어야 합니다.

**Q: 검토 결과가 100% 정확한가요?**
A: 이 도구는 보조 도구이며, 키워드 기반 자동 검토를 수행합니다. 최종 검토 및 승인은 반드시 담당 전문가가 수행해야 합니다.

**Q: DOCX 파일도 지원하나요?**
A: 현재는 PDF만 지원하며, DOCX 지원은 향후 버전에서 추가 예정입니다.

**Q: 체크리스트를 수정할 수 있나요?**
A: 네, `config/` 폴더의 YAML 파일을 수정하여 기관별 요구사항에 맞게 커스터마이징할 수 있습니다.

## 📧 문의

이슈가 있거나 기능 요청이 있으시면 GitHub Issues를 통해 알려주세요.

---

**면책조항**: 이 도구는 임상문서 검토를 보조하는 도구입니다. 규제 제출용 문서의 최종 검토 및 승인은 반드시 자격을 갖춘 전문가가 수행해야 합니다.
