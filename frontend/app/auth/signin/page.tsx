'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { login, setAuthToken } from '@/lib/auth';

// Simple icon components for the form
const EyeIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
);
const EyeOffIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>
);
const IconSpinner = () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="animate-spin"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>;

const LogoPlaceholder = () => (
  <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-500 rounded-2xl mb-6 flex items-center justify-center">
    <div className="w-10 h-10 bg-white rounded-lg shadow-inner"></div>
  </div>
);


export default function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const router = useRouter();

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const token = await login(email, password);
      setAuthToken(token);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Failed to sign in. Please check your credentials.');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600 p-4">
      <div className="w-full max-w-md bg-white rounded-xl shadow-lg p-8 sm:p-12">
        <div className="flex justify-center mb-6">
          <LogoPlaceholder />
        </div>
        <h1 className="mb-4 text-3xl font-bold text-center text-gray-800">Welcome Back</h1>
        <p className="text-center text-gray-600 mb-8">Sign in to continue to your dashboard.</p>

        <form onSubmit={handleSignIn} className="space-y-6">
          <div>
            <label className="block mb-2 text-sm font-semibold text-gray-700">Email</label>
            <input
              type="email"
              className="w-full px-4 py-3 leading-tight text-gray-700 bg-gray-50 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="you@example.com"
            />
          </div>
          <div className="relative">
            <label className="block mb-2 text-sm font-semibold text-gray-700">Password</label>
            <input
              type={showPassword ? 'text' : 'password'}
              className="w-full px-4 py-3 pr-10 leading-tight text-gray-700 bg-gray-50 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="••••••••"
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute inset-y-0 right-0 top-1/2 -translate-y-1/2 transform flex items-center pr-3 text-gray-500 hover:text-gray-700"
              aria-label={showPassword ? 'Hide password' : 'Show password'}
            >
              {showPassword ? <EyeOffIcon /> : <EyeIcon />}
            </button>
          </div>

          {error && <p className="text-red-500 text-sm font-semibold">{error}</p>}

          <div>
            <button
              type="submit"
              disabled={loading}
              className="w-full px-6 py-3 font-bold text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:bg-blue-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 flex items-center justify-center"
            >
              {loading ? <IconSpinner /> : 'Sign In'}
            </button>
          </div>
        </form>

        <p className="mt-8 text-center text-gray-600">
          Don&apos;t have an account?{' '}
          <Link href="/auth/signup" className="font-semibold text-blue-600 hover:underline">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}