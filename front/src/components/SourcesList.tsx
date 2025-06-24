import { ExternalLink } from "lucide-react";
import { Source } from "@/lib/api";

interface SourcesListProps {
  sources: Source[];
}

const SourcesList = ({ sources }: SourcesListProps) => {
  if (!sources || sources.length === 0) {
    return null;
  }

  return (
    <div className="mt-4 p-3 bg-gray-50 rounded-lg border-l-4 border-blue-500">
      <h4 className="text-sm font-semibold text-gray-700 mb-2">📚 참고 자료</h4>
      <div className="space-y-2">
        {sources.map((source, index) => (
          <div key={index} className="flex items-start space-x-2">
            <ExternalLink className="w-3 h-3 text-blue-500 mt-1 flex-shrink-0" />
            <a
              href={source.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-blue-600 hover:text-blue-800 hover:underline line-clamp-2"
              title={source.title}
            >
              {source.title}
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SourcesList; 