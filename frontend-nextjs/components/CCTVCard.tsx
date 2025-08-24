// components/CCTVCard.tsx

import { CCTVData } from "@/types";

interface CCTVCardProps {
  cctv: CCTVData;
  onCardClick: (cctv: CCTVData) => void;
}

const getStatusColor = (status: string) => {
    switch (status) {
        case 'online': return 'bg-green-500';
        case 'offline': return 'bg-red-500';
        case 'maintenance': return 'bg-yellow-500';
        default: return 'bg-gray-500';
    }
};

const CCTVCard: React.FC<CCTVCardProps> = ({ cctv, onCardClick }) => {
  return (
    <div
      className="bg-white border border-gray-200 rounded-lg hover:border-gray-300 transition-colors cursor-pointer"
      onClick={() => onCardClick(cctv)}
    >
      <div className="p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-medium text-gray-900 truncate">{cctv.name}</h3>
          <div className={`w-2 h-2 rounded-full ${getStatusColor(cctv.status)}`}></div>
        </div>
        <p className="text-xs text-gray-600 mb-2">{cctv.location}</p>
        <p className="text-xs text-gray-500 line-clamp-2">{cctv.description}</p>
        {cctv.lastIncident && (
          <p className="text-xs text-gray-500 mt-2 pt-2 border-t border-gray-100">
            Last incident: {cctv.lastIncident}
          </p>
        )}
      </div>
    </div>
  );
}

export default CCTVCard;