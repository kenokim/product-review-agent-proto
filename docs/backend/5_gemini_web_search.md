# LangGraph 2025 현재 Gemini 웹 검색 가이드

## 개요

2025년 현재 Google Gemini API는 **Grounding with Google Search** 기능을 통해 실시간 웹 검색을 지원합니다. 이 기능을 LangGraph와 결합하면 강력한 웹 검색 기반 AI 에이전트를 구축할 수 있습니다.

## 1. 최신 Gemini API 웹 검색 방법

### 1.1 새로운 Google GenAI SDK 사용

2025년 현재 권장되는 방법은 새로운 `google.genai` 패키지를 사용하는 것입니다:

```python
from google import genai
from google.genai import types

# 클라이언트 구성
client = genai.Client()

# 웹 검색 도구 정의
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

# 생성 설정
config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

# 요청 실행
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="2024년 유럽축구선수권대회 우승팀은?",
    config=config,
)

print(response.text)
```

### 1.2 기존 google-generativeai 라이브러리 사용

기존 라이브러리를 사용하는 경우:

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

# 모델 생성
model = genai.GenerativeModel('gemini-2.5-flash')

# 웹 검색 도구 설정
tools = [{"google_search": {}}]

response = model.generate_content(
    "최신 AI 트렌드에 대해 알려줘",
    tools=tools,
    tool_config={'function_calling_config': 'AUTO'}
)

print(response.text)
```

## 2. LangGraph와 Gemini 웹 검색 통합

### 2.1 LangGraph 노드 구현

```python
from google import genai
from google.genai import types
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List

class WebSearchState(TypedDict):
    query: str
    search_results: List[str]
    final_answer: str

def web_search_node(state: WebSearchState) -> WebSearchState:
    """웹 검색 노드"""
    client = genai.Client()
    
    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )
    
    config = types.GenerateContentConfig(
        tools=[grounding_tool],
        temperature=0
    )
    
    # 검색 쿼리 생성 및 실행
    search_prompt = f"""
    다음 질문에 대해 웹 검색을 수행하고 정확한 정보를 제공해주세요:
    {state['query']}
    
    검색 결과를 바탕으로 신뢰할 수 있는 답변을 작성해주세요.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=search_prompt,
        config=config
    )
    
    # 검색 결과 메타데이터 추출
    search_results = []
    if hasattr(response, 'candidates') and response.candidates:
        candidate = response.candidates[0]
        if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
            for chunk in candidate.grounding_metadata.grounding_chunks:
                if hasattr(chunk, 'web'):
                    search_results.append(f"{chunk.web.title}: {chunk.web.uri}")
    
    return {
        "query": state["query"],
        "search_results": search_results,
        "final_answer": response.text
    }

# 그래프 구성
workflow = StateGraph(WebSearchState)
workflow.add_node("web_search", web_search_node)
workflow.add_edge(START, "web_search")
workflow.add_edge("web_search", END)

app = workflow.compile()
```

### 2.2 병렬 웹 검색 구현

```python
from langgraph.graph import Send
from typing import List

def generate_search_queries(state) -> List[str]:
    """검색 쿼리 생성"""
    client = genai.Client()
    
    query_prompt = f"""
    다음 주제에 대해 포괄적인 정보를 얻기 위한 3-5개의 검색 쿼리를 생성해주세요:
    주제: {state['topic']}
    
    각 쿼리는 서로 다른 관점이나 측면을 다루어야 합니다.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query_prompt
    )
    
    # 쿼리 리스트 파싱 (실제 구현에서는 structured output 사용)
    queries = response.text.split('\n')
    return [q.strip('- ').strip() for q in queries if q.strip()]

def continue_to_web_research(state):
    """병렬 웹 검색 시작"""
    queries = generate_search_queries(state)
    return [
        Send("web_research", {"search_query": query, "id": idx})
        for idx, query in enumerate(queries)
    ]

def web_research(state) -> dict:
    """개별 웹 검색 수행"""
    client = genai.Client()
    
    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )
    
    config = types.GenerateContentConfig(
        tools=[grounding_tool],
        temperature=0
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"다음에 대해 자세히 검색해주세요: {state['search_query']}",
        config=config
    )
    
    return {
        "search_results": [response.text],
        "sources": extract_sources(response)
    }

def extract_sources(response):
    """응답에서 출처 정보 추출"""
    sources = []
    if hasattr(response, 'candidates') and response.candidates:
        candidate = response.candidates[0]
        if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
            for chunk in candidate.grounding_metadata.grounding_chunks:
                if hasattr(chunk, 'web'):
                    sources.append({
                        "title": chunk.web.title,
                        "url": chunk.web.uri,
                        "domain": getattr(chunk.web, 'domain', '')
                    })
    return sources
```

## 3. 고급 기능 구현

### 3.1 Reflection 기반 반복 검색

```python
def reflection_node(state) -> dict:
    """검색 결과 평가 및 추가 검색 필요성 판단"""
    client = genai.Client()
    
    reflection_prompt = f"""
    다음 검색 결과들을 분석하여 사용자 질문에 충분히 답변할 수 있는지 평가해주세요:
    
    원래 질문: {state['original_query']}
    검색 결과들: {state['search_results']}
    
    평가 기준:
    1. 정보의 완전성
    2. 신뢰성
    3. 최신성
    4. 관련성
    
    JSON 형식으로 응답해주세요:
    {{
        "is_sufficient": true/false,
        "missing_aspects": ["부족한 정보 1", "부족한 정보 2"],
        "additional_queries": ["추가 검색어 1", "추가 검색어 2"]
    }}
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=reflection_prompt
    )
    
    # JSON 파싱 (실제로는 structured output 사용 권장)
    import json
    try:
        result = json.loads(response.text)
        return {
            "is_sufficient": result.get("is_sufficient", False),
            "additional_queries": result.get("additional_queries", []),
            "reflection_count": state.get("reflection_count", 0) + 1
        }
    except:
        return {
            "is_sufficient": True,
            "additional_queries": [],
            "reflection_count": state.get("reflection_count", 0) + 1
        }

def should_continue_search(state) -> str:
    """검색 계속 여부 결정"""
    max_iterations = 3
    
    if (state.get("is_sufficient", True) or 
        state.get("reflection_count", 0) >= max_iterations):
        return "finalize_answer"
    else:
        return "additional_search"
```

### 3.2 출처 추적 및 인용

```python
def add_citations(response_text: str, sources: List[dict]) -> str:
    """응답에 인용 추가"""
    if not sources:
        return response_text
    
    # 인용 번호 추가
    cited_text = response_text
    for i, source in enumerate(sources, 1):
        citation = f"[{i}]({source['url']})"
        # 간단한 인용 추가 로직 (실제로는 더 정교한 구현 필요)
        cited_text += f"\n\n출처 {i}: {source['title']} - {source['url']}"
    
    return cited_text

def finalize_answer(state) -> dict:
    """최종 답변 생성"""
    client = genai.Client()
    
    final_prompt = f"""
    다음 검색 결과들을 종합하여 사용자 질문에 대한 완전하고 정확한 답변을 작성해주세요:
    
    질문: {state['original_query']}
    검색 결과들: {state['all_search_results']}
    
    답변 요구사항:
    1. 정확하고 신뢰할 수 있는 정보 제공
    2. 출처 명시
    3. 구조화된 형태로 작성
    4. 한국어로 작성
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=final_prompt,
        config=types.GenerateContentConfig(temperature=0.1)
    )
    
    # 출처 정보와 함께 최종 답변 반환
    final_answer = add_citations(response.text, state.get('all_sources', []))
    
    return {
        "final_answer": final_answer,
        "sources_used": state.get('all_sources', [])
    }
```

## 4. 실제 사용 예시

### 4.1 완전한 웹 검색 에이전트

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Optional

class ResearchState(TypedDict):
    original_query: str
    search_queries: List[str]
    search_results: List[str]
    all_sources: List[dict]
    is_sufficient: bool
    reflection_count: int
    final_answer: str

def create_web_research_agent():
    """웹 검색 에이전트 생성"""
    
    workflow = StateGraph(ResearchState)
    
    # 노드 추가
    workflow.add_node("generate_queries", generate_search_queries_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("reflection", reflection_node)
    workflow.add_node("finalize", finalize_answer)
    
    # 엣지 추가
    workflow.add_edge(START, "generate_queries")
    workflow.add_edge("generate_queries", "web_search")
    workflow.add_edge("web_search", "reflection")
    
    # 조건부 엣지
    workflow.add_conditional_edges(
        "reflection",
        should_continue_search,
        {
            "additional_search": "web_search",
            "finalize_answer": "finalize"
        }
    )
    
    workflow.add_edge("finalize", END)
    
    return workflow.compile()

# 사용 예시
agent = create_web_research_agent()

result = agent.invoke({
    "original_query": "2024년 AI 기술 동향과 전망",
    "search_queries": [],
    "search_results": [],
    "all_sources": [],
    "is_sufficient": False,
    "reflection_count": 0,
    "final_answer": ""
})

print(result["final_answer"])
```

## 5. 모범 사례 및 주의사항

### 5.1 API 사용 최적화

```python
# 1. 적절한 온도 설정
config = types.GenerateContentConfig(
    tools=[grounding_tool],
    temperature=0,  # 검색에는 낮은 온도 사용
)

# 2. 재시도 로직
import time
from typing import Optional

def safe_api_call(client, model: str, prompt: str, max_retries: int = 3) -> Optional[str]:
    """안전한 API 호출"""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=config
            )
            return response.text
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 지수 백오프
                continue
            else:
                print(f"API 호출 실패: {e}")
                return None
```

### 5.2 비용 최적화

```python
# 1. 쿼리 중복 제거
def deduplicate_queries(queries: List[str]) -> List[str]:
    """중복 쿼리 제거"""
    seen = set()
    unique_queries = []
    for query in queries:
        normalized = query.lower().strip()
        if normalized not in seen:
            seen.add(normalized)
            unique_queries.append(query)
    return unique_queries

# 2. 결과 캐싱
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_web_search(query: str) -> str:
    """캐시된 웹 검색"""
    # 실제 검색 로직
    pass
```

## 6. 지원되는 모델 및 언어

### 6.1 지원 모델 (2025년 현재)
- Gemini 2.5 Pro
- Gemini 2.5 Flash
- Gemini 2.0 Flash
- Gemini 1.5 Pro
- Gemini 1.5 Flash

### 6.2 다국어 지원
Grounding with Google Search는 모든 사용 가능한 언어를 지원하며, 한국어 쿼리와 응답도 완벽하게 처리됩니다.

## 7. 문제 해결

### 7.1 일반적인 오류

```python
# 1. API 키 설정 확인
import os
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다")

# 2. 응답 구조 확인
def safe_extract_text(response):
    """안전한 텍스트 추출"""
    try:
        return response.text
    except AttributeError:
        if hasattr(response, 'candidates') and response.candidates:
            return response.candidates[0].content.parts[0].text
        return "응답을 처리할 수 없습니다"
```

### 7.2 성능 최적화

```python
# 1. 비동기 처리
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def parallel_web_search(queries: List[str]) -> List[str]:
    """병렬 웹 검색"""
    loop = asyncio.get_event_loop()
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        tasks = [
            loop.run_in_executor(executor, web_search_single, query)
            for query in queries
        ]
        results = await asyncio.gather(*tasks)
    
    return results
```

이 가이드는 2025년 현재 최신 Gemini API와 LangGraph를 사용한 웹 검색 구현의 완전한 가이드를 제공합니다. 실제 프로덕션 환경에서는 에러 처리, 로깅, 모니터링 등을 추가로 구현해야 합니다.