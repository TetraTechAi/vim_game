import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Button,
  Grid,
  Paper,
  Box
} from '@mui/material';

const levels = Array.from({ length: 10 }, (_, i) => i + 1);

function Menu() {
  const navigate = useNavigate();

  const handleLevelSelect = (level) => {
    navigate(`/game/${level}`);
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h2" component="h1" gutterBottom align="center">
          Vim学習ゲーム
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom align="center">
          レベルを選択してください
        </Typography>
        
        <Grid container spacing={2} sx={{ mt: 4 }}>
          {levels.map((level) => (
            <Grid item xs={12} sm={6} md={4} key={level}>
              <Paper
                sx={{
                  p: 2,
                  textAlign: 'center',
                  cursor: 'pointer',
                  '&:hover': {
                    backgroundColor: 'action.hover',
                  },
                }}
                onClick={() => handleLevelSelect(level)}
              >
                <Typography variant="h6" component="div" gutterBottom>
                  レベル {level}
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                >
                  開始
                </Button>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Container>
  );
}

export default Menu;
