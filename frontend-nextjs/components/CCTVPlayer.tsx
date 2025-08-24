'use client';

import React, { useEffect, useRef } from 'react';
import flvjs from 'flv.js';

interface CCTVPlayerProps {
  cctvId: string;
}

const CCTVPlayer: React.FC<CCTVPlayerProps> = ({ cctvId }) => {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    let flvPlayer: flvjs.Player | null = null;

    if (flvjs.isSupported() && videoRef.current) {
      flvPlayer = flvjs.createPlayer({
        type: 'flv',
        isLive: true,
        url: `https://surakarta.atcsindonesia.info:8086/camera/${cctvId}.flv`
      });

      flvPlayer.attachMediaElement(videoRef.current);
      
      const startPlayback = async () => {
        try {
          flvPlayer?.load();
          // Menambahkan penanganan error untuk mengabaikan 'AbortError'
          await flvPlayer?.play();
        } catch (error: any) {
          // Ini adalah cara untuk mengabaikan error interupsi yang tidak berbahaya
          if (error.name !== 'AbortError') {
            console.error(`Gagal memutar CCTV ${cctvId}:`, error);
          }
        }
      };

      startPlayback();
    }

    // Fungsi cleanup untuk menghancurkan player saat komponen tidak lagi digunakan
    return () => {
      if (flvPlayer) {
        flvPlayer.destroy();
      }
    };
  }, [cctvId]); // Efek ini akan berjalan ulang jika cctvId berubah

  return (
    <div className="bg-black rounded-lg shadow-lg overflow-hidden">
      <video 
        ref={videoRef} 
        className="w-full h-full" 
        controls 
        muted 
        autoPlay 
        playsInline // Atribut tambahan untuk kompatibilitas mobile
      />
      <p className="text-white text-center bg-gray-800 p-2 font-semibold">{cctvId}</p>
    </div>
  );
};

export default CCTVPlayer;
