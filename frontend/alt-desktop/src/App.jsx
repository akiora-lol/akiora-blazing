import React from 'react';
import LoginPage from './LoginPage';

function App() {
  const handleLoginSuccess = (userData, redirectPath) => {
    console.log('Login successful:', userData);
    // Здесь можно обновить состояние приложения
    // и перенаправить пользователя
    window.location.href = redirectPath;
  };
  
  return <LoginPage onLoginSuccess={handleLoginSuccess} />;
}

export default App;
