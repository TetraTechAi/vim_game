import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/Auth';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box
} from '@mui/material';

function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Vim Game
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {user ? (
            <>
              <Typography variant="body1">
                {user.username}
              </Typography>
              <Button color="inherit" onClick={handleLogout}>
                ログアウト
              </Button>
            </>
          ) : (
            <Button color="inherit" onClick={() => navigate('/login')}>
              ログイン
            </Button>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Header;
