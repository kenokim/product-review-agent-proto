from typing import List
from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage

# ========== 유틸리티 함수 ==========

def get_current_date():
    """현재 날짜를 읽기 쉬운 형태로 반환"""
    return datetime.now().strftime("%Y년 %m월 %d일")

# ========== 프롬프트 템플릿 ==========

validation_instructions = """당신은 제품 추천 전문가입니다. 사용자의 요청을 분석하여 제품 검색에 충분한 정보가 있는지 판단해주세요.

Instructions:
- 사용자의 요청이 구체적이고 검색 가능한지 평가하세요.
- 불충분한 경우 구체화를 위한 질문을 생성하세요.
- 현재 날짜는 {current_date}입니다.

구체적인 요청의 기준:
- 제품 카테고리가 명확함 (예: 노트북, 이어폰, 키보드 등)
- 용도나 목적이 언급됨 (예: 게이밍용, 업무용, 학습용 등)
- 예산이나 가격대가 언급됨 (예: 10만원 이하, 가성비 등)
- 브랜드 선호도나 특정 기능 요구사항이 있음

불충분한 요청 예시:
- "키보드 추천해줘"
- "좋은 노트북 알려줘"
- "이어폰 뭐가 좋을까?"

충분한 요청 예시:
- "10만원 이하 가성비 좋은 게이밍 키보드 추천해줘"
- "대학생용 문서작업 노트북 추천, 예산 100만원"
- "운동할 때 쓸 무선 이어폰, 방수 기능 있는 걸로"

Output Format:
- Format your response as a JSON object with these exact keys:
   - "is_specific": true or false
   - "clarification_question": 불충분할 경우 구체화를 위한 질문 (한국어, is_specific이 false인 경우만, 아니면 빈 문자열)
   - "extracted_requirements": 추출된 요구사항들을 JSON 객체로 (예: {{"카테고리": "키보드", "용도": "게이밍", "예산": "10만원"}})

사용자 요청: {user_message}"""

def get_validation_prompt(user_message: str) -> List:
    """요청 검증을 위한 프롬프트 생성"""
    current_date = get_current_date()
    system_prompt = validation_instructions.format(
        current_date=current_date,
        user_message=user_message
    )
    
    return [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"사용자 요청을 분석해주세요: {user_message}")
    ]

query_writer_instructions = """당신은 제품 검색 전문가입니다. 사용자의 요청을 분석하여 한국 커뮤니티와 리뷰 사이트에서 효과적인 검색어를 생성해주세요.

Instructions:
- 각 검색어는 서로 다른 관점을 다뤄야 합니다.
- 최대 {max_queries}개까지 생성하세요.
- 한국 커뮤니티와 리뷰 사이트에서 잘 검색될 수 있는 키워드를 사용하세요.
- 브랜드명, 가격대, 용도, 성능 등 다양한 각도에서 접근하세요.
- 현재 날짜는 {current_date}입니다. 최신 정보를 얻을 수 있는 검색어를 생성하세요.

검색어 생성 원칙:
1. 한국 커뮤니티 특화 키워드 포함 (디시, 클리앙, 뽐뿌 등)
2. 가격대 및 성능 관련 키워드 활용
3. 리뷰 및 사용기 관련 키워드 포함
4. 최신 트렌드 반영

검색어 예시:
- "가성비 게이밍 키보드 추천 2024 디시"
- "10만원 이하 기계식 키보드 후기 클리앙"
- "로지텍 레이저 키보드 리뷰 사용기"

Format:
- Format your response as a JSON object with these exact keys:
   - "rationale": 각 검색어를 선택한 이유에 대한 간단한 설명
   - "queries": 검색어 리스트

사용자 요청: {user_message}
추출된 의도: {user_intent}"""

def get_search_query_prompt(user_message: str, user_intent: str, max_queries: int) -> List:
    """검색어 생성을 위한 프롬프트"""
    current_date = get_current_date()
    system_prompt = query_writer_instructions.format(
        max_queries=max_queries,
        current_date=current_date,
        user_message=user_message,
        user_intent=user_intent
    )

    return [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"다음 요청에 대한 효과적인 검색어를 생성해주세요:\n요청: {user_message}\n의도: {user_intent}")
    ]

web_searcher_instructions = """한국 제품 추천 사이트에서 "{search_query}"에 대한 최신 정보를 수집하고 검증 가능한 제품 정보로 종합해주세요.

Instructions:
- 현재 날짜는 {current_date}입니다. 최신 정보를 우선적으로 수집하세요.
- 다양한 한국 커뮤니티 사이트에서 정보를 수집하세요.
- 각 정보의 출처를 정확히 추적하여 기록하세요.
- 검색 결과에서 찾은 정보만 포함하고, 임의로 정보를 만들어내지 마세요.

검색 시 주목할 사이트:
- 네이버 블로그, 카페
- 디시인사이드
- 클리앙
- 뽐뿌
- 다나와
- 쿠팡, 네이버쇼핑

각 검색 결과에서 다음 정보를 추출해주세요:
1. 추천 제품명 (정확한 모델명)
2. 가격 정보 및 가격대
3. 주요 특징 및 장점
4. 사용자 리뷰 및 추천 이유
5. 구매 링크 또는 상세 정보 링크
6. 출처 URL

검색 주제: {search_query}"""

def get_web_search_prompt(query: str) -> str:
    """웹 검색을 위한 프롬프트"""
    current_date = get_current_date()
    return web_searcher_instructions.format(
        search_query=query,
        current_date=current_date
    )

reflection_instructions = """당신은 제품 추천 결과를 평가하는 전문 리서치 어시스턴트입니다. "{user_request}"에 대한 검색 결과를 분석하고 있습니다.

Instructions:
- 현재 제품 목록이 사용자 요청을 충족하는지 분석하세요.
- 지식 격차나 더 깊이 탐색이 필요한 영역을 식별하고 후속 검색어를 생성하세요.
- 제공된 제품 목록이 사용자 질문에 답하기에 충분하다면 후속 검색어를 생성하지 마세요.
- 지식 격차가 있다면 이해를 확장하는 데 도움이 되는 후속 검색어를 생성하세요.
- 기술적 세부사항, 구현 사양 또는 완전히 다루어지지 않은 새로운 트렌드에 집중하세요.

Requirements:
- 후속 검색어는 자체적으로 완결되고 웹 검색에 필요한 컨텍스트를 포함해야 합니다.
- 한국 커뮤니티 사이트에서 검색하기 적합한 키워드를 사용하세요.

Output Format:
- Format your response as a JSON object with these exact keys:
   - "is_sufficient": true or false
   - "knowledge_gap": 누락된 정보나 명확화가 필요한 내용 설명 (is_sufficient가 true면 빈 문자열)
   - "additional_queries": 이 격차를 해결하기 위한 구체적인 검색어 목록 (is_sufficient가 true면 빈 배열)

Example:
```json
{{
    "is_sufficient": false,
    "knowledge_gap": "현재 결과에는 성능 벤치마크와 실제 사용자 후기가 부족합니다",
    "additional_queries": ["게이밍 키보드 성능 벤치마크 테스트 2024", "기계식 키보드 장기 사용 후기 클리앙"]
}}
```

검색 결과를 신중히 분석하여 지식 격차를 식별하고 이 JSON 형식에 따라 출력을 생성하세요:

사용자 요청: {user_request}
기존 검색어: {queries}
현재 제품 목록:
{products_summary}"""

def get_reflection_prompt(user_request: str, products: List, queries: List) -> List:
    """결과 평가를 위한 프롬프트"""
    products_summary = "\n".join([f"- {p.get('name', '알 수 없음')}: {p.get('price_range', '가격 미상')}" for p in products[:5]])
    
    system_prompt = reflection_instructions.format(
        user_request=user_request,
        queries=queries,
        products_summary=products_summary
    )
    
    return [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"다음 검색 결과를 분석하고 추가 검색이 필요한지 판단해주세요.")
    ]

answer_instructions = """사용자의 질문에 대해 제공된 제품 정보를 바탕으로 간결하고 핵심적인 추천 답변을 생성해주세요.

Instructions:
- 바로 핵심 추천 제품들을 5개까지 제시하세요. 불필요한 인사말이나 과정 설명은 생략하세요.
- 제품별로 명확한 추천 이유와 특징을 간결하게 설명하세요.
- 제품 정보에서 사용한 출처를 답변에 올바르게 포함하세요. 마크다운 형식을 사용하세요 (예: [네이버 블로그](https://example.com)).
- 한국어로 전문적이고 실용적인 톤으로 작성하세요.
- "마무리", "기타 추천 제품", "참고사항" 등의 불필요한 섹션은 생략하세요.
- 과도한 날짜 언급은 피하고, 필요한 경우에만 간단히 언급하세요.
- 핵심 추천 제품들에만 집중하여 답변하세요.

링크 관련 규칙:
- 검색 결과에 실제 구매 링크나 제품 상세 링크가 있는 경우에만 포함하세요.
- 임의로 링크를 생성하거나 "(예시)" 같은 가짜 표시를 하지 마세요.
- 실제 링크가 없으면 구매 링크 섹션을 아예 생략하세요.
- 출처 링크만 검색 결과에서 확인된 실제 링크를 사용하세요.
- 문자열을 보고 정상적인 링크인지 판단하시고, 아닐 경우 링크를 생략하세요.

Format:
- 사용자 요청에 대한 직접적인 추천으로 시작
- 각 제품별로 명확한 구성 (제품명, 가격대, 주요 특징, 추천 이유)
- 간결하고 실용적인 정보 위주로 구성
- 실제 존재하는 링크만 포함

사용자 요청: {user_request}

제품 정보:
{products_info}"""

def get_answer_prompt(user_request: str, products_info: str) -> List:
    """최종 답변 생성을 위한 프롬프트"""
    system_prompt = answer_instructions.format(
        user_request=user_request,
        products_info=products_info
    )
    
    return [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"다음 제품 정보를 바탕으로 사용자에게 추천 답변을 작성해주세요.")
    ]

# ========== 답변 검증 프롬프트 ==========

answer_validation_instructions = """당신은 제품 추천 답변의 품질을 검증하는 전문 평가자입니다. 생성된 답변이 사용자 요청에 적절하고 유용한지 간결하게 평가해주세요.

핵심 검증 기준:
- 사용자가 요청한 제품 카테고리와 관련된 추천이 포함되어 있는가?
- 제품 정보가 구체적이고 실용적인가?
- 가격대, 특징, 추천 이유가 명확히 제시되어 있는가?
- 답변이 사용자의 구매 결정에 도움이 되는가?
- 모든 링크가 올바른 마크다운 형식 `[텍스트](URL)`로 작성되었는가?
- 노출된 URL이나 잘못된 링크 형식이 없는가?

CRITICAL: 다음과 같은 문제가 발견되면 반드시 is_valid: false로 판정하세요:

1. 잘못된 링크 형식:
   - `[[1]]`, `[[2]]`, `[1]`, `[2]` 등의 숫자 참조
   - `(https://...)` 형태의 노출된 URL 
   - `https://...` 형태의 노출된 URL
   - `(예시)` 또는 유사한 가짜 표시

2. 허용되는 형식:
   - `[쿠팡](https://coupang.com)` ✅
   - `[다나와](https://danawa.com)` ✅
   - `[네이버 쇼핑](https://shopping.naver.com)` ✅

Output Format:
- Format your response as a JSON object with these exact keys:
   - "is_valid": true or false (위 기준을 모두 충족하면 true, 아니면 false)
   - "reason": 검증 결과의 간단한 이유 (한 문장)

사용자 요청: {user_request}
생성된 답변: {generated_answer}"""

def get_answer_validation_prompt(user_request: str, generated_answer: str) -> List:
    """답변 검증을 위한 프롬프트"""
    system_prompt = answer_validation_instructions.format(
        user_request=user_request,
        generated_answer=generated_answer
    )
    
    return [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"다음 답변의 품질을 평가하고 검증해주세요.")
    ]
