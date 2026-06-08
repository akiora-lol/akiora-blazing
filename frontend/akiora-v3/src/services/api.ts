import axios from 'axios';
import { type User } from '@/types/user.js';
export interface AuthResponse {
    authenticated: boolean;
    user: User | null;
}

export interface LoginCredentials {
    provider: 'yandex' | 'discord' | 'google';
}

const api = axios.create({
    baseURL: 'http://localhost/api', // process.env.REACT_APP_API_URL ||
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    },
});


api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            console.log('Неавторизован');
        }
        return Promise.reject(error);
    }
);

export const authApi = {

    getMe: async (): Promise<AuthResponse> => {
        const { data } = await api.get<AuthResponse>('/auth/me');
        return data;
    },

    // Логаут
    logout: async (): Promise<void> => {
        await api.post('/auth/logout');
    },

    // Получение URL для редиректа (опционально)
    getLoginUrl: (provider: string): string => {
        return `${api.defaults.baseURL}/auth/${provider}/login`;
    },
};

export default api;
