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


# 테스트 실행
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])  # -s 옵션으로 print 출력 표시 