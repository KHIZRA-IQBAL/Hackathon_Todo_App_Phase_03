import { jwtDecode } from 'jwt-decode';
import { User } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function login(email: string, password: string): Promise<string> {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
            username: email,
            password: password,
        }),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Login failed with no error message' }));
        throw new Error(errorData.detail || 'Login failed');
    }

    const data = await response.json();
    return data.access_token;
}

export function setAuthToken(token: string): void {
    localStorage.setItem('token', token);
}

export async function signup(email: string, password: string, fullName?: string): Promise<void> {
    const response = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, full_name: fullName }),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Signup failed with no error message' }));
        throw new Error(errorData.detail || 'Signup failed');
    }

    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    window.location.href = '/dashboard';
}

export function logout(): void {
    localStorage.removeItem('token');
}

export function getAuthToken(): string | null {
    if (typeof window === 'undefined') {
        return null;
    }
    return localStorage.getItem('token');
}

export async function getUserFromServer(token: string): Promise<User | null> {
    try {
        const response = await fetch(`${API_URL}/auth/me`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        if (!response.ok) {
            return null;
        }
        return await response.json();
    } catch (error) {
        return null;
    }
}

export function getUser(): User | null {
    const token = getAuthToken();
    if (!token) {
        return null;
    }

    try {
        const decoded: { sub: string } = jwtDecode(token);
        // We only have the ID in the token, we need to fetch the rest from the server
        // This part will be updated to use `getUserFromServer` in the component that needs user data.
        return { id: parseInt(decoded.sub), email: '' }; // The email is not in the token
    } catch (error) {
        return null;
    }
}
