import React, { useState } from 'react';
import { createTask as apiCreateTask } from '@/lib/api';
import { Task } from '@/lib/types';

interface AddTaskFormProps {
  userId: number;
  onTaskAdded: (task: Task) => void;
  onShowMessage: (message: string, type: 'success' | 'error') => void;
}

const IconSpinner = () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="animate-spin"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>;

const AddTaskForm: React.FC<AddTaskFormProps> = ({ userId, onTaskAdded, onShowMessage }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) {
      onShowMessage('Task title cannot be empty.', 'error');
      return;
    }

    setLoading(true);
    try {
      const newTask = await apiCreateTask(userId, title, description);
      onTaskAdded(newTask);
      onShowMessage('Task added successfully!', 'success');
      setTitle('');
      setDescription('');
    } catch (error) {
      onShowMessage(`Failed to add task: ${error instanceof Error ? error.message : String(error)}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white shadow-md rounded-lg p-6 mb-6">
      <h2 className="mb-4 text-xl font-semibold text-gray-700">Add a new task</h2>
      <div className="space-y-4">
        <input
          type="text"
          placeholder="Task title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
          required
          disabled={loading}
        />
        <textarea
          placeholder="Task description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg h-24 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
          disabled={loading}
        />
        <button
          type="submit"
          className="w-full px-6 py-2 font-bold text-white bg-green-500 rounded-lg hover:bg-green-600 disabled:bg-green-400 transition-colors duration-200 flex items-center justify-center"
          disabled={loading}
        >
          {loading ? <IconSpinner /> : 'Add Task'}
        </button>
      </div>
    </form>
  );
};

export default AddTaskForm;
