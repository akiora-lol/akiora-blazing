import { useState } from 'react';
import { 
  MdMail, 
  MdArrowBack, 
  MdArrowForward, 
  MdSend,
  MdCheckCircle,
  MdErrorOutline
} from 'react-icons/md';
import { FaDiscord } from 'react-icons/fa';
import { SiYandexcloud } from 'react-icons/si';

// Конфигурация API
const AUTH_BASE = "http://localhost:8000";

const API = {
  getOAuthUrl: (provider) => `${AUTH_BASE}/${provider}/login`,
  
  async loginEmailStart(email) {
    const res = await fetch(`${AUTH_BASE}/email/login/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email })
    });
    
    if (!res.ok) {
      const error = await res.text();
      throw new Error(error || 'Failed to send code');
    }
    return res.json();
  },
  
  async loginEmailFinish(code) {
    const res = await fetch(`${AUTH_BASE}/email/login/finish`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ code })
    });
    
    if (!res.ok) {
      const error = await res.text();
      throw new Error(error || 'Invalid code');
    }
    return res.json();
  }
};

function LoginPage({ onLoginSuccess }) {
  const [step, setStep] = useState('providers');
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleOAuth = (provider) => {
    window.location.href = API.getOAuthUrl(provider);
  };
  
  const handleEmailSubmit = async () => {
    if (!email) return;
    
    setLoading(true);
    setError('');
    try {
      await API.loginEmailStart(email);
      setStep('code-input');
      setSuccess('Check your email for the verification code');
      setTimeout(() => setSuccess(''), 5000);
    } catch (err) {
      setError(err.message || 'Failed to send code');
      setTimeout(() => setError(''), 5000);
    } finally {
      setLoading(false);
    }
  };
  
  const handleCodeSubmit = async () => {
    if (code.length !== 6) return;
    
    setLoading(true);
    setError('');
    try {
      const data = await API.loginEmailFinish(code);
      const onboarded = localStorage.getItem('akiora_onboarded');
      if (onLoginSuccess) {
        onLoginSuccess(data, onboarded ? '/about' : '/onboarding');
      }
    } catch (err) {
      setError(err.message || 'Invalid code');
      setTimeout(() => setError(''), 5000);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      {/* Анимированные фоновые элементы */}
      <div style={styles.glowTop} />
      <div style={styles.glowBottom} />
      
      <div style={styles.card}>
        {/* Логотип */}
        <div style={styles.logoContainer}>
          <img src="/violet-yang.svg" alt="Akiora" style={styles.logo} />
        </div>
        
        <h2 style={styles.title}>Sign In</h2>
        <p style={styles.subtitle}>CHOOSE YOUR PREFERRED METHOD</p>
        
        <div style={styles.divider} />
        
        {/* Step: Providers */}
        {step === 'providers' && (
          <div style={styles.stepContainer}>
            <button
              style={styles.providerButton}
              onClick={() => setStep('email-input')}
              disabled={loading}
            >
              <MdMail size={20} color="#06B6D4" />
              <span>Continue with Email</span>
            </button>
            
            <div style={styles.orDivider}>
              <span style={styles.orText}>OR</span>
            </div>
            
            <button
              style={{...styles.providerButton, ...styles.discordButton}}
              onClick={() => handleOAuth('discord')}
              disabled={loading}
            >
              <FaDiscord size={20} color="#5865F2" />
              <span>Continue with Discord</span>
            </button>
            
            <button
              style={{...styles.providerButton, ...styles.yandexButton}}
              onClick={() => handleOAuth('yandex')}
              disabled={loading}
            >
              <SiYandexcloud size={20} color="#FC3F1D" />
              <span>Continue with Yandex</span>
            </button>
          </div>
        )}
        
        {/* Step: Email Input */}
        {step === 'email-input' && (
          <div style={styles.stepContainer}>
            <input
              type="email"
              style={styles.input}
              placeholder="your@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && email && handleEmailSubmit()}
              autoFocus
              disabled={loading}
            />
            <button
              style={styles.submitButton}
              onClick={handleEmailSubmit}
              disabled={!email || loading}
            >
              {loading ? 'Sending...' : 'Send Code'}
              <MdArrowForward size={16} />
            </button>
          </div>
        )}
        
        {/* Step: Code Input */}
        {step === 'code-input' && (
          <div style={styles.stepContainer}>
            <p style={styles.hint}>Check your inbox for the code</p>
            <input
              type="text"
              style={styles.input}
              placeholder="6-digit code"
              value={code}
              onChange={(e) => setCode(e.target.value.slice(0, 6))}
              onKeyPress={(e) => e.key === 'Enter' && code.length === 6 && handleCodeSubmit()}
              autoFocus
              disabled={loading}
            />
            <button
              style={styles.submitButton}
              onClick={handleCodeSubmit}
              disabled={code.length !== 6 || loading}
            >
              {loading ? 'Verifying...' : 'Verify'}
              <MdSend size={16} />
            </button>
          </div>
        )}
        
        {/* Сообщения */}
        {success && (
          <div style={styles.successMessage}>
            <MdCheckCircle size={16} />
            <span>{success}</span>
          </div>
        )}
        
        {error && (
          <div style={styles.errorMessage}>
            <MdErrorOutline size={16} />
            <span>{error}</span>
          </div>
        )}
        
        <div style={styles.divider} />
        
        {/* Back button */}
        <button
          style={styles.backButton}
          onClick={() => {
            if (step === 'providers') {
              window.location.href = '/';
            } else {
              setStep('providers');
              setEmail('');
              setCode('');
              setError('');
            }
          }}
        >
          <MdArrowBack size={12} />
          <span>Back</span>
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'radial-gradient(ellipse at 30% 40%, #1a0b2e 0%, #0a0414 100%)',
    position: 'relative',
    overflow: 'hidden',
    fontFamily: "'Chakra Petch', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
  },
  glowTop: {
    position: 'absolute',
    top: '10%',
    left: '-10%',
    width: '400px',
    height: '400px',
    borderRadius: '50%',
    background: 'radial-gradient(circle, rgba(166,0,255,0.15) 0%, transparent 70%)',
    filter: 'blur(60px)',
    animation: 'float 20s infinite ease-in-out',
  },
  glowBottom: {
    position: 'absolute',
    bottom: '10%',
    right: '-10%',
    width: '500px',
    height: '500px',
    borderRadius: '50%',
    background: 'radial-gradient(circle, rgba(106,0,255,0.12) 0%, transparent 70%)',
    filter: 'blur(80px)',
    animation: 'float 25s infinite reverse ease-in-out',
  },
  card: {
    position: 'relative',
    zIndex: 10,
    width: 'min(400px, calc(100vw - 48px))',
    padding: '44px 40px',
    backgroundColor: 'rgba(0, 0, 0, 0.82)',
    backdropFilter: 'blur(24px)',
    borderRadius: '18px',
    border: '1px solid rgba(166, 0, 255, 0.22)',
    boxShadow: '0 0 60px rgba(166, 0, 255, 0.12), 0 0 120px rgba(166, 0, 255, 0.06)',
    animation: 'riseUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) both',
    animationDelay: '0.1s',
  },
  logoContainer: {
    display: 'flex',
    justifyContent: 'center',
    marginBottom: '6px',
  },
  logo: {
    width: '48px',
    height: '48px',
    filter: 'drop-shadow(0 0 12px #a600ffaa)',
  },
  title: {
    fontFamily: "'Russo One', sans-serif",
    fontSize: '22px',
    color: '#fff',
    textAlign: 'center',
    margin: '0 0 2px',
    letterSpacing: '0.04em',
  },
  subtitle: {
    fontSize: '11px',
    color: 'rgba(255, 255, 255, 0.3)',
    textAlign: 'center',
    letterSpacing: '0.1em',
    margin: '0 0 16px',
  },
  divider: {
    height: '1px',
    background: 'rgba(255, 255, 255, 0.06)',
    margin: '16px 0',
  },
  stepContainer: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  providerButton: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    width: '100%',
    padding: '13px 18px',
    borderRadius: '10px',
    backgroundColor: 'rgba(255, 255, 255, 0.03)',
    border: '1px solid rgba(6, 182, 212, 0.3)',
    color: 'rgba(255, 255, 255, 0.75)',
    fontFamily: "'Chakra Petch', monospace",
    fontSize: '12px',
    letterSpacing: '0.1em',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
  },
  discordButton: {
    borderColor: 'rgba(88, 101, 242, 0.3)',
  },
  yandexButton: {
    borderColor: 'rgba(252, 63, 29, 0.3)',
  },
  orDivider: {
    position: 'relative',
    textAlign: 'center',
    margin: '4px 0',
  },
  orText: {
    fontSize: '10px',
    color: 'rgba(255, 255, 255, 0.2)',
    backgroundColor: 'rgba(0, 0, 0, 0.82)',
    padding: '0 10px',
  },
  input: {
    width: '100%',
    padding: '13px 18px',
    borderRadius: '10px',
    backgroundColor: 'rgba(255, 255, 255, 0.04)',
    border: '1px solid rgba(255, 255, 255, 0.12)',
    color: '#fff',
    fontFamily: "'Chakra Petch', monospace",
    fontSize: '13px',
    letterSpacing: '0.04em',
    outline: 'none',
    transition: 'border-color 0.18s',
    boxSizing: 'border-box',
  },
  submitButton: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
    width: '100%',
    padding: '13px 18px',
    borderRadius: '10px',
    background: 'linear-gradient(135deg, #a600ff, #7000cc)',
    border: '1px solid rgba(166, 0, 255, 0.7)',
    color: '#fff',
    fontFamily: "'Chakra Petch', monospace",
    fontSize: '12px',
    letterSpacing: '0.12em',
    cursor: 'pointer',
    transition: 'box-shadow 0.18s, transform 0.18s',
  },
  hint: {
    fontSize: '10px',
    color: '#06B6D4',
    textAlign: 'center',
    letterSpacing: '0.08em',
    margin: '0 0 8px',
  },
  successMessage: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
    marginTop: '12px',
    padding: '10px',
    borderRadius: '8px',
    backgroundColor: 'rgba(0, 255, 0, 0.1)',
    border: '1px solid rgba(0, 255, 0, 0.2)',
    fontSize: '11px',
    color: '#00ff88',
  },
  errorMessage: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
    marginTop: '12px',
    padding: '10px',
    borderRadius: '8px',
    backgroundColor: 'rgba(255, 0, 0, 0.1)',
    border: '1px solid rgba(255, 0, 0, 0.2)',
    fontSize: '11px',
    color: '#ff4466',
  },
  backButton: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '6px',
    width: '100%',
    background: 'none',
    border: 'none',
    color: 'rgba(255, 255, 255, 0.25)',
    fontFamily: "'Chakra Petch', monospace",
    fontSize: '10px',
    letterSpacing: '0.12em',
    textTransform: 'uppercase',
    cursor: 'pointer',
    padding: '6px 0 0',
    marginTop: '4px',
    transition: 'color 0.18s',
  },
};

// Добавляем CSS анимации
const styleSheet = document.createElement("style");
styleSheet.textContent = `
  @keyframes float {
    0%, 100% { transform: translate(0, 0) rotate(0deg); }
    33% { transform: translate(20px, -20px) rotate(5deg); }
    66% { transform: translate(-10px, 15px) rotate(-3deg); }
  }
  @keyframes riseUp {
    from { opacity: 0; transform: translateY(18px); }
    to { opacity: 1; transform: translateY(0); }
  }
  
  button:hover:not(:disabled) {
    transform: translateX(4px);
  }
  
  .provider-button:hover:not(:disabled) {
    background-color: rgba(255, 255, 255, 0.06);
    border-color: rgba(6, 182, 212, 0.8);
  }
  
  .submit-button:hover:not(:disabled) {
    box-shadow: 0 0 28px rgba(166, 0, 255, 0.45);
    transform: translateY(-1px);
  }
  
  input:focus {
    border-color: rgba(166, 0, 255, 0.5) !important;
  }
  
  input::placeholder {
    color: rgba(255, 255, 255, 0.2);
  }
  
  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }
`;
document.head.appendChild(styleSheet);

export default LoginPage;
