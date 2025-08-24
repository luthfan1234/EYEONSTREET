// hooks/usePolling.ts

import { useState, useEffect } from 'react';

// Tipe generic 'T' memungkinkan hook ini digunakan untuk data apa pun
export function usePolling<T>(url: string, interval: number = 5000) {
  const [data, setData] = useState<T[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`Gagal mengambil data: ${response.statusText}`);
        }
        const result = await response.json();
        setData(result);
      } catch (e) {
        setError(e instanceof Error ? e : new Error('Terjadi kesalahan'));
      } finally {
        // Hanya set loading ke false pada pengambilan data pertama kali
        if (isLoading) {
          setIsLoading(false);
        }
      }
    };

    // Panggil sekali saat pertama kali dimuat
    fetchData(); 

    // Atur interval untuk memanggil fetchData berulang kali
    const intervalId = setInterval(fetchData, interval);

    // Fungsi cleanup: Hentikan interval saat komponen tidak lagi digunakan
    // Ini sangat penting untuk mencegah memory leak!
    return () => clearInterval(intervalId);

  }, [url, interval, isLoading]); // Dependensi effect

  return { data, isLoading, error };
}
