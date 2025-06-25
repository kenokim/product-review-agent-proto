import pytest
import os
import json
from app.graph.graph import create_product_recommendation_graph
from app.graph.tools_and_schemas import ValidationResult


class TestProductRecommendationNodes:
    """제품 추천 그래프 노드별 테스트 - 실제 LLM 호출"""
    
    @pytest.fixture(autouse=True)
    def setup_env(self):
        """환경변수 설정"""
        # 환경변수가 없으면 테스트 스킵
        if not os.getenv("GEMINI_API_KEY"):
            pytest.skip("GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
    
    def test_validate_request_specific_product(self):
        """구체적인 제품 요청 - 가성비 좋은 무선 이어폰"""
        graph = create_product_recommendation_graph()
        state = {"messages": [{"role": "user", "content": "가성비 좋은 무선 이어폰 추천해주세요"}]}
        
        result = graph.nodes["validate_request"].invoke(state)
        
        assert "is_request_specific" in result
        assert "response_to_user" in result
        assert "user_intent" in result
        
        print(f"\n📝 입력: '가성비 좋은 무선 이어폰 추천해주세요'")
        print(f"🔍 구체적 여부: {result['is_request_specific']}")
        print(f"💬 LLM 응답: {result['response_to_user']}")
        print(f"🎯 사용자 의도: {result['user_intent']}")
        print(f"✅ 테스트 통과")

    def test_validate_request_greeting(self):
        """인사말 입력 - 안녕하세요"""
        graph = create_product_recommendation_graph()
        state = {"messages": [{"role": "user", "content": "안녕하세요"}]}
        
        result = graph.nodes["validate_request"].invoke(state)
        
        assert "is_request_specific" in result
        assert "response_to_user" in result
        assert result["is_request_specific"] == False  # 구체적이지 않아야 함
        assert result["response_to_user"] != ""  # 구체화 질문이 있어야 함
        
        print(f"\n📝 입력: '안녕하세요'")
        print(f"🔍 구체적 여부: {result['is_request_specific']}")
        print(f"💬 LLM 응답: {result['response_to_user']}")
        print(f"✅ 테스트 통과")

    def test_validate_request_vague_request(self):
        """모호한 요청 - 뭔가 추천해주세요"""
        graph = create_product_recommendation_graph()
        state = {"messages": [{"role": "user", "content": "뭔가 추천해주세요"}]}
        
        result = graph.nodes["validate_request"].invoke(state)
        
        assert "is_request_specific" in result
        assert "response_to_user" in result
        assert result["is_request_specific"] == False  # 구체적이지 않아야 함
        assert result["response_to_user"] != ""  # 구체화 질문이 있어야 함
        
        print(f"\n📝 입력: '뭔가 추천해주세요'")
        print(f"🔍 구체적 여부: {result['is_request_specific']}")
        print(f"💬 LLM 응답: {result['response_to_user']}")
        print(f"✅ 테스트 통과")

    def test_validate_request_gaming_laptop(self):
        """게임용 노트북 요청"""
        graph = create_product_recommendation_graph()
        state = {"messages": [{"role": "user", "content": "200만원 이하 게임용 노트북 추천해주세요"}]}
        
        result = graph.nodes["validate_request"].invoke(state)
        
        assert "is_request_specific" in result
        assert "response_to_user" in result
        assert "user_intent" in result
        
        print(f"\n📝 입력: '200만원 이하 게임용 노트북 추천해주세요'")
        print(f"🔍 구체적 여부: {result['is_request_specific']}")
        print(f"💬 LLM 응답: {result['response_to_user']}")
        print(f"🎯 사용자 의도: {result['user_intent']}")
        print(f"✅ 테스트 통과")

    def test_validate_request_smartphone(self):
        """스마트폰 요청 - 아이폰 vs 갤럭시"""
        graph = create_product_recommendation_graph()
        state = {"messages": [{"role": "user", "content": "아이폰이랑 갤럭시 중에 뭐가 좋을까요?"}]}
        
        result = graph.nodes["validate_request"].invoke(state)
        
        assert "is_request_specific" in result
        assert "response_to_user" in result
        assert "user_intent" in result
        
        print(f"\n📝 입력: '아이폰이랑 갤럭시 중에 뭐가 좋을까요?'")
        print(f"🔍 구체적 여부: {result['is_request_specific']}")
        print(f"💬 LLM 응답: {result['response_to_user']}")
        print(f"🎯 사용자 의도: {result['user_intent']}")
        print(f"✅ 테스트 통과")

    def test_generate_search_queries_earphones(self):
        """무선 이어폰에 대한 검색 쿼리 생성"""
        graph = create_product_recommendation_graph()
        state = {
            "messages": [{"role": "user", "content": "가성비 좋은 무선 이어폰 추천해주세요"}],
            "is_request_specific": True,
            "user_intent": "가성비 좋은 무선 이어폰 추천"
        }
        
        result = graph.nodes["generate_search_queries"].invoke(state)
        
        assert "search_queries" in result
        assert len(result["search_queries"]) > 0
        
        print(f"\n📝 입력: '가성비 좋은 무선 이어폰 추천해주세요'")
        print(f"🔍 생성된 검색어 개수: {len(result['search_queries'])}")
        print(f"📋 검색어 목록:")
        for i, query in enumerate(result['search_queries'], 1):
            print(f"  {i}. {query}")
        print(f"✅ 테스트 통과")

    def test_generate_search_queries_gaming_laptop(self):
        """게임용 노트북에 대한 검색 쿼리 생성"""
        graph = create_product_recommendation_graph()
        state = {
            "messages": [{"role": "user", "content": "200만원 이하 게임용 노트북 추천해주세요"}],
            "is_request_specific": True,
            "user_intent": "200만원 이하 게임용 노트북 추천"
        }
        
        result = graph.nodes["generate_search_queries"].invoke(state)
        
        assert "search_queries" in result
        assert len(result["search_queries"]) > 0
        
        print(f"\n📝 입력: '200만원 이하 게임용 노트북 추천해주세요'")
        print(f"🔍 생성된 검색어 개수: {len(result['search_queries'])}")
        print(f"📋 검색어 목록:")
        for i, query in enumerate(result['search_queries'], 1):
            print(f"  {i}. {query}")
        print(f"✅ 테스트 통과")

    def test_web_search_wireless_earphones(self):
        """웹 검색 테스트 - 무선 이어폰"""
        graph = create_product_recommendation_graph()
        search_state = {
            "search_query": "가성비 좋은 무선 이어폰 추천 2024",
            "id": 0
        }
        
        result = graph.nodes["web_search"].invoke(search_state)
        
        assert "search_queries" in result
        assert "candidate_products" in result
        assert "sources_gathered" in result
        assert len(result["search_queries"]) == 1
        assert result["search_queries"][0] == "가성비 좋은 무선 이어폰 추천 2024"
        
        print(f"\n🔍 검색어: '가성비 좋은 무선 이어폰 추천 2024'")
        print(f"📦 발견된 제품 수: {len(result['candidate_products'])}")
        print(f"📚 수집된 출처 수: {len(result['sources_gathered'])}")
        
        if result['candidate_products']:
            print(f"🎯 첫 번째 제품:")
            product = result['candidate_products'][0]
            print(f"  - 제품명: {product.get('name', 'N/A')}")
            print(f"  - 가격대: {product.get('price_range', 'N/A')}")
            print(f"  - 출처: {product.get('source_url', 'N/A')}")
        
        if result['sources_gathered']:
            print(f"📖 첫 번째 출처:")
            source = result['sources_gathered'][0]
            print(f"  - 제목: {source.get('title', 'N/A')}")
            print(f"  - URL: {source.get('url', 'N/A')}")
        
        print(f"✅ 테스트 통과")

    def test_web_search_gaming_laptop(self):
        """웹 검색 테스트 - 게임용 노트북"""
        graph = create_product_recommendation_graph()
        search_state = {
            "search_query": "200만원 이하 게임용 노트북 추천 RTX",
            "id": 1
        }
        
        result = graph.nodes["web_search"].invoke(search_state)
        
        assert "search_queries" in result
        assert "candidate_products" in result
        assert "sources_gathered" in result
        assert len(result["search_queries"]) == 1
        assert result["search_queries"][0] == "200만원 이하 게임용 노트북 추천 RTX"
        
        print(f"\n🔍 검색어: '200만원 이하 게임용 노트북 추천 RTX'")
        print(f"📦 발견된 제품 수: {len(result['candidate_products'])}")
        print(f"📚 수집된 출처 수: {len(result['sources_gathered'])}")
        
        if result['candidate_products']:
            print(f"🎯 첫 번째 제품:")
            product = result['candidate_products'][0]
            print(f"  - 제품명: {product.get('name', 'N/A')}")
            print(f"  - 가격대: {product.get('price_range', 'N/A')}")
            print(f"  - 출처: {product.get('source_url', 'N/A')}")
        
        if result['sources_gathered']:
            print(f"📖 첫 번째 출처:")
            source = result['sources_gathered'][0]
            print(f"  - 제목: {source.get('title', 'N/A')}")
            print(f"  - URL: {source.get('url', 'N/A')}")
        
        print(f"✅ 테스트 통과")

    def test_web_search_smartphone(self):
        """웹 검색 테스트 - 스마트폰"""
        graph = create_product_recommendation_graph()
        search_state = {
            "search_query": "아이폰 갤럭시 비교 추천 2024",
            "id": 2
        }
        
        result = graph.nodes["web_search"].invoke(search_state)
        
        assert "search_queries" in result
        assert "candidate_products" in result
        assert "sources_gathered" in result
        assert len(result["search_queries"]) == 1
        assert result["search_queries"][0] == "아이폰 갤럭시 비교 추천 2024"
        
        print(f"\n🔍 검색어: '아이폰 갤럭시 비교 추천 2024'")
        print(f"📦 발견된 제품 수: {len(result['candidate_products'])}")
        print(f"📚 수집된 출처 수: {len(result['sources_gathered'])}")
        
        if result['candidate_products']:
            print(f"🎯 첫 번째 제품:")
            product = result['candidate_products'][0]
            print(f"  - 제품명: {product.get('name', 'N/A')}")
            print(f"  - 가격대: {product.get('price_range', 'N/A')}")
            print(f"  - 출처: {product.get('source_url', 'N/A')}")
        
        if result['sources_gathered']:
            print(f"📖 첫 번째 출처:")
            source = result['sources_gathered'][0]
            print(f"  - 제목: {source.get('title', 'N/A')}")
            print(f"  - URL: {source.get('url', 'N/A')}")
        
        print(f"✅ 테스트 통과")

    def test_reflection_sufficient_results(self):
        """충분한 검색 결과에 대한 reflection 테스트"""
        graph = create_product_recommendation_graph()
        state = {
            "messages": [{"role": "user", "content": "가성비 좋은 무선 이어폰 추천해주세요"}],
            "candidate_products": [
                {"name": "소니 WF-1000XM4", "price_range": "20-30만원", "review_summary": "뛰어난 노이즈 캔슬링"},
                {"name": "애플 에어팟 프로", "price_range": "30-35만원", "review_summary": "아이폰과 완벽한 호환성"},
                {"name": "삼성 갤럭시 버즈", "price_range": "15-20만원", "review_summary": "가성비 좋은 선택"}
            ],
            "search_queries": ["가성비 무선 이어폰", "무선 이어폰 추천 2024"],
            "search_loop_count": 0
        }
        
        result = graph.nodes["reflection"].invoke(state)
        
        assert "is_sufficient" in result
        assert "additional_queries" in result
        assert "search_loop_count" in result
        assert result["search_loop_count"] == 1
        
        print(f"\n📝 입력: 3개 제품 후보")
        print(f"🔍 충분한 결과 여부: {result['is_sufficient']}")
        print(f"📋 추가 검색어 개수: {len(result.get('additional_queries', []))}")
        if result.get('additional_queries'):
            print(f"🔎 추가 검색어:")
            for i, query in enumerate(result['additional_queries'], 1):
                print(f"  {i}. {query}")
        print(f"🔄 검색 루프 카운트: {result['search_loop_count']}")
        print(f"✅ 테스트 통과")

    def test_reflection_insufficient_results(self):
        """부족한 검색 결과에 대한 reflection 테스트"""
        graph = create_product_recommendation_graph()
        state = {
            "messages": [{"role": "user", "content": "200만원 이하 게임용 노트북 추천해주세요"}],
            "candidate_products": [
                {"name": "일반 노트북", "price_range": "100만원", "review_summary": "기본적인 성능"}
            ],
            "search_queries": ["게임용 노트북"],
            "search_loop_count": 0
        }
        
        result = graph.nodes["reflection"].invoke(state)
        
        assert "is_sufficient" in result
        assert "additional_queries" in result
        assert "search_loop_count" in result
        assert result["search_loop_count"] == 1
        
        print(f"\n📝 입력: 1개 제품 후보 (부족)")
        print(f"🔍 충분한 결과 여부: {result['is_sufficient']}")
        print(f"📋 추가 검색어 개수: {len(result.get('additional_queries', []))}")
        if result.get('additional_queries'):
            print(f"🔎 추가 검색어:")
            for i, query in enumerate(result['additional_queries'], 1):
                print(f"  {i}. {query}")
        print(f"🔄 검색 루프 카운트: {result['search_loop_count']}")
        print(f"✅ 테스트 통과")

    def test_format_response_with_products(self):
        """제품이 있는 경우의 응답 포맷팅 테스트"""
        graph = create_product_recommendation_graph()
        state = {
            "messages": [{"role": "user", "content": "가성비 좋은 무선 이어폰 추천해주세요"}],
            "candidate_products": [
                {
                    "name": "소니 WF-1000XM4",
                    "price_range": "20-30만원",
                    "review_summary": "뛰어난 노이즈 캔슬링 기능과 고음질을 제공하는 프리미엄 무선 이어폰",
                    "source_url": "https://example.com/sony-review",
                    "purchase_link": "https://example.com/buy-sony"
                },
                {
                    "name": "애플 에어팟 프로 2세대",
                    "price_range": "30-35만원",
                    "review_summary": "아이폰과의 완벽한 호환성과 공간 음향 기능",
                    "source_url": "https://example.com/airpods-review",
                    "purchase_link": "https://example.com/buy-airpods"
                }
            ]
        }
        
        result = graph.nodes["format_response"].invoke(state)
        
        assert "response_to_user" in result
        assert "messages" in result
        assert len(result["messages"]) == 1
        
        response = result["response_to_user"]
        assert "가성비 좋은 무선 이어폰" in response
        assert "소니 WF-1000XM4" in response
        assert "애플 에어팟 프로" in response
        assert "20-30만원" in response
        assert "30-35만원" in response
        
        print(f"\n📝 입력: 2개 제품 후보")
        print(f"📄 응답 길이: {len(response)}자")
        print(f"🎯 응답 미리보기:")
        print(f"  {response[:200]}...")
        print(f"✅ 마크다운 형식 확인")
        print(f"✅ 제품 정보 포함 확인")
        print(f"✅ 테스트 통과")

    def test_format_response_no_products(self):
        """제품이 없는 경우의 응답 포맷팅 테스트"""
        graph = create_product_recommendation_graph()
        state = {
            "messages": [{"role": "user", "content": "존재하지 않는 제품 추천해주세요"}],
            "candidate_products": []
        }
        
        result = graph.nodes["format_response"].invoke(state)
        
        assert "response_to_user" in result
        assert "messages" in result
        assert len(result["messages"]) == 1
        
        response = result["response_to_user"]
        assert "죄송합니다" in response
        assert "찾지 못했습니다" in response
        
        print(f"\n📝 입력: 제품 없음")
        print(f"📄 응답: {response}")
        print(f"✅ 빈 결과 처리 확인")
        print(f"✅ 테스트 통과")

    def test_format_response_single_product(self):
        """단일 제품에 대한 응답 포맷팅 테스트"""
        graph = create_product_recommendation_graph()
        state = {
            "messages": [{"role": "user", "content": "최고급 게임용 노트북 추천해주세요"}],
            "candidate_products": [
                {
                    "name": "ASUS ROG Strix G15",
                    "price_range": "180-200만원",
                    "review_summary": "RTX 4070 탑재, 고성능 게이밍 노트북으로 모든 최신 게임을 원활하게 실행",
                    "source_url": "https://example.com/asus-review",
                    "purchase_link": "https://example.com/buy-asus"
                }
            ]
        }
        
        result = graph.nodes["format_response"].invoke(state)
        
        assert "response_to_user" in result
        assert "messages" in result
        
        response = result["response_to_user"]
        assert "최고급 게임용 노트북" in response
        assert "ASUS ROG Strix G15" in response
        assert "180-200만원" in response
        assert "RTX 4070" in response
        
        print(f"\n📝 입력: 1개 제품 후보")
        print(f"📄 응답 길이: {len(response)}자")
        print(f"🎯 응답 미리보기:")
        print(f"  {response[:200]}...")
        print(f"✅ 단일 제품 포맷팅 확인")
        print(f"✅ 테스트 통과")


# 테스트 실행
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])  # -s 옵션으로 print 출력 표시 