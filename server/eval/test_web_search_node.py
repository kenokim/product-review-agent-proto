#!/usr/bin/env python3
"""
웹 검색 노드 (Node 3) 단독 테스트 스크립트

Usage:
    python test_web_search_node.py
"""

import os
import sys
import time
import json
from pathlib import Path
from dotenv import load_dotenv

# 프로젝트 경로 추가
sys.path.append(str(Path(__file__).parent))

# 환경 변수 로드
load_dotenv()

# 로컬 모듈 import
from app.graph.graph import web_search
from app.graph.config import ProductRecommendationConfig
from langchain_core.runnables import RunnableConfig

def test_web_search_node():
    """웹 검색 노드 단독 테스트"""
    
    print("🧪 웹 검색 노드 (Node 3) 단독 테스트 시작")
    print("=" * 60)
    
    # 테스트 케이스 정의
    test_cases = [
        {
            "id": 0,
            "search_query": "10만원 이하 무선 이어폰 추천 2024",
            "description": "가성비 무선 이어폰 검색"
        },
        {
            "id": 1,
            "search_query": "게이밍 기계식 키보드 20만원 이하 추천",
            "description": "게이밍 키보드 검색"
        },
        {
            "id": 2,
            "search_query": "휴대용 모니터 30만원 이내 업무용",
            "description": "휴대용 모니터 검색"
        }
    ]
    
    # RunnableConfig 설정
    config = RunnableConfig(
        configurable={
            "search_model": "gemini-2.0-flash",
            "search_timeout": 20,
            "max_search_queries": 4,
            "required_search_results": 3
        }
    )
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🚀 테스트 케이스 {i}/{len(test_cases)}")
        print(f"📝 설명: {test_case['description']}")
        print(f"🔍 검색어: {test_case['search_query']}")
        print("-" * 40)
        
        # 노드 입력 상태 구성
        input_state = {
            "search_query": test_case["search_query"],
            "id": test_case["id"]
        }
        
        print(f"📥 입력 상태:")
        print(f"   - search_query: {input_state['search_query']}")
        print(f"   - id: {input_state['id']}")
        
        # 시간 측정 시작
        start_time = time.time()
        
        try:
            # 웹 검색 노드 실행
            print(f"\n⏳ 웹 검색 노드 실행 중...")
            output_state = web_search(input_state, config)
            
            # 실행 시간 계산
            elapsed_time = time.time() - start_time
            
            # 결과 분석
            sources_count = len(output_state.get("sources_gathered", []))
            search_queries_count = len(output_state.get("search_query", []))
            research_results_count = len(output_state.get("web_research_result", []))
            
            print(f"✅ 실행 완료! (소요 시간: {elapsed_time:.2f}초)")
            print(f"📤 출력 상태:")
            print(f"   - sources_gathered: {sources_count}개")
            print(f"   - search_query: {search_queries_count}개")
            print(f"   - web_research_result: {research_results_count}개")
            
            # 결과 미리보기
            if output_state.get("web_research_result"):
                result_preview = output_state["web_research_result"][0][:200]
                print(f"   - 결과 미리보기: {result_preview}...")
            
            # 테스트 결과 저장
            test_result = {
                "test_case": i,
                "description": test_case["description"],
                "input": input_state,
                "output": {
                    "sources_count": sources_count,
                    "search_queries_count": search_queries_count,
                    "research_results_count": research_results_count,
                    "elapsed_time": round(elapsed_time, 2),
                    "success": True
                },
                "raw_output": output_state  # 전체 출력 저장
            }
            
            results.append(test_result)
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"❌ 실행 실패! (소요 시간: {elapsed_time:.2f}초)")
            print(f"🚨 오류: {str(e)}")
            
            # 실패 결과 저장
            test_result = {
                "test_case": i,
                "description": test_case["description"],
                "input": input_state,
                "output": {
                    "sources_count": 0,
                    "search_queries_count": 0,
                    "research_results_count": 0,
                    "elapsed_time": round(elapsed_time, 2),
                    "success": False,
                    "error": str(e)
                },
                "raw_output": None
            }
            
            results.append(test_result)
    
    # 전체 결과 요약
    print("\n" + "=" * 60)
    print("📊 테스트 결과 요약")
    print("=" * 60)
    
    successful_tests = [r for r in results if r["output"]["success"]]
    failed_tests = [r for r in results if not r["output"]["success"]]
    
    print(f"총 테스트: {len(results)}개")
    print(f"성공: {len(successful_tests)}개")
    print(f"실패: {len(failed_tests)}개")
    
    if successful_tests:
        avg_time = sum(r["output"]["elapsed_time"] for r in successful_tests) / len(successful_tests)
        avg_sources = sum(r["output"]["sources_count"] for r in successful_tests) / len(successful_tests)
        print(f"평균 실행 시간: {avg_time:.2f}초")
        print(f"평균 출처 수: {avg_sources:.1f}개")
    
    if failed_tests:
        print(f"\n❌ 실패한 테스트:")
        for test in failed_tests:
            print(f"  - 테스트 {test['test_case']}: {test['output'].get('error', 'Unknown error')}")
    
    # 결과 파일 저장
    output_file = "web_search_node_test_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 상세 결과가 저장되었습니다: {output_file}")
    
    return results

def test_single_query(query: str, search_id: int = 0):
    """단일 쿼리 빠른 테스트"""
    
    print(f"🔍 단일 쿼리 테스트: {query}")
    
    config = RunnableConfig(
        configurable={
            "search_model": "gemini-2.0-flash",
            "search_timeout": 15  # 빠른 테스트를 위해 15초
        }
    )
    
    input_state = {
        "search_query": query,
        "id": search_id
    }
    
    start_time = time.time()
    
    try:
        result = web_search(input_state, config)
        elapsed_time = time.time() - start_time
        
        print(f"✅ 완료 ({elapsed_time:.2f}초)")
        print(f"📊 출처: {len(result.get('sources_gathered', []))}개")
        print(f"📄 결과: {len(result.get('web_research_result', []))}개")
        
        return result
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"❌ 실패 ({elapsed_time:.2f}초): {e}")
        return None

if __name__ == "__main__":
    # 명령행 인자 확인
    if len(sys.argv) > 1:
        # 단일 쿼리 테스트
        query = " ".join(sys.argv[1:])
        test_single_query(query)
    else:
        # 전체 테스트 실행
        test_web_search_node() 