import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google import genai as google_genai
from google.genai import types
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

from app.graph.utils import resolve_urls, get_citations, insert_citation_markers, get_current_date
from app.graph.prompts import reflection_instructions
from app.graph.tools_and_schemas import ReflectionResult

load_dotenv()

client = google_genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 한국어 웹 검색 프롬프트
def get_web_search_prompt(query, current_date):
    """한국어 웹 검색을 위한 프롬프트 생성"""
    return f"""주제 "{query}"에 대해 최신의 신뢰할 수 있는 정보를 수집하고 종합하여 검증 가능한 보고서를 작성해주세요.

지침:
- 가장 최신 정보를 수집하도록 검색해주세요. 오늘 날짜는 {current_date}입니다.
- 다양하고 포괄적인 검색을 통해 정보를 수집해주세요.
- 각 정보의 출처를 정확하게 추적하고 기록해주세요.
- 검색 결과를 바탕으로 잘 정리된 요약 또는 보고서를 작성해주세요.
- 검색 결과에서 찾은 정보만 포함하고, 임의로 정보를 만들어내지 마세요.
- 출처를 명확히 표시해주세요.

검색 주제: {query}"""


# 1. 웹 검색 1 - 키워드 검색
def web_search_1():
    config = types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="가성비 좋은 무선 이어폰",
        config=config
    )

    print(response.text)


# 2. 웹 검색 2 - 프롬프트 사용
def web_search_prompt():
    config = types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())]
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=get_web_search_prompt("가성비 좋은 무선 이어폰", "2025-06-23"),
        config=config
    )
    
    print(response.text)


# 3. 웹 검색 3 - grounding
def web_search_grounding():
    config = types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())]
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=get_web_search_prompt("가성비 좋은 무선 이어폰", "2025-06-23"),
        config=config
    )
    
    resolved_urls = resolve_urls(response.candidates[0].grounding_metadata.grounding_chunks, 1)
    #print(resolved_urls)

    citations = get_citations(response, resolved_urls)
    #print(citations)

    modified_text = insert_citation_markers(response.text, citations)
    print(modified_text)

    sources_gathered = [item for citation in citations for item in citation["segments"]]
    #print(sources_gathered)

    return modified_text


# 4. 리플렉션
def reflection(modified_text):
    formatted_prompt = reflection_instructions.format(
        user_request='가성비 좋은 무선 이어폰 추천해줘.',
        products_summary=modified_text,
        queries=['가성비 좋은 무선 이어폰']
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=1.0,
        max_retries=2,
        api_key=os.getenv("GEMINI_API_KEY")
    )

    result = llm.with_structured_output(ReflectionResult).invoke(formatted_prompt)
    
    print(result)


if __name__ == "__main__":
    print("=== 기본 웹 검색 실행 ===")
    #web_search_1()
    
    print("\n" + "="*50 + "\n")
    
    print("=== 프롬프트 웹 검색 실행 ===")
    #web_search_prompt()

    print("\n" + "="*50 + "\n")

    print("=== grounding 웹 검색 실행 ===")
    modified_text = web_search_grounding()

    print("\n" + "="*50 + "\n")

    print("=== 리플렉션 실행 ===")
    reflection(modified_text)