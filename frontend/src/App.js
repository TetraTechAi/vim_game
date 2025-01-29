import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
import { SettingsProvider } from './contexts/Settings';

// Pages
import Menu from './pages/Menu';
import Game from './pages/Game';
import Result from './pages/Result';
import Login from './pages/Login';
import Register from './pages/Register';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#66bb6a',
    },
    secondary: {
      main: '#f50057',
    },
  },
});

function PrivateRoute({ children }) {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <SettingsProvider>
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/menu" element={
              <PrivateRoute>
                <Menu />
              </PrivateRoute>
            } />
            <Route path="/game/:level" element={
              <PrivateRoute>
                <Game />
              </PrivateRoute>
            } />
            <Route path="/result" element={
              <PrivateRoute>
                <Result />
              </PrivateRoute>
            } />
            <Route path="/" element={<Navigate to="/menu" replace />} />
          </Routes>
        </Router>
      </SettingsProvider>
    </ThemeProvider>
  );
}

export default App;
