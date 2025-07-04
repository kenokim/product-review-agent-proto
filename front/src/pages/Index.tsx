import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import ChatHeader from "@/components/ChatHeader";
import ChatInterface from "@/components/ChatInterface";
import RelatedProducts from "@/components/RelatedProducts";

const Index = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* 상단 헤더 */}
      <div className="bg-white border-b border-gray-200">
        <div className="px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-900">제품 추천 플랫폼</h1>
          <p className="text-sm text-gray-600">똑똑한 AI가 도와드리는 제품 추천 서비스</p>
        </div>
        
        {/* 탭 메뉴 */}
        <Tabs defaultValue="ai-compare" className="px-6">
          <TabsList className="grid w-full max-w-md grid-cols-2">
            <TabsTrigger value="ai-compare">AI 제품 추천</TabsTrigger>
            <TabsTrigger value="categories">카테고리</TabsTrigger>
          </TabsList>
          
          <TabsContent value="ai-compare" className="mt-0">
            <div className="flex h-[calc(100vh-180px)]">
              <div className="flex-1 flex flex-col">
                <ChatHeader />
                <ChatInterface />
              </div>
              
              {/* 항상 표시되는 사이드바 */}
              <div className="hidden lg:block">
                <RelatedProducts />
              </div>
            </div>
          </TabsContent>
          
          <TabsContent value="categories" className="mt-4">
            <div className="p-6 text-center text-gray-500">
              카테고리별 제품 추천이 여기에 표시됩니다.
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Index;
