import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import aiohttp
import aiofiles
from dataclasses import dataclass, asdict

@dataclass
class TestResult:
    """테스트 결과 데이터 클래스"""
    test_id: int
    query: str
    response: str
    sources: List[Dict[str, Any]]
    response_time_ms: float
    status_code: int
    timestamp: str
    error: str = None

class TestQuerySender:
    """테스트 쿼리 전송 및 결과 수집 클래스"""
    
    def __init__(self, 
                 api_url: str = "http://localhost:8000/api/v1/chat",
                 test_case_file: str = "test_case.json",
                 output_file: str = "test_results.json",
                 max_concurrent: int = 3):
        self.api_url = api_url
        self.test_case_file = Path(test_case_file)
        self.output_file = Path(output_file)
        self.max_concurrent = max_concurrent
        self.results: List[TestResult] = []
        
    async def load_test_cases(self) -> List[Dict[str, Any]]:
        """테스트 케이스 파일 로드"""
        try:
            async with aiofiles.open(self.test_case_file, 'r', encoding='utf-8') as f:
                content = await f.read()
                test_cases = json.loads(content)
                print(f"✅ {len(test_cases)}개의 테스트 케이스를 로드했습니다.")
                return test_cases
        except FileNotFoundError:
            print(f"❌ 테스트 케이스 파일을 찾을 수 없습니다: {self.test_case_file}")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ JSON 파싱 오류: {e}")
            return []
    
    async def save_individual_result(self, result: TestResult) -> None:
        """개별 테스트 결과를 별도 파일로 저장"""
        individual_file = Path(f"test_result_{result.test_id}.json")
        
        try:
            result_data = {
                "test_info": {
                    "test_id": result.test_id,
                    "timestamp": result.timestamp,
                    "response_time_ms": result.response_time_ms,
                    "status_code": result.status_code,
                    "success": result.error is None
                },
                "query": result.query,
                "response": result.response,
                "sources": result.sources,
                "error": result.error
            }
            
            async with aiofiles.open(individual_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(result_data, ensure_ascii=False, indent=2))
                
            print(f"💾 Test {result.test_id} 결과 저장: {individual_file}")
            
        except Exception as e:
            print(f"❌ Test {result.test_id} 개별 저장 실패: {e}")

    async def send_query(self, session: aiohttp.ClientSession, test_case: Dict[str, Any]) -> TestResult:
        """개별 쿼리 전송"""
        test_id = test_case['id']
        query = test_case['query']
        
        print(f"🚀 Test {test_id}: '{query[:50]}...' 요청 시작")
        
        payload = {
            "message": query
        }
        
        start_time = time.time()
        
        try:
            async with session.post(
                self.api_url,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=120)  # 2분 타임아웃
            ) as response:
                response_time_ms = (time.time() - start_time) * 1000
                response_data = await response.json()
                
                # 응답 데이터 파싱
                message = response_data.get('message', '')
                sources = response_data.get('sources', [])
                
                result = TestResult(
                    test_id=test_id,
                    query=query,
                    response=message,
                    sources=sources,
                    response_time_ms=round(response_time_ms, 2),
                    status_code=response.status,
                    timestamp=datetime.now().isoformat()
                )
                
                # 개별 결과 즉시 저장
                await self.save_individual_result(result)
                
                print(f"✅ Test {test_id}: 완료 ({response_time_ms:.0f}ms)")
                return result
                
        except asyncio.TimeoutError:
            print(f"⏰ Test {test_id}: 타임아웃")
            result = TestResult(
                test_id=test_id,
                query=query,
                response="",
                sources=[],
                response_time_ms=(time.time() - start_time) * 1000,
                status_code=0,
                timestamp=datetime.now().isoformat(),
                error="Timeout"
            )
            
            # 실패 결과도 개별 저장
            await self.save_individual_result(result)
            return result
            
        except Exception as e:
            print(f"❌ Test {test_id}: 오류 - {str(e)}")
            result = TestResult(
                test_id=test_id,
                query=query,
                response="",
                sources=[],
                response_time_ms=(time.time() - start_time) * 1000,
                status_code=0,
                timestamp=datetime.now().isoformat(),
                error=str(e)
            )
            
            # 실패 결과도 개별 저장
            await self.save_individual_result(result)
            return result
    
    async def run_tests(self) -> List[TestResult]:
        """모든 테스트 실행"""
        test_cases = await self.load_test_cases()
        
        if not test_cases:
            print("❌ 실행할 테스트 케이스가 없습니다.")
            return []
        
        print(f"🚀 {len(test_cases)}개 테스트 케이스를 최대 {self.max_concurrent}개씩 병렬 실행합니다.")
        print(f"📡 API URL: {self.api_url}")
        print("-" * 60)
        
        # 세마포어로 동시 요청 수 제한
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def bounded_send_query(session: aiohttp.ClientSession, test_case: Dict[str, Any]):
            async with semaphore:
                return await self.send_query(session, test_case)
        
        async with aiohttp.ClientSession() as session:
            tasks = [
                bounded_send_query(session, test_case) 
                for test_case in test_cases
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 예외 처리
            valid_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"❌ Test {test_cases[i]['id']}: 예외 발생 - {result}")
                    valid_results.append(TestResult(
                        test_id=test_cases[i]['id'],
                        query=test_cases[i]['query'],
                        response="",
                        sources=[],
                        response_time_ms=0,
                        status_code=0,
                        timestamp=datetime.now().isoformat(),
                        error=str(result)
                    ))
                else:
                    valid_results.append(result)
            
            self.results = valid_results
            return valid_results
    
    async def save_results(self) -> None:
        """결과 저장"""
        if not self.results:
            print("❌ 저장할 결과가 없습니다.")
            return
        
        # 결과를 딕셔너리로 변환
        results_data = {
            "test_summary": {
                "total_tests": len(self.results),
                "successful_tests": len([r for r in self.results if r.error is None]),
                "failed_tests": len([r for r in self.results if r.error is not None]),
                "average_response_time_ms": round(
                    sum(r.response_time_ms for r in self.results if r.error is None) / 
                    len([r for r in self.results if r.error is None]), 2
                ) if any(r.error is None for r in self.results) else 0,
                "timestamp": datetime.now().isoformat()
            },
            "test_results": [asdict(result) for result in self.results]
        }
        
        try:
            async with aiofiles.open(self.output_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(results_data, ensure_ascii=False, indent=2))
            
            print(f"💾 결과가 저장되었습니다: {self.output_file}")
            print(f"📊 성공: {results_data['test_summary']['successful_tests']}개")
            print(f"📊 실패: {results_data['test_summary']['failed_tests']}개")
            print(f"📊 평균 응답시간: {results_data['test_summary']['average_response_time_ms']}ms")
            
        except Exception as e:
            print(f"❌ 결과 저장 실패: {e}")
    
    def print_summary(self) -> None:
        """결과 요약 출력"""
        if not self.results:
            return
        
        print("\n" + "="*60)
        print("📋 테스트 결과 요약")
        print("="*60)
        
        successful = [r for r in self.results if r.error is None]
        failed = [r for r in self.results if r.error is not None]
        
        print(f"총 테스트: {len(self.results)}개")
        print(f"성공: {len(successful)}개")
        print(f"실패: {len(failed)}개")
        
        if successful:
            avg_time = sum(r.response_time_ms for r in successful) / len(successful)
            print(f"평균 응답시간: {avg_time:.2f}ms")
            print(f"최고 응답시간: {max(r.response_time_ms for r in successful):.2f}ms")
            print(f"최저 응답시간: {min(r.response_time_ms for r in successful):.2f}ms")
        
        if failed:
            print(f"\n❌ 실패한 테스트:")
            for result in failed:
                print(f"  - Test {result.test_id}: {result.error}")

async def cleanup_individual_files():
    """개별 테스트 결과 파일들을 results 폴더로 이동"""
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    individual_files = list(Path(".").glob("test_result_*.json"))
    
    if individual_files:
        print(f"\n📁 {len(individual_files)}개의 개별 결과 파일을 results/ 폴더로 이동합니다.")
        
        for file in individual_files:
            try:
                target_path = results_dir / file.name
                file.rename(target_path)
                print(f"  ✅ {file.name} → results/{file.name}")
            except Exception as e:
                print(f"  ❌ {file.name} 이동 실패: {e}")

async def main():
    """메인 실행 함수"""
    print("🔧 테스트 쿼리 전송기 시작")
    
    sender = TestQuerySender(
        api_url="http://localhost:8000/api/v1/chat",
        test_case_file="test_case.json",
        output_file="test_results.json",
        max_concurrent=3  # 동시 요청 수 제한
    )
    
    try:
        # 테스트 실행
        results = await sender.run_tests()
        
        # 결과 저장
        await sender.save_results()
        
        # 요약 출력
        sender.print_summary()
        
        # 개별 파일들 정리
        await cleanup_individual_files()
        
        print(f"\n🎉 모든 테스트가 완료되었습니다!")
        print(f"📄 통합 결과: test_results.json")
        print(f"📁 개별 결과: results/ 폴더")
        
    except KeyboardInterrupt:
        print("\n⏹️ 사용자에 의해 중단되었습니다.")
        await cleanup_individual_files()  # 중단되어도 정리
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        await cleanup_individual_files()  # 오류가 발생해도 정리

if __name__ == "__main__":
    asyncio.run(main())
