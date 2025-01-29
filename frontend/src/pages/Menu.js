import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Paper,
  Box,
  Button,
  FormControlLabel,
  Checkbox,
  Grid,
  Select,
  MenuItem,
  FormControl,
  InputLabel
} from '@mui/material';
import { useSettings } from '../contexts/Settings';

const levels = Array.from({ length: 10 }, (_, i) => i + 1);
const gameTimes = [60, 90, 120, 180];

function Menu() {
  const navigate = useNavigate();
  const { showCommand, setShowCommand, gameTime, setGameTime } = useSettings();

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
        
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            設定
          </Typography>
          <FormControlLabel
            control={
              <Checkbox
                checked={showCommand}
                onChange={(e) => setShowCommand(e.target.checked)}
              />
            }
            label="コマンドを表示する（練習モード）"
          />
          <FormControl fullWidth sx={{ mt: 2 }}>
            <InputLabel>ゲーム時間</InputLabel>
            <Select
              value={gameTime}
              onChange={(e) => setGameTime(e.target.value)}
              label="ゲーム時間"
            >
              {gameTimes.map((time) => (
                <MenuItem key={time} value={time}>
                  {time}秒
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Paper>
        
        <Grid container spacing={2} sx={{ mt: 4 }}>
          {levels.map((level) => (
            <Grid item xs={12} sm={6} md={4} key={level}>
              <Paper
                sx={{
                  p: 2,
                  textAlign: 'center',
                  '&:hover': {
                    backgroundColor: 'action.hover',
                  },
                }}
              >
                <Typography variant="h6" component="div" gutterBottom>
                  レベル {level}
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  onClick={() => handleLevelSelect(level)}
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
