import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';

// Pages
import Menu from './pages/Menu';
import Game from './pages/Game';
import Result from './pages/Result';

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

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<Menu />} />
          <Route path="/game/:level" element={<Game />} />
          <Route path="/result" element={<Result />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
