# DeepResearch 기반 제품 추천 서비스 확장 PRD

> 버전: 0.1 (2025-07-01)
> 작성자: 팀 LangGraph ✕ DeepResearch

## 1. 배경
- 현 플랫폼은 "웹 검색 → 간략 추천 리스트" 수준으로도 30 개 테스트 중 29 개 합격(≈97%) 성능을 달성했음.
- 그러나 고가·전문화 카테고리(예: 워크스테이션 노트북, 영상장비)와 주기적 가격 변동 영역에서 **심층 분석·신뢰도·트렌드 반영** 요구가 증가.
- `deepresearch/` 워크플로우는 Plan → Review → Execute 루프, LLM Self-Grader, 사용자 피드백 인터럽트 등 **품질 보증 기제**를 이미 제공. 이를 제품 추천 도메인에 맞게 확장한다.

## 2. 목표 (OKR)
| Objective | Key Result |
|-----------|------------|
| O1 : 추천 리포트 신뢰도 향상 | • Human eval "근거 신뢰도" 점수 4.0 → 4.7 /5<br/>• 인용 링크 클릭율 15 % 이상 |
| O2 : 사용자 참여 증대 | • Follow-up Q&A 사용률 > 40 %<br/>• 개인화 가중치 슬라이더 조정 후 재정렬 경험률 > 50 % |
| O3 : 콘텐츠 신선도 유지 | • 자동 트렌드 업데이트 주기 1 주 이내

## 3. 핵심 기능 아이디어
| # | 기능 | 상세 설명 | 예상 효과 |
|---|--------|-----------|------------|
| 1 | **Deep Insight Report** | 문제 정의→고려 요소→후보 비교→최종 추천+TL;DR. DeepResearch가 스펙 분석·가격 추적·리뷰 요약을 병렬 수행 후 Self-Grader로 검수. | 고가/전문화 카테고리 차별화, 체류 시간 ↑ |
| 2 | **Plan ↔ Feedback 루프** | 리포트 초안 후 `human_feedback` 노드로 즉시 피드백 받고 요구사항 확정 시까지 반복. | 맞춤형 정확도·사용자 참여 ↑ |
| 3 | **Section Self-Grader** | 각 제품 설명 후 LLM Grader가 근거·객관성·출처 정합성을 평가, fail → 자동 보강. | 정보 오류·출처 누락 ↓ |
| 4 | **Evidence Explorer** | 추천 카드 옆 "🔍 근거 보기" 클릭 시 웹 캡처·인용 문장·Grader 신뢰 점수를 사이드바로 노출. | 투명성·CTR ↑ |
| 5 | **Trend Pulse** | 스케줄 노드로 주 1 회 가격/신제품 업데이트 → 리포트에 Change-log 배너. | 콘텐츠 신선도 유지, 유지보수 자동화 |
| 6 | **Personal Constraint Optimizer** | 예산·브랜드·무게 등 가중치 슬라이더 → 플래너 prompt 반영해 가치 점수 재계산. | 개인화 경험·전환율 ↑ |
| 7 | **Multi-Agent Battle Test** | 두 후보를 입력하면 spec_analyst / price_tracker / review_summarizer 등 에이전트가 각 측면 비교 → 표·그래프 출력. | 경쟁 제품 비교 시나리오 지원 |
| 8 | **Scenario-Based Bundles** | "신혼집 홈오피스 세트" 입력 시 카테고리별 하위 그래프 병렬 실행 후 패키지 제안. | 객단가 상승, Cross-Sell |
| 9 | **Sustainability Score** | CSR·탄소발자국 데이터 수집 → 친환경 점수 라벨링. | ESG 민감 고객 타깃 |
| 10 | **One-Click Vendor Outreach** | 확정 리스트에 최저가 링크, A/S 정보, 구매 체크리스트 자동 생성·공유. | 구매 전환 보조, UX 개선 |

## 4. 우선순위 / 단계별 도입
1. Evidence Explorer (저비용·고효과)
2. Deep Insight Report + Feedback 루프
3. Trend Pulse 자동 업데이트
4. Personal Constraint Optimizer
5. 나머지 기능은 토큰/비용·SLA를 고려해 롤아웃

## 5. 기술 스택 & 구현 힌트
- **그래프 확장**: `server/app/graph/graph.py`에 DeepDive 노드 추가, `deepresearch/` 플로우를 서브그래프로 임포트.
- **출처 저장**: 검색 결과를 Postgres + pgvector에 embedding & metadata 형태로 저장, `source_id` FK로 메시지 카드와 연결.
- **Self-Grader 프롬프트**: `state["messages"]` 윈도우 512 토큰 유지(`trim_messages`).
- **프런트**: React에 Evidence Drawer 컴포넌트, Badge UI (`src/components/ui/badge.tsx`) 재사용.

## 6. 리스크 & 완화
| 리스크 | 대응 |
|---------|------|
| 토큰 비용 폭증 | • 슬라이딩 윈도우 + 요약 전략<br/>• Section 최대 반복 횟수 제한 |
| 응답 지연 | • 하위 그래프 병렬 실행(`graph.parallel`)<br/>• 캐싱 로직 도입 |
| 근거 신뢰도 편차 | • 다중 검색 엔진 투표(Tavily, DDG, Bing) 사용<br/>• Grader threshold 조정 |

---
> **다음 단계**: Evidence Explorer POC → 내부 QA → A/B 테스트 지표 검증 후 단계적 롤아웃.
