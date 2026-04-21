const buttonVariants = {
  default: 'bg-primary text-white hover:bg-primary/90 glow-red',
  secondary: 'bg-surface text-white border border-white/10 hover:bg-white/10',
  accent: 'bg-accent text-white hover:bg-accent/90 glow-cyan',
  outline: 'border-2 border-primary text-primary hover:bg-primary hover:text-white',
  ghost: 'text-white hover:bg-white/10',
  link: 'text-primary hover:underline'
}

const buttonSizes = {
  default: 'h-10 px-4 py-2',
  sm: 'h-9 px-3 text-sm',
  lg: 'h-12 px-8 text-lg',
  icon: 'h-10 w-10'
}

export { buttonVariants, buttonSizes }
