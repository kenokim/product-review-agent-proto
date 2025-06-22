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
        
        assert "request_validation" in result
        assert result["request_validation"]["is_specific"] == True
        assert result["request_validation"]["extracted_requirements"] is not None
        
        print(f"\n📝 입력: '가성비 좋은 무선 이어폰 추천해주세요'")
        print(f"🔍 구체적 여부: {result['request_validation']['is_specific']}")
        print(f"📋 추출된 요구사항: {result['request_validation']['extracted_requirements']}")
        print(f"✅ 테스트 통과")

    def test_validate_request_greeting(self):
        """인사말 입력 - 안녕하세요"""
        graph = create_product_recommendation_graph()
        state = {"messages": [{"role": "user", "content": "안녕하세요"}]}
        
        result = graph.nodes["validate_request"].invoke(state)
        
        assert "request_validation" in result
        assert result["request_validation"]["is_specific"] == False
        assert result["request_validation"]["clarification_question"] != ""
        
        print(f"\n📝 입력: '안녕하세요'")
        print(f"🔍 구체적 여부: {result['request_validation']['is_specific']}")
        print(f"❓ 구체화 질문: {result['request_validation']['clarification_question']}")
        print(f"✅ 테스트 통과")

    def test_validate_request_vague_request(self):
        """모호한 요청 - 뭔가 추천해주세요"""
        graph = create_product_recommendation_graph()
        state = {"messages": [{"role": "user", "content": "뭔가 추천해주세요"}]}
        
        result = graph.nodes["validate_request"].invoke(state)
        
        assert "request_validation" in result
        assert result["request_validation"]["is_specific"] == False
        assert result["request_validation"]["clarification_question"] != ""
        
        print(f"\n📝 입력: '뭔가 추천해주세요'")
        print(f"🔍 구체적 여부: {result['request_validation']['is_specific']}")
        print(f"❓ 구체화 질문: {result['request_validation']['clarification_question']}")
        print(f"✅ 테스트 통과")

    def test_validate_request_gaming_laptop(self):
        """게임용 노트북 요청"""
        graph = create_product_recommendation_graph()
        state = {"messages": [{"role": "user", "content": "200만원 이하 게임용 노트북 추천해주세요"}]}
        
        result = graph.nodes["validate_request"].invoke(state)
        
        assert "request_validation" in result
        assert result["request_validation"]["is_specific"] == True
        assert result["request_validation"]["extracted_requirements"] is not None
        
        print(f"\n📝 입력: '200만원 이하 게임용 노트북 추천해주세요'")
        print(f"🔍 구체적 여부: {result['request_validation']['is_specific']}")
        print(f"📋 추출된 요구사항: {result['request_validation']['extracted_requirements']}")
        print(f"✅ 테스트 통과")

    def test_validate_request_smartphone(self):
        """스마트폰 요청 - 아이폰 vs 갤럭시"""
        graph = create_product_recommendation_graph()
        state = {"messages": [{"role": "user", "content": "아이폰이랑 갤럭시 중에 뭐가 좋을까요?"}]}
        
        result = graph.nodes["validate_request"].invoke(state)
        
        assert "request_validation" in result
        assert result["request_validation"]["is_specific"] == True
        assert result["request_validation"]["extracted_requirements"] is not None
        
        print(f"\n📝 입력: '아이폰이랑 갤럭시 중에 뭐가 좋을까요?'")
        print(f"🔍 구체적 여부: {result['request_validation']['is_specific']}")
        print(f"📋 추출된 요구사항: {result['request_validation']['extracted_requirements']}")
        print(f"✅ 테스트 통과")

    def test_generate_search_queries_earphones(self):
        """무선 이어폰에 대한 검색 쿼리 생성"""
        graph = create_product_recommendation_graph()
        state = {
            "messages": [{"role": "user", "content": "가성비 좋은 무선 이어폰 추천해주세요"}],
            "request_validation": ValidationResult(
                is_specific=True,
                extracted_requirements={"category": "이어폰", "type": "무선", "criteria": "가성비"},
                clarification_question=""
            )
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
            "request_validation": ValidationResult(
                is_specific=True,
                extracted_requirements={"category": "노트북", "purpose": "게임용", "budget": "200만원 이하"},
                clarification_question=""
            )
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


# 테스트 실행
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])  # -s 옵션으로 print 출력 표시 