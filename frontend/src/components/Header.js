import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/Auth';

function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header style={styles.header}>
      <h1 style={styles.title}>Vim Game</h1>
      <div style={styles.userInfo}>
        {user ? (
          <>
            <span style={styles.username}>{user.username}</span>
            <button onClick={handleLogout} style={styles.button}>ログアウト</button>
          </>
        ) : (
          <button onClick={() => navigate('/login')} style={styles.button}>ログイン</button>
        )}
      </div>
    </header>
  );
}

const styles = {
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '1rem 2rem',
    backgroundColor: '#2c3e50',
    color: 'white',
  },
  title: {
    margin: 0,
    fontSize: '1.5rem',
  },
  userInfo: {
    display: 'flex',
    alignItems: 'center',
    gap: '1rem',
  },
  username: {
    fontSize: '1rem',
  },
  button: {
    padding: '0.5rem 1rem',
    backgroundColor: '#3498db',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '0.9rem',
    transition: 'background-color 0.2s',
    '&:hover': {
      backgroundColor: '#2980b9',
    },
  },
};

export default Header;
