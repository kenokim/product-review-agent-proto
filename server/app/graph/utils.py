from typing import Any, Dict, List
from datetime import datetime


def get_current_date() -> str:
    """현재 날짜를 한국어 형식으로 반환"""
    return datetime.now().strftime("%Y-%m-%d")


def get_research_topic(messages: List[Dict[str, str]]) -> str:
    """
    메시지에서 연구 주제를 추출합니다.
    
    Args:
        messages: 메시지 리스트 (dict 형태)
        
    Returns:
        str: 연구 주제 문자열
    """
    if len(messages) == 1:
        return messages[-1].get("content", "")
    else:
        research_topic = ""
        for message in messages:
            role = message.get("role", "")
            content = message.get("content", "")
            if role == "user":
                research_topic += f"사용자: {content}\n"
            elif role == "assistant":
                research_topic += f"어시스턴트: {content}\n"
    return research_topic


def resolve_urls(urls_to_resolve: List[Any], session_id: int = 0) -> Dict[str, str]:
    """
    긴 URL을 짧은 형태로 변환하여 토큰 절약 및 시간 단축
    
    Args:
        urls_to_resolve: 변환할 URL들의 리스트
        session_id: 세션 고유 ID (기본값: 0)
        
    Returns:
        Dict[str, str]: 원본 URL -> 단축 URL 매핑
    """
    prefix = f"https://search.google.com/ref/"
    urls = []
    
    # URL 추출 (다양한 형태의 input 처리)
    for site in urls_to_resolve:
        if hasattr(site, 'web') and hasattr(site.web, 'uri'):
            urls.append(site.web.uri)
        elif isinstance(site, str):
            urls.append(site)
        elif isinstance(site, dict) and 'uri' in site:
            urls.append(site['uri'])

    # 각 고유 URL에 대해 단축 형태 생성
    resolved_map = {}
    for idx, url in enumerate(urls):
        if url not in resolved_map:
            resolved_map[url] = f"{prefix}{session_id}-{idx}"

    return resolved_map


def insert_citation_markers(text: str, citations_list: List[Dict]) -> str:
    """
    텍스트에 citation 마커를 삽입합니다.
    
    Args:
        text: 원본 텍스트
        citations_list: citation 정보가 담긴 리스트
        
    Returns:
        str: citation 마커가 삽입된 텍스트
    """
    # end_index 기준으로 내림차순 정렬 (뒤에서부터 삽입하여 인덱스 무결성 유지)
    sorted_citations = sorted(
        citations_list, 
        key=lambda c: (c.get("end_index", 0), c.get("start_index", 0)), 
        reverse=True
    )

    modified_text = text
    for citation_info in sorted_citations:
        end_idx = citation_info.get("end_index", 0)
        marker_to_insert = ""
        
        segments = citation_info.get("segments", [])
        for segment in segments:
            label = segment.get("label", "출처")
            short_url = segment.get("short_url", "#")
            marker_to_insert += f" [{label}]({short_url})"
        
        # 원본 end_idx 위치에 citation 마커 삽입
        modified_text = (
            modified_text[:end_idx] + marker_to_insert + modified_text[end_idx:]
        )

    return modified_text


def get_citations(response, resolved_urls_map: Dict[str, str]) -> List[Dict]:
    """
    Gemini 응답에서 citation 정보를 추출하고 포맷팅합니다.
    
    Args:
        response: Gemini 모델의 응답 객체
        resolved_urls_map: URL 매핑 딕셔너리
        
    Returns:
        List[Dict]: citation 정보 리스트
    """
    citations = []

    # 응답과 필수 구조체 확인
    if not response or not hasattr(response, 'candidates') or not response.candidates:
        return citations

    candidate = response.candidates[0]
    if (
        not hasattr(candidate, "grounding_metadata")
        or not candidate.grounding_metadata
        or not hasattr(candidate.grounding_metadata, "grounding_supports")
    ):
        return citations

    for support in candidate.grounding_metadata.grounding_supports:
        citation = {}

        # 세그먼트 정보 확인
        if not hasattr(support, "segment") or support.segment is None:
            continue

        start_index = (
            support.segment.start_index
            if hasattr(support.segment, 'start_index') and support.segment.start_index is not None
            else 0
        )

        # end_index가 없으면 건너뛰기
        if not hasattr(support.segment, 'end_index') or support.segment.end_index is None:
            continue

        citation["start_index"] = start_index
        citation["end_index"] = support.segment.end_index
        citation["segments"] = []

        # grounding chunk 정보 처리
        if (
            hasattr(support, "grounding_chunk_indices")
            and support.grounding_chunk_indices
        ):
            for ind in support.grounding_chunk_indices:
                try:
                    chunk = candidate.grounding_metadata.grounding_chunks[ind]
                    if hasattr(chunk, 'web') and chunk.web:
                        resolved_url = resolved_urls_map.get(chunk.web.uri, chunk.web.uri)
                        title = chunk.web.title if hasattr(chunk.web, 'title') else "출처"
                        
                        # 제목에서 확장자 제거
                        if "." in title:
                            title = title.split(".")[0]
                        
                        citation["segments"].append({
                            "label": title,
                            "short_url": resolved_url,
                            "value": chunk.web.uri,
                        })
                except (IndexError, AttributeError, KeyError) as e:
                    # 오류 발생 시 해당 세그먼트는 건너뛰기
                    print(f"Citation 처리 중 오류: {e}")
                    continue

        if citation["segments"]:  # 유효한 세그먼트가 있을 때만 추가
            citations.append(citation)

    return citations
