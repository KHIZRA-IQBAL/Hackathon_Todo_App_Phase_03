'use client'

import { useEffect, useState, useMemo, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { getAuthToken, getUserFromServer, logout } from '@/lib/auth'
import { getTasks, createTask, updateTask, deleteTask, toggleComplete } from '@/lib/api'

import { User, Task } from '@/lib/types'

// Import the new components
import Header from '@/components/Header'
import AddTaskForm from '@/components/AddTaskForm'
import TaskList from '@/components/TaskList'
import EditModal from '@/components/EditModal'
import ChatWidget from '@/components/ChatWidget'
import { IconSpinner } from '@/components/Icons'

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');
  const [loadingTasks, setLoadingTasks] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  const router = useRouter();

  const handleShowMessage = useCallback((message: string, type: 'success' | 'error') => {
    // In a real application, you'd integrate a toast notification library here (e.g., react-hot-toast)
    console.log(`Message (${type}): ${message}`);
    if (type === 'error') {
      setError(message);
    } else {
      // Simple success feedback, clear error
      setError(null);
    }
  }, []);

  useEffect(() => {
    const token = getAuthToken();
    if (!token) {
      router.push('/auth/signin');
      return;
    }

    const fetchUserAndTasks = async () => {
      try {
        setLoadingTasks(true);
        const currentUser = await getUserFromServer(token);
        if (!currentUser) {
          logout();
          router.push('/auth/signin');
          return;
        }
        setUser(currentUser);
        const userTasks = await getTasks(currentUser.id, filter);
        setTasks(userTasks);
        setError(null);
      } catch (err: any) {
        handleShowMessage(`Failed to load data: ${err.message || 'Unknown error'}`, 'error');
      } finally {
        setLoadingTasks(false);
      }
    };

    fetchUserAndTasks();
  }, [router, filter, handleShowMessage]);

  const handleTaskAdded = useCallback((newTask: Task) => {
    setTasks(prev => [newTask, ...prev]); // Add new tasks to the top
    handleShowMessage('Task added successfully!', 'success');
  }, [handleShowMessage]);

  const handleUpdateTask = useCallback(async (id: number, updates: Partial<Task>) => {
    if (!user) return;
    try {
      const existingTask = tasks.find(t => t.id === id);
      if (!existingTask) throw new Error('Task not found for update');

      const updatedTask = await updateTask(
        user.id,
        id,
        updates.title !== undefined ? updates.title : existingTask.title,
        updates.description !== undefined ? updates.description : existingTask.description || ''
      );
      setTasks(prev => prev.map(task => task.id === id ? updatedTask : task));
      handleShowMessage('Task updated successfully!', 'success');
    } catch (err: any) {
      handleShowMessage(`Failed to update task: ${err.message || 'Unknown error'}`, 'error');
    }
  }, [user, tasks, handleShowMessage]);

  const handleToggleComplete = useCallback(async (id: number) => {
    if (!user) return;
    try {
      const updatedTask = await toggleComplete(user.id, id);
      setTasks(prev => prev.map(task => task.id === id ? updatedTask : task));
      handleShowMessage('Task completion status updated!', 'success');
    } catch (err: any) {
      handleShowMessage(`Failed to toggle task completion: ${err.message || 'Unknown error'}`, 'error');
    }
  }, [user, handleShowMessage]);

  const handleSaveEdit = useCallback(async (id: number, updates: Partial<Task>) => {
    await handleUpdateTask(id, updates);
    setEditingTask(null);
  }, [handleUpdateTask]);

  const handleDeleteTask = useCallback(async (id: number) => {
    if (!user) return;
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(user.id, id);
        setTasks(prev => prev.filter(task => task.id !== id));
        handleShowMessage('Task deleted successfully!', 'success');
      } catch (err: any) {
        handleShowMessage(`Failed to delete task: ${err.message || 'Unknown error'}`, 'error');
      }
    }
  }, [user, handleShowMessage]);

  const handleLogout = useCallback(() => {
    logout();
    router.push('/auth/signin');
  }, [router]);

  const displayedTasks = useMemo(() => {
    if (filter === 'pending') return tasks.filter(t => !t.completed);
    if (filter === 'completed') return tasks.filter(t => t.completed);
    return tasks;
  }, [tasks, filter]);

  if (!user) {
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <IconSpinner />
            <p className="ml-2 text-gray-700">Loading user data...</p>
        </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header user={user} onLogout={handleLogout} />
      <main className="container mx-auto p-4 sm:p-6 lg:p-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column: Task Management */}
          <div className="flex flex-col gap-6">
            <AddTaskForm 
                userId={user.id} 
                onTaskAdded={handleTaskAdded} 
                onShowMessage={handleShowMessage}
            />

            <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center gap-2 mb-4 border-b pb-2">
                    {(['all', 'pending', 'completed'] as const).map(f => (
                        <button 
                            key={f} 
                            onClick={() => setFilter(f)}
                            className={`px-4 py-2 rounded-lg text-sm font-semibold transition-colors duration-200 ${
                                filter === f 
                                ? 'bg-blue-500 text-white' 
                                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                            }`}
                        >
                            {f.charAt(0).toUpperCase() + f.slice(1)}
                        </button>
                    ))}
                </div>

                <TaskList
                  tasks={displayedTasks}
                  onUpdate={handleUpdateTask}
                  onDelete={handleDeleteTask}
                  onToggle={handleToggleComplete}
                  onEdit={setEditingTask}
                  loading={loadingTasks}
                />
            </div>
          </div>

          {/* Right Column: AI Chat */}
          <div>
            <ChatWidget token={getAuthToken()} />
          </div>
        </div>
      </main>

      {editingTask && (
        <EditModal 
            task={editingTask} 
            onSave={handleSaveEdit} 
            onCancel={() => setEditingTask(null)}
        />
      )}
    </div>
  )
}