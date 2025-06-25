import { TrendingUp, ExternalLink } from "lucide-react";

const RelatedProducts = () => {
  const relatedPosts = [
    {
      title: "이달의 가성비 좋은 키보드",
      description: "10만원 이하 기계식 키보드 5종 비교",
      views: "2.3k",
      date: "2일 전"
    },
    {
      title: "게이밍 마우스 추천 TOP 5",
      description: "프로게이머들이 선택한 마우스",
      views: "1.8k", 
      date: "1주 전"
    },
    {
      title: "노트북 구매 가이드 2024",
      description: "용도별 노트북 추천 리스트",
      views: "4.1k",
      date: "3일 전"
    }
  ];

  return (
    <div className="w-80 bg-white border-l border-gray-200 p-6 overflow-y-auto">
      {/* 연관 제품 추천 섹션 */}
      <div className="mb-8">
        <div className="flex items-center space-x-2 mb-6">
          <TrendingUp className="w-5 h-5 text-blue-600" />
          <h2 className="text-lg font-semibold text-gray-900">연관 제품 추천</h2>
        </div>
        
        <div className="space-y-4">
          {relatedPosts.map((post, index) => (
            <div 
              key={index}
              className="p-4 rounded-lg border border-gray-100 hover:border-blue-200 hover:bg-blue-50/50 transition-all duration-200 cursor-pointer group"
            >
              <div className="flex items-start justify-between mb-2">
                <h3 className="font-medium text-gray-900 text-sm group-hover:text-blue-700 transition-colors">
                  {post.title}
                </h3>
                <ExternalLink className="w-4 h-4 text-gray-400 group-hover:text-blue-600 transition-colors flex-shrink-0 ml-2" />
              </div>
              <p className="text-xs text-gray-600 mb-3">{post.description}</p>
              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>{post.views} 조회</span>
                <span>{post.date}</span>
              </div>
            </div>
          ))}
        </div>
        
        {/* 자세히 보기 버튼 */}
        <div className="mt-4 text-center">
          <button className="text-sm text-blue-600 hover:text-blue-700 font-medium transition-colors">
            자세히 보기 →
          </button>
        </div>
      </div>
    </div>
  );
};

export default RelatedProducts;
