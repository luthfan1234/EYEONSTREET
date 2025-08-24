// app/cctv/page.tsx

'use client';

import { useState } from 'react';
import { CCTVData } from '@/types';
import CCTVCard from '@/components/CCTVCard';
import CCTVModal from '@/components/CCTVModal';
import Link from 'next/link';

export default function CctvListPage() {
  const [selectedCCTV, setSelectedCCTV] = useState<CCTVData | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const cctvList: CCTVData[] = [
    { id: 'Agas', name: 'CCTV Agas', location: 'Simpang Agas', description: 'Monitoring lalu lintas di simpang Agas.', status: 'online' },
    { id: 'BalaiKota', name: 'CCTV Balai Kota', location: 'Area Balai Kota Surakarta', description: 'Pemantauan keamanan di sekitar kantor Walikota.', status: 'online' },
    { id: 'Balapan01', name: 'CCTV Stasiun Balapan', location: 'Pintu Masuk Stasiun Balapan', description: 'Monitoring area pintu masuk stasiun kereta.', status: 'online' },
    { id: 'Banjarsari', name: 'CCTV Banjarsari', location: 'Area Kecamatan Banjarsari', description: 'Pemantauan area publik Banjarsari.', status: 'online' },
    { id: 'Baron', name: 'CCTV Baron', location: 'Simpang Baron', description: 'Monitoring lalu lintas di simpang Baron.', status: 'online' },
    { id: 'Gladag', name: 'CCTV Bundaran Gladag', location: 'Bundaran Gladag', description: 'Pemantauan area ikonik Bundaran Gladag.', status: 'online' },
    { id: 'JembatanTirtonadi', name: 'CCTV Jembatan Tirtonadi', location: 'Jembatan Tirtonadi', description: 'Monitoring kondisi jembatan dan sekitarnya.', status: 'online' },
    { id: 'FlyoverTimur', name: 'CCTV Flyover Purwosari', location: 'Sisi Timur Flyover Purwosari', description: 'Pemantauan lalu lintas di flyover.', status: 'online' },
    { id: 'Brimob01', name: 'CCTV Mako Brimob', location: 'Area Mako Brimob', description: 'Pemantauan keamanan di markas Brimob.', status: 'maintenance' },
    { id: 'UNSTimur', name: 'CCTV UNS Timur', location: 'Gerbang Timur UNS', description: 'Monitoring area gerbang timur kampus UNS.', status: 'online' },
    { id: 'UNSBarat', name: 'CCTV UNS Barat', location: 'Gerbang Barat UNS', description: 'Monitoring area gerbang barat kampus UNS.', status: 'online' },
    { id: 'UNS', name: 'CCTV UNS Pusat', location: 'Area Pusat UNS', description: 'Pemantauan area utama kampus UNS.', status: 'online' },
    { id: 'Cembengan', name: 'CCTV Tugu Cembengan', location: 'Tugu Cembengan', description: 'Monitoring lalu lintas di Tugu Cembengan.', status: 'offline' },
    { id: 'Sriwedari01', name: 'CCTV Sriwedari', location: 'Area Taman Sriwedari', description: 'Pemantauan keamanan di Taman Sriwedari.', status: 'online' },
    { id: 'Singosaren', name: 'CCTV Singosaren', location: 'Simpang Singosaren', description: 'Monitoring pusat perbelanjaan Singosaren.', status: 'online' },
    { id: 'Sekarpace', name: 'CCTV Sekarpace', location: 'Simpang Sekarpace', description: 'Monitoring lalu lintas di simpang Sekarpace.', status: 'online' },
    { id: 'PasarNusukan', name: 'CCTV Pasar Nusukan', location: 'Area Pasar Nusukan', description: 'Monitoring aktivitas di Pasar Nusukan.', status: 'online' },
    { id: 'PasarKlewer', name: 'CCTV Pasar Klewer', location: 'Area Pasar Klewer', description: 'Pemantauan pusat grosir batik Klewer.', status: 'online' },
    { id: 'PasarKembang', name: 'CCTV Pasar Kembang', location: 'Area Pasar Kembang', description: 'Monitoring aktivitas di Pasar Kembang.', status: 'online' },
    { id: 'PasarGede', name: 'CCTV Pasar Gede', location: 'Pasar Gede Hardjonagoro', description: 'Monitoring keamanan area pasar.', status: 'maintenance' },
    { id: 'Panggung', name: 'CCTV Panggung', location: 'Simpang Panggung', description: 'Monitoring lalu lintas di simpang Panggung.', status: 'online' },
    { id: 'OverpassManahan', name: 'CCTV Overpass Manahan', location: 'Overpass Manahan', description: 'Pemantauan lalu lintas di overpass Manahan.', status: 'online' },
  ];

  const openModal = (cctv: CCTVData) => {
    setSelectedCCTV(cctv);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedCCTV(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Navigation Header */}
      <nav className="bg-white/80 backdrop-blur-sm border-b border-white/20 shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-8">
              <Link href="/landing" className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                </div>
                <span className="text-xl font-bold text-gray-900">EyeOnStreets</span>
              </Link>
              
              <div className="hidden md:flex items-center space-x-1">
                <Link href="/dashboard" className="text-gray-600 hover:text-gray-900 hover:bg-white/50 px-4 py-2 rounded-xl transition-colors text-sm font-medium">
                  Dashboard
                </Link>
                <Link href="/cctv" className="bg-blue-100 text-blue-600 px-4 py-2 rounded-xl font-semibold text-sm transition-colors">
                  CCTV Monitoring
                </Link>
                <Link href="/incidents" className="text-gray-600 hover:text-gray-900 hover:bg-white/50 px-4 py-2 rounded-xl transition-colors text-sm font-medium">
                  Incidents
                </Link>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="hidden md:flex items-center space-x-3 px-4 py-2 bg-white/50 rounded-xl">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-gray-700">Live Monitoring</span>
              </div>
              <Link href="/login" className="flex items-center space-x-2 text-gray-600 hover:text-red-600 hover:bg-red-50 px-4 py-2 rounded-xl transition-colors text-sm font-medium">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                <span>Logout</span>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Header Section */}
        <div className="mb-8">
          <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-8 border border-white/20 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-4xl font-bold text-gray-900 mb-3">CCTV Monitoring</h1>
                <p className="text-lg text-gray-600">Monitor live surveillance feeds across the city</p>
              </div>
              <div className="hidden lg:block">
                <div className="w-20 h-20 bg-gradient-to-r from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center">
                  <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white/60 backdrop-blur-sm border border-white/20 rounded-2xl p-6 text-center shadow-lg hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-gradient-to-r from-green-500 to-green-600 rounded-xl flex items-center justify-center mx-auto mb-3">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div className="text-2xl font-bold text-green-600">
              {cctvList.filter(c => c.status === 'online').length}
            </div>
            <div className="text-sm text-gray-600">Online Cameras</div>
          </div>
          <div className="bg-white/60 backdrop-blur-sm border border-white/20 rounded-2xl p-6 text-center shadow-lg hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-gradient-to-r from-yellow-500 to-yellow-600 rounded-xl flex items-center justify-center mx-auto mb-3">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="text-2xl font-bold text-yellow-600">
              {cctvList.filter(c => c.status === 'maintenance').length}
            </div>
            <div className="text-sm text-gray-600">Under Maintenance</div>
          </div>
          <div className="bg-white/60 backdrop-blur-sm border border-white/20 rounded-2xl p-6 text-center shadow-lg hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-gradient-to-r from-red-500 to-red-600 rounded-xl flex items-center justify-center mx-auto mb-3">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <div className="text-2xl font-bold text-red-600">
              {cctvList.filter(c => c.status === 'offline').length}
            </div>
            <div className="text-sm text-gray-600">Offline</div>
          </div>
          <div className="bg-white/60 backdrop-blur-sm border border-white/20 rounded-2xl p-6 text-center shadow-lg hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl flex items-center justify-center mx-auto mb-3">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div className="text-2xl font-bold text-gray-900">{cctvList.length}</div>
            <div className="text-sm text-gray-600">Total Cameras</div>
          </div>
        </div>

        {/* CCTV Grid */}
        <section className="bg-white/60 backdrop-blur-sm border border-white/20 rounded-2xl shadow-lg overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200/50 bg-gradient-to-r from-blue-50 to-indigo-50">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
              <h2 className="text-lg font-bold text-gray-900">Live Camera Feeds</h2>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span>Real-time monitoring active</span>
              </div>
            </div>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {cctvList.map((cctv) => (
                <CCTVCard key={cctv.id} cctv={cctv} onCardClick={openModal} />
              ))}
            </div>
          </div>
        </section>

        <CCTVModal isOpen={isModalOpen} onClose={closeModal} cctv={selectedCCTV} />
      </main>
    </div>
  );
}
