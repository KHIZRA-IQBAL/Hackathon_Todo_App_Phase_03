import { User } from '@/lib/types'

interface HeaderProps {
  user: User | null
  onLogout: () => void
}

export default function Header({ user, onLogout }: HeaderProps) {
  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto py-4 px-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">Todo App</h1>
        {user && (
          <div className="flex items-center gap-4">
            <span className="text-xl font-semibold text-gray-700 hidden sm:block">Welcome, {user.full_name || user.email}</span>
            <button
              onClick={onLogout}
              className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg font-semibold transition-colors duration-200"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  )
}