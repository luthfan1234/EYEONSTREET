// types/index.ts

export interface Incident {
  id: number;
  cctv_id: string;
  type: string;
  image_path: string;
  created_at: string;
}

export interface CCTVData {
  id: string;
  name: string;
  location: string;
  description: string;
  status: 'online' | 'offline' | 'maintenance';
  lastIncident?: string;
}