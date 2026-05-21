# Deng et al. 2025 — Psychiatric PGHD RWE 1건 역추적

대상 논문: Deng Y-F, Girman CJ, Ritchey ME. "Real-World Evidence in FDA Approvals for Labeling Expansion of Small Molecules and Biologics." *Ther Innov Regul Sci*. 2025. DOI: 10.1007/s43441-025-00816-9 (Springer link / PMC12446098).

## 0. 조사 환경 한계 (먼저 명시)

이 세션의 네트워크 정책상 직접 호출이 차단된 엔드포인트:
- `api.fda.gov/drug/drugsfda.json` (openFDA Drugs@FDA) — WebFetch 403, curl 차단
- `eutils.ncbi.nlm.nih.gov/entrez/eutils/*` (PubMed E-utilities) — 403
- `clinicaltrials.gov` API — 403
- `fda.gov/media/...` (FDA Efficacy Supplement PDF) — 403
- `link.springer.com/article/10.1007/s43441-025-00816-9` (본문) — 403
- `pmc.ncbi.nlm.nih.gov/articles/PMC12446098/` — 403
- `static-content.springer.com/...` (보충자료 PDF/XLSX) — 403
- `web.archive.org` — 차단
- Google/Bing/Semantic Scholar/Europe PMC API — 403

→ Drugs@FDA의 sNDA/sBLA 전수 다운로드는 이 세션에서 불가.
WebSearch(허용)와 공개 보도자료, 학회/제약사 사이트로부터 추론한 결과를 보고합니다.
약물 enumeration은 **완전성이 보장되지 않습니다** — 보수적으로 "주요 후보군"만 다룹니다.

---

## 1. Deng et al. 2025 핵심 (검색 결과 발췌로 확정)

검색 결과로 직접 인용 가능한 본문 fragment:

- "Among 218 labeling expansions granted, RWE was found in FDA documents for 3 approvals and elsewhere for 52 approvals."
- "Proportion of approvals with RWE was 23.3% in 2022, 27.7% in 2023, and 23.7% in 2024."
- "RWE was most commonly found in submissions for oncology (43.6%), infection (9.1%), and dermatology (7.3%)."
- "Among the 88 RWE studies, EHR (75%) was the most frequently used data source, followed by combinations of EHR and PGHD (5.7%) and registry data (4.6%)."
- **"Across therapeutic areas, data source preferences varied, with combinations of EHR and PGHD used in allergy, PGHD in psychiatry, registry data in pulmonary, and claims data in rheumatology."**
- PGHD 정의: "adverse events, questionnaires, indices based on patient-reported information, and data collected by devices such as Fitbits, smartwatches, smartphones or tablets."

→ 정신과 영역에서 RWE 데이터원으로 **PGHD**가 가장 흔하게 사용됨이 확정.
오뮬렉(oncology) 등 다른 영역 대비 정신과 RWE 사건 수 자체는 매우 적음(전체 88건 중 PGHD-only는 약 4건, 그 중 정신과는 1건 수준으로 추정 — 사용자가 명시한 "1건"과 일치).

---

## 2. 2022-01-01 ~ 2024-05-31 정신과 sNDA/sBLA label expansion 후보 (소아 단독 제외)

openFDA 직접 enumeration 불가 → 공개 보도/언론 종합으로 다음 후보 식별:

| # | Brand (generic) | App # | Sponsor | 승인일 | 확장 내용 | 분류 |
|---|---|---|---|---|---|---|
| 1 | **Qelbree (viloxazine ER)** | NDA 211964 / S-003 | Supernus | **2022-04-29** | adult ADHD 추가 (피어→성인 확대; 소아 단독 아님) | 성인 모집단 확대 |
| 2 | **Vraylar (cariprazine)** | NDA 204370 / S-024(추정) | AbbVie | **2022-12-16** | MDD adjunctive 추가 (신규 적응증) | 신규 적응증 |
| 3 | **Rexulti (brexpiprazole)** | NDA 205422 / S-009 | Otsuka/Lundbeck | **2023-05-10** | Agitation associated with Alzheimer's dementia (AAD) 추가 | 신규 적응증 |
| 4 | **Sublocade (buprenorphine ER)** | NDA 209819 / S-024 | Indivior | 2023-05 | OUD 라벨 변경 (rapid initiation은 후속) | (SUD; 정신과 분류 시) |
| 5 | **Ingrezza (valbenazine)** | NDA 209241 / S-008 | Neurocrine | **2023-08-18** | Chorea in Huntington's disease | 신경/정신과 borderline |
| 6 | **Fanapt (iloperidone)** | NDA 022192 / S-007(추정) | Vanda | **2024-04-02** | Bipolar I mania/mixed 추가 | 신규 적응증 |

소아 단독 추가는 명시 제외:
- Wakix (pitolisant) pediatric narcolepsy 2023-10 — 제외
- Latuda pediatric MDD 2022-10 — 소아 단독 → 제외
- Daytrana 청소년 ADHD — 기존 소아 적응증 연장
- Onyda XR clonidine 2024-04-23 — 신규 NDA(보충 아님)

제외/범위 밖:
- Caplyta 양극성 우울증 2021-12-17(범위 직전), Caplyta MDD adjunct 2025-11(범위 후)
- Spravato monotherapy TRD 2025-01(범위 후); 2022-2024년 사이 공식 라벨 확장 없음
- Auvelity 2022-08-19 — 신규 NDA(보충 아님)
- Quviviq 2022-01, Adlarity 2022-03 — 신규 NDA

---

## 3. 각 후보의 RWE/observational 연구 — 승인일 이전 발표/등록분

PubMed eutils 직접 조회 불가 → WebSearch로 확인 가능한 범위.

### 3-1. Qelbree (viloxazine ER) — adult ADHD, 2022-04-29
- 승인 근거: **P304 (SPN-812-303)** Phase 3 RCT (성인, AISRS primary). RWE 없음.
- 승인 이전 publication에서 PGHD/wearable로 시행된 observational 연구는 확인되지 않음.
- 분류: **unknown / 없음**. PGHD 사용 흔적 약함.

### 3-2. Vraylar (cariprazine) — MDD adjunctive, 2022-12-16
- 승인 근거: **Study 3111-301-001 (NCT03738215)** + Phase 2 보조. MADRS 중심.
- 승인 이후(2024-2025) 발표된 cariprazine MDD adjunctive RWE:
  - PMID 39945353 — *Healthcare resource utilization with adjunctive cariprazine* (MarketScan 청구, 2018-2021) → **claims**
  - PMID 40445745 — *Real-world effectiveness of cariprazine in MDD and bipolar I disorder in US* (Komodo Health claims + EHR + **PHQ-9 PRO** ML-추출, n=396) → **EHR + PGHD(PRO)**
  - PMID 40904619 — *Real-World Disability Outcomes ... cariprazine vs other AAP for MDD adjunctive* → claims
- Deng의 검색 시점(2025 상반기) 기준으로 PMID 40445745 (Komodo + PHQ-9)이 PubMed에 인덱싱되어 있을 가능성 높음.
- 분류: **EHR + PGHD(PHQ-9 self-report ePRO)**

### 3-3. Rexulti (brexpiprazole) — AAD, 2023-05-10
- 승인 근거: **Study 331-12-283**, **331-14-213** 두 Phase 3 RCT, **CMAI total score**(요양자 인터뷰) primary.
- 승인 이전 RWE 거의 없음. post hoc 분석은 RCT 데이터 풀링.
- CMAI는 caregiver-interview 기반 — 엄밀히는 "구조화된 임상 평가도구"이지 PGHD(환자 본인의 디바이스/앱/직접 응답)와 다소 거리. 다만 Deng 정의("questionnaires, indices based on patient-reported information")에는 caregiver-reported도 포함될 여지가 있음.
- 분류: **unknown** (RWE 미식별; CMAI가 PGHD로 분류된다면 보더라인)

### 3-4. Sublocade (buprenorphine ER) — 2023-05 sNDA S-024
- S-024는 라벨 변경(REMS 등) 위주. 동일 윈도우 내 라벨 확장으로 보기 어려움.
- Indivior가 발표한 RWE는 **Canada chart review** (retrospective EHR/chart). PGHD 아님.
- 분류: **EHR/claims (chart review)**

### 3-5. Ingrezza (valbenazine) — HD chorea, 2023-08-18
- 승인 근거: **KINECT-HD Phase 3 RCT (NCT04102579)** + KINECT-HD2 open-label.
- KINECT-HD에 **wearable movement sensor substudy** 포함됨 (Phase 3 첫 사례) — 단, 이는 RCT 내부 substudy로, "real-world observational" 정의에 부합하지 않을 수 있음.
- HD는 통상 neurology로 분류 (Deng 분류는 불명).
- 분류: **wearable PGHD (RCT 내 substudy)** — 정신과로 분류된다면 PGHD 후보.

### 3-6. Fanapt (iloperidone) — bipolar I mania, 2024-04-02
- 승인 근거: **Phase 3 RCT (4-week, manic/mixed episodes)** + 기존 schizophrenia 안전성.
- 승인 이전 발표된 iloperidone+bipolar 관련 PGHD observational 연구는 확인 안 됨.
- (별개로 BDmon 등 bipolar smartphone PGHD 연구는 약물 비특이적)
- 분류: **unknown / 없음**

---

## 4. 데이터원 분류 종합

| # | 약물 | 승인일 | RWE 식별? | 분류 | 주된 데이터원 |
|---|---|---|---|---|---|
| 1 | Qelbree | 2022-04-29 | 없음 | unknown | — |
| 2 | **Vraylar (cariprazine)** | 2022-12-16 | **있음** (post-approval, Deng 검색 윈도우 내) | **PGHD + EHR** | **PHQ-9 self-report** + Komodo EHR/claims |
| 3 | Rexulti | 2023-05-10 | 없음 (RCT 위주) | unknown | (caregiver CMAI = borderline) |
| 4 | Sublocade | 2023-05 | 있음 | EHR/claims | Canadian chart review |
| 5 | Ingrezza | 2023-08-18 | RCT-내 substudy | wearable (그러나 RCT) | wrist accelerometer (KINECT-HD substudy) |
| 6 | Fanapt | 2024-04-02 | 없음 | unknown | — |

---

## 5. PGHD 정신과 expansion 후보 — 분류 근거(abstract/보도 인용)

### A. Vraylar (cariprazine) MDD adjunctive (2022-12-16) — **최우선 후보**

근거 인용:
- *Real-world effectiveness of cariprazine in MDD and bipolar I disorder in the United States* (J Med Econ, 2025; PMID 40445745):
  > "depression severity was assessed using **PHQ-9 total scores that were observed or estimated from clinical notes** using a previously validated machine learning algorithm ... mean reductions in PHQ-9 scores from baseline to 2, 6, and 12 months of adjunctive cariprazine treatment were 3.5 (n=127), 4.1 (n=87), and 3.7 (n=52)."
  - 데이터원: Komodo Health Map closed claims + linked EHR + PHQ-9 self-report 추출.
  - PHQ-9는 Deng PGHD 정의의 "questionnaires / indices based on patient-reported information"에 정면 부합.
- 두 번째 후보 study (PMID 39945353): MarketScan claims만 사용. PGHD 아님.

### B. Rexulti (brexpiprazole) AAD (2023-05-10) — 차순위 가능성

근거 인용:
- *Otsuka and Lundbeck Announce U.S. FDA Approval of sNDA for REXULTI* (Otsuka 2023-05-11):
  > "two Phase 3, 12-week, randomized, double-blind, placebo-controlled fixed-dose studies that evaluated ... agitation symptoms in patients with dementia due to Alzheimer's disease based on the **Cohen-Mansfield Agitation Inventory (CMAI) total score**."
  > "CMAI is administered through an **interview with the caregiver**..."
- CMAI를 PGHD(보호자 보고)로 분류한다면 후보, 그러나 통상 PGHD는 환자 본인 또는 본인 디바이스 데이터를 의미. 보더라인.

### C. Ingrezza (valbenazine) HD chorea (2023-08-18) — 정신과로 분류 시 후보

근거 인용:
- *Neurocrine Biosciences Presents INGREZZA Capsules Interim Data ... HSG 2023*:
  > "KINECT-HD, which was the **first Phase 3 clinical trial to include a wearable movement sensor substudy**. Significant improvements in truncal chorea and gait asymmetry measures were seen from baseline to maintenance following the Week 10 visit in the INGREZZA-treated group compared to placebo."
- 단점: HD는 보통 neurology 분류; substudy는 RCT 내부로 RWE 정의와 불일치.

### D. Sublocade S-024 (2023-05), Qelbree adult (2022-04), Fanapt mania (2024-04) — **PGHD 흔적 없음 → unknown**

---

## 6. Deng의 정신과 PGHD 1건은 어느 것일까 — 최종 추론

**가장 가능성 높은 1건: Vraylar (cariprazine) — MDD adjunctive, 2022-12-16 승인.**

근거:
1. **정신과(MDD adjunctive)로 명확히 분류** — Ingrezza(neurology)와 달리 모호함 없음.
2. **PGHD에 부합하는 RWE 데이터원**: PHQ-9 self-report PRO를 Komodo EHR/claims에 매핑한 cohort study가 Deng의 문헌 검색 윈도우(~2025 상반기) 안에 PubMed 인덱싱.
3. Deng paper에서 "EHR + PGHD"(5.7%) 카테고리가 따로 명시되어 있으며, 정신과 항목이 이 패턴에 정합 — Vraylar RW study가 정확히 EHR+PHQ-9의 결합 형태.
4. Deng의 방법론: "searched ClinicalTrials.gov and PubMed to identify RWE not included in FDA approval documents but potentially incorporated by sponsors" — Vraylar의 PHQ-9 기반 RW 분석은 정확히 이런 "FDA 문서 외부, 후원자 incorporable" 유형.

차순위 후보 (분류 정의 차이에 따라 가능):
- **Rexulti (brexpiprazole) for AAD** — CMAI(caregiver-reported)를 PGHD 정의에 포함시킬 경우.
- **Ingrezza (valbenazine) for HD chorea** — Deng이 HD를 정신과 분류했고 KINECT-HD wearable substudy를 RWE로 카운트했을 경우.

**확정 불가능 사유**: Deng 본문/보충자료(Table 1-2, 약물별 list) 직접 열람이 환경 제약으로 불가.
Deng et al. 2025 supplementary table 1·2를 사용자 측에서 열람할 수 있다면, "Therapeutic area = Psychiatry, Data source = PGHD" 행 하나가 위 셋 중 어떤 약물인지 확정될 것.

---

## 7. 후속 검증 방법 (사용자가 직접 할 수 있는 단계)

1. Springer 본문 https://link.springer.com/article/10.1007/s43441-025-00816-9 에서 **Table 2 (RWE characteristics by therapeutic area)** 및 **Supplementary Material**(Table S1: drug-by-drug list)을 확인.
2. PubMed에서 `cariprazine[Title/Abstract] AND ("real-world"[All] OR observational[All]) AND PHQ-9[All]` 검색 → publication 시점이 Deng paper 제출(2024 후반-2025 초) 이전인지 확인.
3. Drugs@FDA의 NDA 204370/S-024 (Vraylar MDD adjunctive) 및 NDA 205422/S-009 (Rexulti AAD) review documents를 검색해 "Real-World Data" 섹션 유무 확인.
4. ClinicalTrials.gov에서 cariprazine NCT 검색 → observational study with PHQ-9 PRO collection (digital ePRO 모듈) 등록 여부 확인.
