// components/CCTVModal.tsx

'use client';

import { useMemo } from 'react';
import dynamic from 'next/dynamic';
import { CCTVData } from '@/types';

interface CCTVModalProps {
  isOpen: boolean;
  onClose: () => void;
  cctv: CCTVData | null;
}

const getStatusColor = (status: string) => {
    switch (status) {
        case 'online': return 'text-green-600';
        case 'offline': return 'text-red-600';
        case 'maintenance': return 'text-yellow-600';
        default: return 'text-gray-600';
    }
};

const CCTVModal: React.FC<CCTVModalProps> = ({ isOpen, onClose, cctv }) => {
  const CCTVPlayer = useMemo(() => dynamic(
    () => import('@/components/CCTVPlayer'),
    { ssr: false, loading: () => <div className="flex items-center justify-center h-64"><div className="text-sm text-gray-600">Loading player...</div></div> }
  ), []);

  if (!isOpen || !cctv) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-white rounded-lg shadow-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{cctv.name}</h3>
            <p className="text-sm text-gray-600">{cctv.location}</p>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 transition-colors">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div className="p-6">
          <div className="mb-6">
            <CCTVPlayer cctvId={cctv.id} />
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Status:</span>
              <span className={`font-medium capitalize ${getStatusColor(cctv.status)}`}>{cctv.status}</span>
            </div>
            
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Description:</span>
              <span className="text-gray-900">{cctv.description}</span>
            </div>
            
            {cctv.lastIncident && (
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">Last incident:</span>
                <span className="text-gray-900">{cctv.lastIncident}</span>
              </div>
            )}
            
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Camera ID:</span>
              <span className="text-gray-900 font-mono">{cctv.id}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CCTVModal;