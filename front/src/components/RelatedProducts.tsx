
import { TrendingUp, ExternalLink, Star, Clock, Users } from "lucide-react";

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

  const popularCategories = [
    { name: "노트북/PC", count: 152 },
    { name: "키보드/마우스", count: 89 },
    { name: "헤드폰/이어폰", count: 76 },
    { name: "스마트폰", count: 134 },
    { name: "모니터", count: 67 }
  ];

  const recentComparisons = [
    { product1: "아이폰 15", product2: "갤럭시 S24", time: "5분 전" },
    { product1: "맥북 에어", product2: "LG 그램", time: "12분 전" },
    { product1: "에어팟 프로", product2: "소니 WF-1000XM4", time: "18분 전" }
  ];

  return (
    <div className="w-80 bg-white border-l border-gray-200 p-6 overflow-y-auto">
      {/* 연관 제품 비교 섹션 */}
      <div className="mb-8">
        <div className="flex items-center space-x-2 mb-6">
          <TrendingUp className="w-5 h-5 text-blue-600" />
          <h2 className="text-lg font-semibold text-gray-900">연관 제품 비교</h2>
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
      </div>

      {/* 인기 카테고리 섹션 */}
      <div className="mb-8">
        <div className="flex items-center space-x-2 mb-4">
          <Star className="w-5 h-5 text-orange-500" />
          <h3 className="text-md font-semibold text-gray-900">인기 카테고리</h3>
        </div>
        
        <div className="space-y-2">
          {popularCategories.map((category, index) => (
            <div 
              key={index}
              className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
            >
              <span className="text-sm text-gray-700">{category.name}</span>
              <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                {category.count}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* 실시간 비교 현황 섹션 */}
      <div className="mb-6">
        <div className="flex items-center space-x-2 mb-4">
          <Clock className="w-5 h-5 text-green-500" />
          <h3 className="text-md font-semibold text-gray-900">실시간 비교</h3>
        </div>
        
        <div className="space-y-3">
          {recentComparisons.map((comparison, index) => (
            <div 
              key={index}
              className="p-3 rounded-lg bg-gray-50 hover:bg-gray-100 cursor-pointer transition-colors"
            >
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center space-x-2">
                  <Users className="w-3 h-3 text-gray-500" />
                  <span className="text-xs text-gray-500">{comparison.time}</span>
                </div>
              </div>
              <p className="text-sm text-gray-700">
                <span className="font-medium">{comparison.product1}</span>
                <span className="text-gray-400 mx-2">vs</span>
                <span className="font-medium">{comparison.product2}</span>
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* 더보기 버튼 */}
      <div className="pt-4 border-t border-gray-200">
        <button className="w-full text-sm text-blue-600 hover:text-blue-700 font-medium transition-colors">
          더 많은 비교 보기 →
        </button>
      </div>
    </div>
  );
};

export default RelatedProducts;
