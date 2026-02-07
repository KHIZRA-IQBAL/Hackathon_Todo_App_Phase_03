import React, { useState, useEffect } from 'react';
import { Task } from '@/lib/types';
import { IconSpinner } from './Icons'; // Assuming IconSpinner is in Icons.tsx

interface EditModalProps {
    task: Task;
    onSave: (id: number, updates: Partial<Task>) => Promise<void>;
    onCancel: () => void;
    loading?: boolean;
}

const EditModal: React.FC<EditModalProps> = ({ task, onSave, onCancel, loading = false }) => {
    const [title, setTitle] = useState(task.title);
    const [description, setDescription] = useState(task.description || '');

    useEffect(() => {
        setTitle(task.title);
        setDescription(task.description || '');
    }, [task]);

    const handleSaveClick = async () => {
        await onSave(task.id, { title, description });
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md">
                <h3 className="text-lg font-semibold mb-4 text-gray-800">Edit Task</h3>
                <div className="space-y-4">
                    <input
                        type="text"
                        value={title}
                        onChange={e => setTitle(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                        disabled={loading}
                        aria-label="Task title"
                    />
                    <textarea
                        value={description}
                        onChange={e => setDescription(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                        rows={4}
                        disabled={loading}
                        aria-label="Task description"
                    />
                </div>
                <div className="flex justify-end mt-6 space-x-2">
                    <button
                        onClick={onCancel}
                        className="px-4 py-2 text-gray-600 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors duration-200 disabled:opacity-50"
                        disabled={loading}
                    >
                        Cancel
                    </button>
                    <button
                        onClick={handleSaveClick}
                        className="px-4 py-2 font-bold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50 flex items-center justify-center"
                        disabled={loading}
                    >
                        {loading ? <IconSpinner /> : 'Save Changes'}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default EditModal;