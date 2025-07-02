# 멀티 에이전트 활용
- 제품을 추천해줘, 제품 리뷰를 분석해줘, 최저가 제품을 찾아줘, 유사한 제품을 찾아줘 등등
- 사용자 요청에 따라 기대하는 결과 리포트가 다르다.
- 이걸 각각 에이전트로 구현하여 멀티에이전트를 형성해야 한다.
- 브라우저 MCP, playwright
- ReAct 에이전트 활용
- 멀티 에이전트 -> 추천 + 리뷰, 두개가 서로 연동이 되는지 테스트한다.

## 멀티-에이전트 고도화 설계

### 1. 문제 정의
- 사용자는 "제품을 추천해줘 / 리뷰를 분석해줘 / 최저가를 찾아줘 / 유사 제품을 찾아줘" 등 서로 다른 결과물을 요청
- 하나의 거대 에이전트보다는 작업 단위를 분리한 여러 서브-에이전트가 협력하는 편이 안정적이며 유지보수 용이

### 2. 에이전트 군 및 역할
1) **Planner / Orchestrator**  
   - 사용자 의도를 파싱하여 Task를 분해하고 수행 순서(병렬/직렬)를 결정  
   - LangGraph Router 노드 + 공유 `state`에 `task_list` 기록  
2) **Product Recommender**  
   - 키워드·사용자 조건으로 후보 제품을 탐색 (웹 검색 + 벡터 DB 유사도)  
   - ReAct 패턴: *Search → Parse → Reason*  
3) **Review Analyst**  
   - 크롤링된 리뷰를 요약하고 장·단점, 평점 분포를 산출  
   - Playwright 브라우저 자동화 + LLM 요약  
4) **Price Hunter**  
   - 다중 쇼핑몰 실시간 스크래핑 → 최저가, 가격 추세 그래프 제공  
5) **Similar Product Finder**  
   - 임베딩 벡터 검색을 통해 유사 제품 Top-k 반환  
6) **Critic / QA Agent (옵션)**  
   - 중간 산출물을 검증하고 품질 피드백 제공  

### 3. 데이터 & 상태 흐름 (LangGraph)
- **State** = `{ user_query, task_list, shared_context, partial_results, final_report }`
- Planner → `task_list` 추가 → 병렬/직렬 에이전트 실행  
- 각 에이전트 결과를 `partial_results`에 누적  
- 모든 필수 Task 완료 시 Summarizer가 `final_report` 생성 → Critic 검수 후 반환  

### 4. 통신 & 동기화 전략
- 공유 State 객체에서 키 단위 Lock 으로 Race Condition 방지  
- 에이전트 간 직접 메시지는 최소화하고 State Update 이벤트로 동기화  

### 5. Reason-and-Act 루프
- 각 에이전트: `Thought → Action → Observation` 최대 N회 반복  
- Action 예시: `web_search`, `browse_site(url)`, `run_python(code)`, `lookup_vector(query)`  

### 6. 브라우저 자동화 (MCP / Playwright)
- Tool 세트: `open_page`, `click`, `get_text`, `screenshot`  
- Review Analyst, Price Hunter가 주로 사용  
- MCP(Memory-Context-Propagation) 기법으로 중복 탐색 최소화  

### 7. 평가 및 피드백
- `tests/evals` 모듈 활용하여 정확성·완성도 자동 스코어링  
- Critic Agent가 낮은 점수 산출물에 대해 수정 프롬프트 생성 → 재실행 또는 Human-in-the-loop  

### 8. 동시성 & 자원 관리
- CPU-bound(LLM) vs IO-bound(크롤링) 분리 → `asyncio.TaskGroup` 활용  
- Rate-limit, 토큰 한도, 동시 요청 수를 공통 Config에서 관리  

### 9. 단계별 구현 로드맵
1. `server/app/graph`에 Planner + Product Recommender, Review Analyst 우선 구현  
2. Price Hunter, Similar Finder 추가 및 Planner 스케줄 알고리즘 개선  
3. Critic Agent로 Self-healing 루프 적용  
4. Playwright 기반 브라우저 Tool 완성 후 Prompt 튜닝  
5. E2E 벤치마크 & 테스트 작성 (`tests/evals`)  
6. 캐싱·모니터링·분산 실행(워크큐) 확장  

### 10. 기술 스택 매핑
| 영역 | 기술 |
| --- | --- |
| Orchestration | LangGraph + Pydantic State |
| LLM | OpenAI / Gemini (Function Calling) |
| Vector DB | Chroma / PGVector |
| Browser | Playwright (Headless) |
| Metrics & Logging | LangSmith, Prometheus, Grafana |
