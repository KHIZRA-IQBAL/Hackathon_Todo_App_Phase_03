import React from 'react';
import TaskCard from './TaskCard';
import { Task } from '@/lib/types';

interface TaskListProps {
  tasks: Task[];
  onUpdate: (taskId: number, updates: Partial<Task>) => void;
  onDelete: (taskId: number) => void;
  onToggle: (taskId: number) => void;
  onEdit: (task: Task) => void;
  loading: boolean;
}

const IconSpinner = () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="animate-spin"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>;

const TaskList: React.FC<TaskListProps> = ({ tasks, onUpdate, onDelete, onToggle, onEdit, loading }) => {
  if (loading && tasks.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8">
        <IconSpinner />
        <p>Loading tasks...</p>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8">
        <p>No tasks yet. Add one above!</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map(task => (
        <TaskCard
          key={task.id}
          task={task}
          onToggle={onToggle}
          onEdit={onEdit}
          onDelete={onDelete}
          loading={loading}
        />
      ))}
    </div>
  );
};

export default TaskList;
