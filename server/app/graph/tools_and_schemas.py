from typing import List, Dict, Any, Union, Optional
from pydantic import BaseModel, Field, field_validator
import json

# ========== 구조화된 출력 스키마 ==========

class ValidationResult(BaseModel):
    """요청 검증 결과 스키마"""
    is_specific: bool = Field(description="요청이 구체적인지 여부")
    clarification_question: str = Field(default="", description="구체화를 위한 질문")
    extracted_requirements: Optional[Dict[str, Any]] = Field(default_factory=dict, description="추출된 요구사항")
    
    @field_validator('extracted_requirements', mode='before')
    @classmethod
    def parse_requirements(cls, v):
        """문자열로 된 JSON을 딕셔너리로 파싱"""
        if v is None:
            return {}
        if isinstance(v, str):
            if not v.strip():
                return {}
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # JSON 파싱에 실패하면 기본 딕셔너리 반환
                return {"raw_text": v}
        return v if isinstance(v, dict) else {}

class SearchQueryResult(BaseModel):
    """검색어 생성 결과 스키마"""
    queries: List[str] = Field(description="생성된 검색어 목록")
    rationale: str = Field(description="검색어 선택 이유")

class ReflectionResult(BaseModel):
    """검색 결과 평가 스키마"""
    is_sufficient: bool = Field(description="현재 결과가 충분한지 여부")
    additional_queries: List[str] = Field(description="추가 검색어 목록")
    gap_analysis: str = Field(description="부족한 부분 분석")

class AnswerValidationResult(BaseModel):
    """답변 검증 결과 스키마"""
    is_valid: bool = Field(description="답변이 적절한지 여부 (true/false)")
    reason: str = Field(description="검증 결과의 간단한 이유")

# ========== 도구 함수 ==========

def validate_schema_result(result, schema_name: str) -> bool:
    """스키마 결과 검증 함수"""
    try:
        if schema_name == "ValidationResult":
            return hasattr(result, 'is_specific') and hasattr(result, 'clarification_question')
        elif schema_name == "SearchQueryResult":
            return hasattr(result, 'queries') and hasattr(result, 'rationale')
        elif schema_name == "ReflectionResult":
            return hasattr(result, 'is_sufficient') and hasattr(result, 'additional_queries')
        elif schema_name == "AnswerValidationResult":
            return hasattr(result, 'is_valid') and hasattr(result, 'reason')
        return False
    except Exception:
        return False
