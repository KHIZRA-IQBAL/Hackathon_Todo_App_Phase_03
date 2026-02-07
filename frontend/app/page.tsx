"use client";

import Link from 'next/link';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-purple-600 to-pink-500 flex flex-col text-white">

      {/* Header */}
      <header className="bg-white/10 backdrop-blur-md shadow-lg">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-white text-2xl font-bold">Todo App</h1>
          <nav>
            <Link href="/auth/signin" className="text-white hover:underline">
              Sign In
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1 flex items-center justify-center px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight">
            Organize Your Life with Todo App
          </h1>
          <p className="text-xl text-white/90 mb-8">
            Simple, fast, and secure task management.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Link href="/auth/signup" className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-4 rounded-xl font-semibold text-lg shadow-xl hover:shadow-2xl transform hover:scale-105 transition">
                Get Started
            </Link>
            <Link href="/auth/signin" className="bg-blue-500/20 backdrop-blur text-white border-2 border-white hover:bg-white/30 px-8 py-4 rounded-xl font-semibold text-lg shadow-xl hover:shadow-2xl transform hover:scale-105 transition">
                Sign In
            </Link>
          </div>
        </div>
      </main>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-white text-center mb-12">
            Why you&apos;ll love our Todo App
          </h2>
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {/* Feature 1 */}
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 text-center hover:bg-white/20 transition transform hover:scale-105">
              <span className="text-4xl mb-4 inline-block">✓</span>
              <h3 className="text-xl font-bold text-white mb-3">Easy Task Management</h3>
              <p className="text-white/80">A simple and intuitive interface to manage your tasks effortlessly.</p>
            </div>
            {/* Feature 2 */}
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 text-center hover:bg-white/20 transition transform hover:scale-105">
              <span className="text-4xl mb-4 inline-block">🔒</span>
              <h3 className="text-xl font-bold text-white mb-3">Secure Authentication</h3>
              <p className="text-white/80">Your data is safe with our robust authentication system.</p>
            </div>
            {/* Feature 3 */}
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 text-center hover:bg-white/20 transition transform hover:scale-105">
              <span className="text-4xl mb-4 inline-block">🖼️</span>
              <h3 className="text-xl font-bold text-white mb-3">Clean Interface</h3>
              <p className="text-white/80">A beautiful and clean UI that helps you focus on what matters.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 text-center text-white/80">
        <p>Phase 2 Hackathon Project</p>
      </footer>
    </div>
  );
};

export default LandingPage;
