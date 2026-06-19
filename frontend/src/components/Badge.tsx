import { ReactNode } from 'react';
import { cn } from '../lib/utils';

interface BadgeProps {
  variant?: 'default' | 'success' | 'warning' | 'error' | 'outline';
  className?: string;
  children: ReactNode;
  dot?: boolean;
}

export function Badge({ variant = 'default', className, children, dot }: BadgeProps) {
  const variants = {
    default: 'bg-neutral-200 text-neutral-900',
    success: 'bg-accent-sage/20 text-accent-sage border border-accent-sage/30',
    warning: 'bg-accent-sand/20 text-accent-sand border border-accent-sand/30',
    error: 'bg-accent-rust/20 text-accent-rust border border-accent-rust/30',
    outline: 'border border-neutral-300 text-neutral-600',
  };

  return (
    <span className={cn('inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium', variants[variant], className)}>
      {dot && <span className={cn('h-1.5 w-1.5 rounded-full', {
        'bg-neutral-600': variant === 'default' || variant === 'outline',
        'bg-accent-sage': variant === 'success',
        'bg-accent-sand': variant === 'warning',
        'bg-accent-rust': variant === 'error',
      })} />}
      {children}
    </span>
  );
}
