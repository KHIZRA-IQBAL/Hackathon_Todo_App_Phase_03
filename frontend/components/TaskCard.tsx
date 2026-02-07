import React from 'react';
import { Task } from '@/lib/types';
import { IconPencil, IconTrash } from './Icons';

interface TaskCardProps {
  task: Task;
  onToggle: (taskId: number) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
  loading: boolean;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onToggle, onEdit, onDelete, loading }) => {
  return (
    <div className={`bg-white shadow-md rounded-lg p-4 mb-3 hover:shadow-lg transition flex items-start ${loading ? 'opacity-50' : ''}`}>
      <input
        type="checkbox"
        checked={task.completed}
        onChange={() => onToggle(task.id)}
        className="w-5 h-5 mr-3 mt-1 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
        disabled={loading}
      />
      <div className="flex-1">
        <p className={`font-semibold text-lg ${task.completed ? 'line-through text-gray-400' : 'text-gray-800'}`}>
          {task.title}
        </p>
        {task.description && (
          <p className={`text-gray-600 text-sm ${task.completed ? 'line-through' : ''}`}>
            {task.description}
          </p>
        )}
      </div>
      <div className="flex gap-2 items-center">
        <button
          onClick={() => onEdit(task)}
          className="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded-md text-sm font-semibold transition-colors disabled:opacity-50"
          disabled={loading}
          aria-label="Edit task"
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(task.id)}
          className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-md text-sm font-semibold transition-colors disabled:opacity-50"
          disabled={loading}
          aria-label="Delete task"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TaskCard;