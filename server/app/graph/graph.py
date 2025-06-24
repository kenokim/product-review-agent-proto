import os
from dotenv import load_dotenv

# LangGraph 관련
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage

# LLM 관련
from langchain_google_genai import ChatGoogleGenerativeAI
from google import genai as google_genai
from google.genai import types

# 로컬 모듈 import
from .prompts import (
    get_validation_prompt,
    get_search_query_prompt,
    get_web_search_prompt,
    get_reflection_prompt,
    get_answer_prompt
)
from .state import (
    ProductRecommendationState,
    get_latest_user_message
)
from .config import ProductRecommendationConfig
from .tools_and_schemas import (
    ValidationResult,
    SearchQueryResult,
    ReflectionResult
)

load_dotenv()

if os.getenv("GEMINI_API_KEY") is None:
    raise ValueError("GEMINI_API_KEY is not set")

# ========== 노드 구현 ==========

# 1. 검증 노드
def validate_request(state: ProductRecommendationState, config: RunnableConfig) -> dict:
    """사용자 요청의 구체성을 검증하고 필요시 구체화 질문을 생성합니다."""
    
    configurable = ProductRecommendationConfig.from_runnable_config(config)
    
    # LLM 초기화
    llm = ChatGoogleGenerativeAI(
        model=configurable.validation_model,
        temperature=0.1,
        max_retries=5,  # 재시도 횟수 증가
        retry_delay=2,  # 재시도 간격 추가
        api_key=os.getenv("GEMINI_API_KEY")
    )
    
    # 구조화된 출력을 위한 스키마 적용
    structured_llm = llm.with_structured_output(ValidationResult)
    
    # 사용자 요청 추출
    user_message = get_latest_user_message(state["messages"])
    
    # 프롬프트 구성
    validation_prompt = get_validation_prompt(user_message)
    
    # LLM 호출
    result = structured_llm.invoke(validation_prompt)
    
    return {
        "is_request_specific": result.is_specific,
        "response_to_user": result.clarification_question if not result.is_specific else "",
        "user_intent": result.extracted_requirements.get("intent", "")
    }


# 2. 검색어 생성 노드
def generate_search_queries(state: ProductRecommendationState, config: RunnableConfig) -> dict:
    """구체화된 요청을 바탕으로 효과적인 검색어들을 생성합니다."""
    
    configurable = ProductRecommendationConfig.from_runnable_config(config)
    
    llm = ChatGoogleGenerativeAI(
        model=configurable.search_model,
        temperature=0.7,
        max_retries=2,
        api_key=os.getenv("GEMINI_API_KEY")
    )
    
    structured_llm = llm.with_structured_output(SearchQueryResult)
    
    user_intent = state.get("user_intent", "")
    user_message = get_latest_user_message(state["messages"])
    
    search_prompt = get_search_query_prompt(user_message, user_intent, configurable.max_search_queries)
    result = structured_llm.invoke(search_prompt)
    
    return {"search_queries": result.queries}


def continue_to_web_search(state: ProductRecommendationState):
    """LangGraph의 Send 이벤트를 사용한 동적 병렬 검색"""
    return [
        Send("web_search", {"search_query": query, "id": int(idx)})
        for idx, query in enumerate(state["search_queries"])
    ]


# 3. 웹 검색 노드
def web_search(state: dict, config: RunnableConfig) -> dict:
    """Gemini API의 Google Search 기능을 사용하여 웹 검색을 수행하고 제품 후보를 추출합니다."""
    
    from .utils import resolve_urls, get_citations, insert_citation_markers
    
    configurable = ProductRecommendationConfig.from_runnable_config(config)
    
    # 단일 검색어 처리 (병렬 처리용)
    query = state["search_query"]
    search_id = state["id"]
    
    client = google_genai.Client()
    
    search_prompt = get_web_search_prompt(query)

    response = client.models.generate_content(
        model=configurable.search_model,
        contents=search_prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=0.3
        )
    )

    resolved_urls = resolve_urls(response.candidates[0].grounding_metadata.grounding_chunks, 1)
    citations = get_citations(response, resolved_urls)

    modified_text = insert_citation_markers(response.text, citations)
    sources_gathered = [item for citation in citations for item in citation["segments"]]

    return {
        "sources_gathered": sources_gathered,
        "search_query": [state["search_query"]],
        "web_research_result": [modified_text],
    }


# 4. 리플렉션
def reflection(state: ProductRecommendationState, config: RunnableConfig) -> dict:
    """검색 결과를 평가하고 추가 검색이 필요한지 판단합니다."""
    
    configurable = ProductRecommendationConfig.from_runnable_config(config)
    
    llm = ChatGoogleGenerativeAI(
        model=configurable.analysis_model,
        temperature=0.1,
        max_retries=2,
        api_key=os.getenv("GEMINI_API_KEY")
    )
    
    # 현재 검색 결과 분석
    user_message = get_latest_user_message(state["messages"])
    candidate_products = state.get("candidate_products", [])
    search_queries = state.get("search_queries", [])
    
    reflection_prompt = get_reflection_prompt(user_message, candidate_products, search_queries)
    
    structured_llm = llm.with_structured_output(ReflectionResult)
    result = structured_llm.invoke(reflection_prompt)
    
    return {
        "is_sufficient": result.is_sufficient,
        "additional_queries": result.additional_queries if not result.is_sufficient else [],
        "search_loop_count": state.get("search_loop_count", 0) + 1
    }


# 5. 답변 생성
def answer_generation(state: ProductRecommendationState, config: RunnableConfig) -> dict:
    """최종 답변을 생성합니다. quickstart의 finalize_answer 패턴을 따릅니다."""
    
    configurable = ProductRecommendationConfig.from_runnable_config(config)
    
    # LLM 초기화
    llm = ChatGoogleGenerativeAI(
        model=configurable.analysis_model,  # 답변 생성에는 분석 모델 사용
        temperature=0.1,
        max_retries=2,
        api_key=os.getenv("GEMINI_API_KEY")
    )
    
    # 사용자 요청과 검색 결과 수집
    user_message = get_latest_user_message(state["messages"])
    web_research_results = state.get("web_research_result", [])
    sources_gathered = state.get("sources_gathered", [])
    
    # 답변 생성 프롬프트 구성
    summaries = "\n---\n".join(web_research_results) if web_research_results else "검색 결과가 없습니다."
    answer_prompt = get_answer_prompt(user_message, summaries)
    
    # 답변 생성
    result = llm.invoke(answer_prompt)
    
    # 단축 URL을 원본 URL로 변환
    final_content = result.content if result and hasattr(result, 'content') else "답변 생성에 실패했습니다."
    unique_sources = []
    
    if sources_gathered and isinstance(sources_gathered, list):
        for source in sources_gathered:
            if (isinstance(source, dict) and 
                source.get("short_url") and 
                source["short_url"] in final_content):
                # 단축 URL을 원본 URL로 교체
                final_content = final_content.replace(
                    source["short_url"], 
                    source.get("value", source["short_url"])
                )
                unique_sources.append(source)
    
    return {
        "messages": [AIMessage(content=final_content)],
        "sources_gathered": unique_sources,
        "response_to_user": final_content
    }

def should_refine_or_search(state: ProductRecommendationState) -> str:
    """요청의 구체성에 따른 라우팅 결정"""
    return "search" if state.get("is_request_specific", False) else "refine"

# ========== 그래프 구성 ==========

def create_product_recommendation_graph():
    """제품 추천 그래프 생성"""
    
    # 그래프 빌더 초기화
    builder = StateGraph(ProductRecommendationState, config_schema=ProductRecommendationConfig)
    
    # 노드 추가
    builder.add_node("validate_request", validate_request)
    builder.add_node("generate_search_queries", generate_search_queries)
    builder.add_node("web_search", web_search)
    builder.add_node("reflection", reflection)
    builder.add_node("answer_generation", answer_generation)
    
    # 엣지 구성
    builder.add_edge(START, "validate_request")
    builder.add_conditional_edges(
        "validate_request",
        should_refine_or_search,
        {
            "refine": END,  # 구체화 질문으로 종료
            "search": "generate_search_queries"  # 검색 진행
        }
    )
    builder.add_conditional_edges("generate_search_queries", continue_to_web_search, ["web_search"])
    builder.add_edge("web_search", "reflection")
    builder.add_edge("reflection", "answer_generation")
    builder.add_edge("answer_generation", END)
    
    return builder.compile()

# 그래프 인스턴스 생성
graph = create_product_recommendation_graph()
