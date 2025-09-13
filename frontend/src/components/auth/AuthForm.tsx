import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Button } from '../ui/Button';
import { Card, CardContent, CardHeader } from '../ui/Card';
import { useAuthStore } from '../../store/authStore';
import { isValidEmail, isValidPassword } from '../../lib/utils';
import toast from 'react-hot-toast';

interface AuthFormProps {
  mode: 'login' | 'register';
  onModeChange: (mode: 'login' | 'register') => void;
}

interface FormData {
  name?: string;
  email: string;
  password: string;
  confirmPassword?: string;
}

export const AuthForm: React.FC<AuthFormProps> = ({ mode, onModeChange }) => {
  const [isLoading, setIsLoading] = useState(false);
  const { login, register } = useAuthStore();
  
  const {
    register: registerForm,
    handleSubmit,
    formState: { errors },
    watch,
    reset,
  } = useForm<FormData>();

  const password = watch('password');

  const onSubmit = async (data: FormData) => {
    setIsLoading(true);
    try {
      if (mode === 'login') {
        await login(data.email, data.password);
        toast.success('Welcome back!');
      } else {
        if (data.password !== data.confirmPassword) {
          toast.error('Passwords do not match');
          return;
        }
        await register(data.name!, data.email, data.password);
        toast.success('Account created successfully!');
      }
    } catch (error) {
      toast.error(mode === 'login' ? 'Login failed' : 'Registration failed');
    } finally {
      setIsLoading(false);
    }
  };

  const switchMode = () => {
    reset();
    onModeChange(mode === 'login' ? 'register' : 'login');
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="text-center">
        <div className="flex items-center justify-center mb-4">
          <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center">
            <span className="text-2xl">♻️</span>
          </div>
        </div>
        <h2 className="text-2xl font-bold text-gray-900">
          {mode === 'login' ? 'Welcome Back' : 'Create Account'}
        </h2>
        <p className="text-gray-600 mt-2">
          {mode === 'login'
            ? 'Sign in to continue your waste-to-energy journey'
            : 'Join the AI-powered waste conversion revolution'}
        </p>
      </CardHeader>
      
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {mode === 'register' && (
            <div>
              <label className="label">Full Name</label>
              <input
                {...registerForm('name', {
                  required: 'Name is required',
                  minLength: {
                    value: 2,
                    message: 'Name must be at least 2 characters',
                  },
                })}
                type="text"
                className={`input ${errors.name ? 'input-error' : ''}`}
                placeholder="Enter your full name"
              />
              {errors.name && (
                <p className="text-danger-500 text-sm mt-1">{errors.name.message}</p>
              )}
            </div>
          )}

          <div>
            <label className="label">Email Address</label>
            <input
              {...registerForm('email', {
                required: 'Email is required',
                validate: (value) => isValidEmail(value) || 'Invalid email address',
              })}
              type="email"
              className={`input ${errors.email ? 'input-error' : ''}`}
              placeholder="Enter your email"
            />
            {errors.email && (
              <p className="text-danger-500 text-sm mt-1">{errors.email.message}</p>
            )}
          </div>

          <div>
            <label className="label">Password</label>
            <input
              {...registerForm('password', {
                required: 'Password is required',
                validate: (value) => isValidPassword(value) || 'Password must be at least 8 characters with uppercase, lowercase, and number',
              })}
              type="password"
              className={`input ${errors.password ? 'input-error' : ''}`}
              placeholder="Enter your password"
            />
            {errors.password && (
              <p className="text-danger-500 text-sm mt-1">{errors.password.message}</p>
            )}
          </div>

          {mode === 'register' && (
            <div>
              <label className="label">Confirm Password</label>
              <input
                {...registerForm('confirmPassword', {
                  required: 'Please confirm your password',
                  validate: (value) => value === password || 'Passwords do not match',
                })}
                type="password"
                className={`input ${errors.confirmPassword ? 'input-error' : ''}`}
                placeholder="Confirm your password"
              />
              {errors.confirmPassword && (
                <p className="text-danger-500 text-sm mt-1">{errors.confirmPassword.message}</p>
              )}
            </div>
          )}

          <Button
            type="submit"
            className="w-full"
            size="lg"
            loading={isLoading}
          >
            {mode === 'login' ? 'Sign In' : 'Create Account'}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-600">
            {mode === 'login' ? "Don't have an account?" : 'Already have an account?'}
            <button
              type="button"
              onClick={switchMode}
              className="ml-2 text-primary-600 hover:text-primary-700 font-medium"
            >
              {mode === 'login' ? 'Sign up' : 'Sign in'}
            </button>
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

