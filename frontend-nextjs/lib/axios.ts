// lib/axios.ts

import axios from 'axios';

const axiosClient = axios.create({
    // URL dasar untuk semua request API ke backend Laravel Anda
    baseURL: 'http://localhost:8000',
    // Mengizinkan pengiriman cookie antar domain (localhost:3000 -> localhost:8000)
    withCredentials: true,
    headers: {
        'X-Requested-With': 'XMLHttpRequest',
    },
});

export default axiosClient;