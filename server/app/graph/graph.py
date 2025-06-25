import os
import logging
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
    get_answer_prompt,
    # get_answer_validation_prompt
)
from .state import (
    ProductRecommendationState,
    get_latest_user_message
)
from .config import ProductRecommendationConfig
from .tools_and_schemas import (
    ValidationResult,
    SearchQueryResult,
    ReflectionResult,
    # AnswerValidationResult
)

load_dotenv()

# 로거 설정
logger = logging.getLogger(__name__)

if os.getenv("GEMINI_API_KEY") is None:
    raise ValueError("GEMINI_API_KEY is not set")

# ========== 노드 구현 ==========

# 1. 검증 노드
def validate_request(state: ProductRecommendationState, config: RunnableConfig) -> dict:
    """사용자 요청의 구체성을 검증하고 필요시 구체화 질문을 생성합니다."""
    
    logger.info("[validate_request] 노드 시작")
    
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
    logger.info(f"[validate_request] 사용자 메시지: {user_message[:100]}...")
    
    # 프롬프트 구성
    validation_prompt = get_validation_prompt(user_message)
    
    # LLM 호출
    result = structured_llm.invoke(validation_prompt)
    
    logger.info(f"[validate_request] 검증 완료 - 구체적 여부: {result.is_specific}")
    
    # 반려될 경우 AI 메시지를 state에 추가
    if not result.is_specific and result.clarification_question:
        ai_message = AIMessage(content=result.clarification_question)
        return {
            "is_request_specific": result.is_specific,
            "response_to_user": result.clarification_question,
            "user_intent": result.extracted_requirements.get("intent", ""),
            "messages": [ai_message]  # AI가 생성한 구체화 질문을 메시지로 추가
        }
    else:
        return {
            "is_request_specific": result.is_specific,
            "response_to_user": result.clarification_question if not result.is_specific else "",
            "user_intent": result.extracted_requirements.get("intent", "")
        }


# 2. 검색어 생성 노드
def generate_search_queries(state: ProductRecommendationState, config: RunnableConfig) -> dict:
    """구체화된 요청을 바탕으로 효과적인 검색어들을 생성합니다."""
    
    logger.info("[generate_search_queries] 노드 시작")
    
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
    
    logger.info(f"[generate_search_queries] 검색어 생성 완료 - {len(result.queries)}개 생성")
    for i, query in enumerate(result.queries, 1):
        logger.info(f"[generate_search_queries] 검색어 {i}: {query}")
    
    return {"search_queries": result.queries}


def continue_to_web_search(state: ProductRecommendationState):
    """LangGraph의 Send 이벤트를 사용한 동적 병렬 검색"""
    logger.info(f"[continue_to_web_search] 병렬 검색 시작 - {len(state['search_queries'])}개 검색어")
    return [
        Send("web_search", {"search_query": query, "id": int(idx)})
        for idx, query in enumerate(state["search_queries"])
    ]


# 3. 웹 검색 노드
def web_search(state: dict, config: RunnableConfig) -> dict:
    """Gemini API의 Google Search 기능을 사용하여 웹 검색을 수행하고 제품 후보를 추출합니다."""
    
    query = state["search_query"]
    search_id = state["id"]
    logger.info(f"[web_search] 검색 시작 - ID: {search_id}, 쿼리: {query}")
    
    try:
        from .utils import resolve_urls, get_citations, insert_citation_markers
        
        configurable = ProductRecommendationConfig.from_runnable_config(config)
        
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

        # 안전한 grounding_metadata 처리 (quickstart 패턴 참고)
        if (response.candidates and 
            len(response.candidates) > 0 and 
            response.candidates[0].grounding_metadata and
            response.candidates[0].grounding_metadata.grounding_chunks):
            
            resolved_urls = resolve_urls(response.candidates[0].grounding_metadata.grounding_chunks, search_id)
            citations = get_citations(response, resolved_urls)
            modified_text = insert_citation_markers(response.text, citations)
            sources_gathered = [item for citation in citations for item in citation["segments"]]
            
            logger.info(f"[web_search] 검색 완료 - ID: {search_id}, 출처: {len(sources_gathered)}개")
        else:
            logger.warning(f"[web_search] ID: {search_id} - grounding_metadata가 없음")
            modified_text = response.text if response.text else f"검색 실패: {query}"
            sources_gathered = []
            
            logger.info(f"[web_search] 검색 완료 - ID: {search_id}, 출처: 0개 (metadata 없음)")

        # quickstart 패턴과 동일한 반환 구조
        return {
            "sources_gathered": sources_gathered,
            "search_query": [state["search_query"]],
            "web_research_result": [modified_text],
        }
        
    except Exception as e:
        logger.error(f"[web_search] ID: {search_id} 검색 실패: {str(e)}")
        return {
            "sources_gathered": [],
            "search_query": [state["search_query"]],
            "web_research_result": [f"검색 오류: {query} - {str(e)}"],
        }


# 4. 리플렉션
def reflection(state: ProductRecommendationState, config: RunnableConfig) -> dict:
    """검색 결과를 평가하고 추가 검색이 필요한지 판단합니다."""
    
    logger.info("[reflection] 노드 시작")
    
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
    
    search_loop_count = state.get("search_loop_count", 0) + 1
    logger.info(f"[reflection] 반성 완료 - 충분 여부: {result.is_sufficient}, 검색 루프: {search_loop_count}")
    
    return {
        "is_sufficient": result.is_sufficient,
        "additional_queries": result.additional_queries if not result.is_sufficient else [],
        "search_loop_count": search_loop_count
    }


# 5. 답변 생성
def answer_generation(state: ProductRecommendationState, config: RunnableConfig) -> dict:
    """최종 답변을 생성합니다. quickstart의 finalize_answer 패턴을 따릅니다."""
    
    logger.info("[answer_generation] 노드 시작")
    
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
    
    logger.info(f"[answer_generation] 답변 생성 중 - 검색 결과: {len(web_research_results)}개, 출처: {len(sources_gathered)}개")
    
    # quickstart 패턴: web_research_result 리스트를 조인하여 summaries 생성
    if web_research_results:
        summaries = "\n---\n".join(web_research_results)
    else:
        summaries = "검색 결과가 없습니다."
        
    logger.info(f"[answer_generation] summaries 길이: {len(summaries)} 문자")
    
    # 답변 생성 프롬프트 구성
    answer_prompt = get_answer_prompt(user_message, summaries)
    
    # 답변 생성
    result = llm.invoke(answer_prompt)
    
    # quickstart 패턴: 단축 URL을 원본 URL로 변환
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
    
    logger.info(f"[answer_generation] 답변 생성 완료 - 최종 출처: {len(unique_sources)}개")
    
    return {
        "messages": [AIMessage(content=final_content)],
        "sources_gathered": unique_sources,
        "response_to_user": final_content
    }

# 6. 답변 검증
# def validate_answer(state: ProductRecommendationState, config: RunnableConfig) -> dict:
#     """생성된 답변의 품질을 검증하고 개선이 필요한지 판단합니다."""
#     
#     logger.info("[validate_answer] 노드 시작")
#     
#     configurable = ProductRecommendationConfig.from_runnable_config(config)
#     
#     # LLM 초기화
#     llm = ChatGoogleGenerativeAI(
#         model=configurable.validation_model,  # 검증용 모델 사용
#         temperature=0.1,
#         max_retries=2,
#         api_key=os.getenv("GEMINI_API_KEY")
#     )
#     
#     # 구조화된 출력을 위한 스키마 적용
#     structured_llm = llm.with_structured_output(AnswerValidationResult)
#     
#     # 사용자 요청과 생성된 답변 추출
#     user_message = get_latest_user_message(state["messages"])
#     generated_answer = state.get("response_to_user", "")
#     
#     logger.info(f"[validate_answer] 답변 검증 중 - 답변 길이: {len(generated_answer)} 문자")
#     
#     # 검증 프롬프트 구성
#     validation_prompt = get_answer_validation_prompt(user_message, generated_answer)
#     
#     # 검증 수행
#     result = structured_llm.invoke(validation_prompt)
#     
#     logger.info(f"[validate_answer] 검증 완료 - 유효성: {result.is_valid}, 이유: {result.reason}")
#     
#     return {
#         "answer_is_valid": result.is_valid,
#         "answer_validation_reason": result.reason
#     }

def should_refine_or_search(state: ProductRecommendationState) -> str:
    """요청의 구체성에 따른 라우팅 결정"""
    decision = "search" if state.get("is_request_specific", False) else "refine"
    logger.info(f"[should_refine_or_search] 라우팅 결정: {decision}")
    return decision

# ========== 그래프 구성 ==========

def create_product_recommendation_graph():
    """제품 추천 그래프 생성"""
    
    logger.info("제품 추천 그래프 생성 시작")
    
    # 그래프 빌더 초기화
    builder = StateGraph(ProductRecommendationState, config_schema=ProductRecommendationConfig)
    
    # 노드 추가
    builder.add_node("validate_request", validate_request)
    builder.add_node("generate_search_queries", generate_search_queries)
    builder.add_node("web_search", web_search)
    builder.add_node("reflection", reflection)
    builder.add_node("answer_generation", answer_generation)
    # builder.add_node("validate_answer", validate_answer)
    
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
    
    logger.info("제품 추천 그래프 생성 완료")
    
    return builder.compile()

# 그래프 인스턴스 생성
graph = create_product_recommendation_graph()
