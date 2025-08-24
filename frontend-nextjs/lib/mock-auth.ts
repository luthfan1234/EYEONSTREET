// lib/mock-auth.ts

export const mockLogin = async (credentials: { email: string, password: string }) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  // Mock validation
  if (credentials.email === 'test@example.com' && credentials.password === 'password') {
    return {
      id: 1,
      name: 'Test User',
      email: 'test@example.com',
      email_verified_at: new Date().toISOString(),
    };
  } else {
    throw new Error('Invalid credentials');
  }
};

export const mockUser = {
  id: 1,
  name: 'Test User',
  email: 'test@example.com',
  email_verified_at: new Date().toISOString(),
};
