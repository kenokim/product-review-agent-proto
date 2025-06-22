import os
from typing import List
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai

# 프롬프트 함수 import
from .prompts import (
    get_validation_prompt,
    get_search_query_prompt,
    get_web_search_prompt,
    get_reflection_prompt,
    get_answer_prompt
)

# State 및 설정 import
from .state import (
    Product,
    ProductRecommendationState,
    ProductRecommendationConfig,
    get_latest_user_message
)

# 스키마 import
from .tools_and_schemas import (
    ValidationResult,
    SearchQueryResult,
    ReflectionResult
)

# Environment setup
from dotenv import load_dotenv

load_dotenv()

if os.getenv("GEMINI_API_KEY") is None:
    raise ValueError("GEMINI_API_KEY is not set")

# Gemini 클라이언트 초기화
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ========== 노드 구현 ==========

# 1. 검증 노드
def validate_request(state: ProductRecommendationState, config: RunnableConfig) -> dict:
    """사용자 요청의 구체성을 검증하고 필요시 구체화 질문을 생성합니다."""
    
    configurable = ProductRecommendationConfig.from_runnable_config(config)
    
    # LLM 초기화
    llm = ChatGoogleGenerativeAI(
        model=configurable.validation_model,
        temperature=0.1,
        max_retries=2,
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


def web_search(state: dict, config: RunnableConfig) -> dict:
    """Gemini API의 Google Search 기능을 사용하여 웹 검색을 수행하고 제품 후보를 추출합니다."""
    
    configurable = ProductRecommendationConfig.from_runnable_config(config)
    
    # 단일 검색어 처리 (병렬 처리용)
    query = state["search_query"]
    search_id = state["id"]
    
    try:
        # Gemini에 검색 프롬프트 구성
        search_prompt = get_web_search_prompt(query)

        # Gemini API 호출 (Google Search 도구 포함)
        model = genai.GenerativeModel(configurable.search_model)
        response = model.generate_content(
            search_prompt,
            tools=[{"google_search": {}}],
            generation_config=genai.types.GenerationConfig(temperature=0.3)
        )
        
        # grounding metadata에서 출처 정보 추출 (quickstart 방식)
        sources_gathered = []
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                for chunk in candidate.grounding_metadata.grounding_chunks:
                    if hasattr(chunk, 'web') and chunk.web:
                        sources_gathered.append({
                            "title": chunk.web.title,
                            "url": chunk.web.uri,
                            "search_id": search_id
                        })
        
        # 제품 정보 추출
        products = extract_products_from_search_result(response.text, sources_gathered)
        
        return {
            "search_queries": [query],
            "candidate_products": products,
            "sources_gathered": sources_gathered
        }
        
    except Exception as e:
        print(f"검색 오류 ({query}): {e}")
        return {
            "search_queries": [query],
            "candidate_products": [],
            "sources_gathered": []
        }


def extract_products_from_search_result(content: str, sources: List) -> List[Product]:
    """검색 결과에서 제품 정보를 추출합니다."""
    
    products = []
    
    try:
        # 검색 결과에서 제품 정보 추출 로직
        if "추천" in content and ("제품" in content or "상품" in content):
            # 간단한 파싱 - 실제로는 더 정교한 LLM 기반 추출 필요
            lines = content.split('\n')
            current_product = {}
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # 제품명 추출 시도
                if any(keyword in line for keyword in ['추천', '베스트', '인기', '순위']):
                    if current_product and current_product.get('name'):
                        products.append(current_product)
                        current_product = {}
                    
                    current_product = {
                        "name": line[:50],  # 첫 50자만
                        "source_url": sources[0]["url"] if sources else "",
                        "purchase_link": "",
                        "review_summary": content[:200] + "...",
                        "price_range": "가격 정보 확인 필요"
                    }
            
            # 마지막 제품 추가
            if current_product and current_product.get('name'):
                products.append(current_product)
            
            # 최소 1개는 반환
            if not products and sources:
                products.append({
                    "name": f"검색 결과 제품 ({len(sources)}개 출처)",
                    "source_url": sources[0]["url"],
                    "purchase_link": "",
                    "review_summary": content[:200] + "..." if content else "검색 결과를 확인해주세요.",
                    "price_range": "가격 정보 확인 필요"
                })
                
    except Exception as e:
        print(f"제품 추출 오류: {e}")
    
    return products[:3]  # 최대 3개까지


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


def should_continue_search(state: ProductRecommendationState) -> str:
    """추가 검색 필요성에 따른 라우팅 결정"""
    max_loops = state.get("max_search_loops", 2)
    current_loop = state.get("search_loop_count", 0)
    
    if state.get("is_sufficient", False) or current_loop >= max_loops:
        return "format_response"
    else:
        return "generate_search_queries"


def format_response(state: ProductRecommendationState, config: RunnableConfig) -> dict:
    """최종 추천 결과를 사용자 친화적인 형태로 포맷팅합니다."""
    
    user_message = get_latest_user_message(state["messages"])
    candidate_products = state.get("candidate_products", [])
    
    if not candidate_products:
        response = "죄송합니다. 요청하신 조건에 맞는 제품을 찾지 못했습니다. 다른 키워드로 다시 검색해보시겠어요?"
    else:
        response = format_product_recommendations(user_message, candidate_products)
    
    return {
        "response_to_user": response,
        "messages": [AIMessage(content=response)]
    }


def format_product_recommendations(user_request: str, products: List[Product]) -> str:
    """제품 추천 결과를 마크다운 형식으로 포맷팅"""
    
    response = f"**'{user_request}'** 요청에 대한 추천 제품입니다! 🎯\n\n"
    
    for i, product in enumerate(products[:5], 1):  # 최대 5개까지
        response += f"## {i}. {product['name']}\n\n"
        
        if product.get('price_range'):
            response += f"💰 **가격대**: {product['price_range']}\n\n"
        
        if product.get('review_summary'):
            response += f"📝 **제품 정보**:\n{product['review_summary']}\n\n"
        
        if product.get('purchase_link'):
            response += f"🛒 [구매하러 가기]({product['purchase_link']})\n\n"
        
        if product.get('source_url'):
            response += f"📚 [상세 정보 보기]({product['source_url']})\n\n"
        
        response += "---\n\n"
    
    response += "💡 **추가 문의사항이 있으시면 언제든 말씀해주세요!**"
    
    return response


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
    builder.add_node("format_response", format_response)
    
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
    builder.add_conditional_edges(
        "reflection",
        should_continue_search,
        {
            "generate_search_queries": "generate_search_queries",  # 추가 검색 필요
            "format_response": "format_response"  # 검색 완료
        }
    )
    builder.add_edge("format_response", END)
    
    return builder.compile()

# 그래프 인스턴스 생성 (quickstart 방식)
#graph = create_product_recommendation_graph()

# 테스트 그래프 구성
def create_test_product_recommendation_graph():
    """제품 추천 그래프 생성"""
    
    # 그래프 빌더 초기화
    builder = StateGraph(ProductRecommendationState, config_schema=ProductRecommendationConfig)
    
    # 노드 추가
    builder.add_node("validate_request", validate_request)
    builder.add_node("generate_search_queries", generate_search_queries)

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
    
    builder.add_edge("generate_search_queries", END)
    
    return builder.compile()

graph = create_test_product_recommendation_graph()