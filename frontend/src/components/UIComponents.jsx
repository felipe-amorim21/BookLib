import React from 'react';

// Button Component
export const Button = ({ children, variant = 'primary', ...props }) => {
  const baseStyle = 'py-2 px-4 rounded focus:outline-none focus:ring';
  const variantStyle = variant === 'link' ? 'text-blue-600 hover:text-blue-800' : 'bg-blue-600 text-white';

  return (
    <button className={`${baseStyle} ${variantStyle}`} {...props}>
      {children}
    </button>
  );
};

// Card Component
export const Card = ({ children, ...props }) => {
  return <div className="bg-white shadow-md rounded-lg" {...props}>{children}</div>;
};

// CardHeader Component
export const CardHeader = ({ children }) => {
  return <div className="p-4 border-b">{children}</div>;
};

// CardTitle Component
export const CardTitle = ({ children }) => {
  return <h2 className="font-bold text-lg">{children}</h2>;
};

// CardDescription Component
export const CardDescription = ({ children }) => {
  return <p className="text-gray-500">{children}</p>;
};

// CardContent Component
export const CardContent = ({ children }) => {
  return <div className="p-4">{children}</div>;
};

// CardFooter Component
export const CardFooter = ({ children }) => {
  return <div className="p-4 border-t">{children}</div>;
};

// Label Component
export const Label = ({ children, htmlFor }) => {
  return <label htmlFor={htmlFor} className="block text-sm font-medium text-gray-700">{children}</label>;
};

// Input Component
export const Input = React.forwardRef(({ className, ...props }, ref) => {
  return (
    <input
      ref={ref}
      className={`block w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-opacity-50 ${className}`}
      {...props}
    />
  );
});

// Alert Component
export const Alert = ({ children, variant = 'info' }) => {
  const variantStyle = variant === 'destructive' ? 'bg-red-100 border-red-500 text-red-600' : 'bg-blue-100 border-blue-500 text-blue-600';
  return (
    <div className={`border-l-4 ${variantStyle} p-4`} role="alert">
      {children}
    </div>
  );
};

// AlertDescription Component
export const AlertDescription = ({ children }) => {
  return <span className="ml-2">{children}</span>;
};
