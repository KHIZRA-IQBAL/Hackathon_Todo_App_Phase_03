export interface User {
    id: number;
    email: string;
    full_name?: string;
  }
  
  export enum TaskPriority {
    LOW = "Low",
    MEDIUM = "Medium",
    HIGH = "High",
  }
  
  export interface Category {
    id: number;
    name: string;
  }
  
  export interface Task {
    id: number;
    title: string;
    description?: string;
    completed: boolean;
    priority: TaskPriority;
    due_date?: string; // or Date if you prefer Date objects
    category_id?: number;
    category?: Category;
    created_at: string;
    updated_at: string;
    user_id: number;
  }
  