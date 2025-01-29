import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Paper,
  Box,
  Button,
  Grid
} from '@mui/material';

function Result() {
  const location = useLocation();
  const navigate = useNavigate();
  const { score, level, mistakes, totalCommands } = location.state || {
    score: 0,
    level: 1,
    mistakes: 0,
    totalCommands: 0
  };

  const accuracy = totalCommands > 0
    ? Math.round((totalCommands - mistakes) / totalCommands * 100)
    : 0;

  const handleRetry = () => {
    navigate(`/game/${level}`);
  };

  const handleBackToMenu = () => {
    navigate('/');
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          ゲーム結果
        </Typography>

        <Paper sx={{ p: 3, mb: 3 }}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="h5" gutterBottom>
                レベル: {level}
              </Typography>
              <Typography variant="h5" gutterBottom>
                最終スコア: {score}
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="h5" gutterBottom>
                正解数: {totalCommands}
              </Typography>
              <Typography variant="h5" gutterBottom>
                正確性: {accuracy}%
              </Typography>
            </Grid>
          </Grid>
        </Paper>

        <Box sx={{ mt: 4, display: 'flex', gap: 2, justifyContent: 'center' }}>
          <Button
            variant="contained"
            color="primary"
            onClick={handleRetry}
            size="large"
          >
            もう一度挑戦
          </Button>
          <Button
            variant="outlined"
            color="primary"
            onClick={handleBackToMenu}
            size="large"
          >
            メニューに戻る
          </Button>
        </Box>
      </Box>
    </Container>
  );
}

export default Result;
