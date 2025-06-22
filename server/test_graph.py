import pytest
from unittest.mock import MagicMock, patch
import asyncio
from app.graph.graph import create_product_recommendation_graph
from app.graph.state import ProductRecommendationState, Product
from app.graph.tools_and_schemas import ValidationResult, SearchQueryResult, ReflectionResult


class TestProductRecommendationGraph:
    """제품 추천 그래프 테스트 클래스"""
    
    @pytest.fixture
    def mock_llm(self):
        """LLM 모킹"""
        mock = MagicMock()
        mock.invoke.return_value = MagicMock(content="mocked response")
        return mock
    
    @pytest.fixture
    def sample_state(self):
        """테스트용 상태"""
        return ProductRecommendationState(
            messages=[{"role": "user", "content": "아이폰 추천해주세요"}],
            request_validation=None,
            search_queries=[],
            search_results=[],
            reflection_result=None,
            final_answer=""
        )

    # Level 0: 단위 테스트 - 개별 노드 테스트
    def test_validate_request_node_specific(self):
        """validate_request 노드만 테스트"""
        graph = create_product_recommendation_graph()
        
        # 특정 노드만 실행
        state = {"messages": [{"role": "user", "content": "아이폰 추천해주세요"}]}
        
        with patch('app.graph.graph.genai') as mock_genai:
            mock_genai.GenerativeModel.return_value.generate_content.return_value.text = '''
            {
                "is_specific": true,
                "extracted_requirements": {"category": "smartphone", "brand": "Apple"},
                "clarification_question": ""
            }
            '''
            
            # 노드 직접 실행
            result = graph.nodes["validate_request"].invoke(state)
            
            assert "request_validation" in result
            assert result["request_validation"]["is_specific"] == True

    def test_generate_queries_node_specific(self):
        """generate_queries 노드만 테스트"""
        graph = create_product_recommendation_graph()
        
        state = {
            "messages": [{"role": "user", "content": "아이폰 추천해주세요"}],
            "request_validation": ValidationResult(
                is_specific=True,
                extracted_requirements={"category": "smartphone"},
                clarification_question=""
            )
        }
        
        with patch('app.graph.graph.genai') as mock_genai:
            mock_genai.GenerativeModel.return_value.generate_content.return_value.text = '''
            {
                "queries": ["아이폰 15 리뷰", "아이폰 15 가격 비교", "아이폰 15 사용후기"]
            }
            '''
            
            result = graph.nodes["generate_queries"].invoke(state)
            
            assert "search_queries" in result
            assert len(result["search_queries"]) > 0

    # Level 1: 그래프 라우팅 테스트
    def test_graph_routing_specific_request(self):
        """구체적인 요청에 대한 라우팅 테스트"""
        with patch('app.graph.graph.genai') as mock_genai:
            # validate_request가 구체적이라고 응답하도록 설정
            mock_genai.GenerativeModel.return_value.generate_content.side_effect = [
                MagicMock(text='{"is_specific": true, "extracted_requirements": {}, "clarification_question": ""}'),
                MagicMock(text='{"queries": ["test query"]}'),
                MagicMock(text='test search results'),
                MagicMock(text='{"needs_more_search": false, "additional_queries": []}'),
                MagicMock(text='final answer')
            ]
            
            graph = create_product_recommendation_graph()
            
            # 그래프 실행 경로 추적
            state = {"messages": [{"role": "user", "content": "아이폰 15 추천해주세요"}]}
            
            # 중간 상태들을 확인하기 위해 stream 사용
            events = []
            for event in graph.stream(state):
                events.append(list(event.keys())[0])
            
            # 예상 경로: validate_request -> generate_queries -> web_search -> reflection -> format_response
            expected_path = ["validate_request", "generate_queries", "web_search", "reflection", "format_response"]
            assert events == expected_path

    def test_graph_routing_vague_request(self):
        """모호한 요청에 대한 라우팅 테스트"""
        with patch('app.graph.graph.genai') as mock_genai:
            # validate_request가 모호하다고 응답하도록 설정
            mock_genai.GenerativeModel.return_value.generate_content.return_value.text = '''
            {
                "is_specific": false,
                "extracted_requirements": {},
                "clarification_question": "어떤 종류의 제품을 찾고 계신가요?"
            }
            '''
            
            graph = create_product_recommendation_graph()
            
            state = {"messages": [{"role": "user", "content": "뭔가 추천해주세요"}]}
            
            events = []
            for event in graph.stream(state):
                events.append(list(event.keys())[0])
            
            # 모호한 요청은 바로 format_response로 가야 함
            expected_path = ["validate_request", "format_response"]
            assert events == expected_path

    # Level 2: 통합 테스트 (모킹된 응답 사용)
    def test_full_workflow_integration(self):
        """전체 워크플로 통합 테스트"""
        with patch('app.graph.graph.genai') as mock_genai:
            # 순서대로 각 노드의 응답 설정
            mock_genai.GenerativeModel.return_value.generate_content.side_effect = [
                # validate_request 응답
                MagicMock(text='{"is_specific": true, "extracted_requirements": {"category": "smartphone"}, "clarification_question": ""}'),
                # generate_queries 응답  
                MagicMock(text='{"queries": ["아이폰 15 리뷰", "아이폰 15 가격"]}'),
                # web_search 응답
                MagicMock(text='아이폰 15는 훌륭한 스마트폰입니다. 가격은 100만원 정도입니다.'),
                # reflection 응답
                MagicMock(text='{"needs_more_search": false, "additional_queries": []}'),
                # format_response 응답
                MagicMock(text='아이폰 15를 추천드립니다. 성능이 우수하고 가격은 100만원 정도입니다.')
            ]
            
            graph = create_product_recommendation_graph()
            
            initial_state = {
                "messages": [{"role": "user", "content": "아이폰 추천해주세요"}]
            }
            
            result = graph.invoke(initial_state)
            
            # 최종 결과 검증
            assert "final_answer" in result
            assert result["final_answer"] != ""
            assert "아이폰 15" in result["final_answer"]

    # 에러 처리 테스트
    def test_error_handling(self):
        """에러 상황 처리 테스트"""
        with patch('app.graph.graph.genai') as mock_genai:
            # LLM 호출에서 예외 발생
            mock_genai.GenerativeModel.return_value.generate_content.side_effect = Exception("API Error")
            
            graph = create_product_recommendation_graph()
            
            state = {"messages": [{"role": "user", "content": "테스트"}]}
            
            # 예외가 적절히 처리되는지 확인
            with pytest.raises(Exception):
                graph.invoke(state)

    # 상태 검증 테스트
    def test_state_validation(self):
        """상태 유효성 검증 테스트"""
        graph = create_product_recommendation_graph()
        
        # 잘못된 상태로 테스트
        invalid_state = {}  # messages 필드 없음
        
        with pytest.raises(Exception):
            graph.invoke(invalid_state)

    # 성능 테스트
    @pytest.mark.asyncio
    async def test_node_performance(self):
        """노드 실행 성능 테스트"""
        import time
        
        graph = create_product_recommendation_graph()
        
        state = {"messages": [{"role": "user", "content": "테스트"}]}
        
        with patch('app.graph.graph.genai') as mock_genai:
            mock_genai.GenerativeModel.return_value.generate_content.return_value.text = '{"is_specific": true, "extracted_requirements": {}, "clarification_question": ""}'
            
            start_time = time.time()
            result = graph.nodes["validate_request"].invoke(state)
            end_time = time.time()
            
            # 노드 실행이 1초 이내에 완료되는지 확인
            assert (end_time - start_time) < 1.0
            assert "request_validation" in result


# 유틸리티 함수들
def create_mock_graph_factory():
    """모킹된 노드들로 그래프 팩토리 생성"""
    def factory(mock_services):
        # 실제 그래프 구조는 유지하되 서비스만 모킹
        pass
    return factory


# 테스트 실행 예시
if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 