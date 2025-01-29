import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Paper,
  Box,
  TextField,
  LinearProgress
} from '@mui/material';
import axios from 'axios';
import { useSettings } from '../contexts/Settings';

function Game() {
  const { level } = useParams();
  const navigate = useNavigate();
  const { showCommand, gameTime } = useSettings();
  const [currentCommand, setCurrentCommand] = useState(null);
  const [userInput, setUserInput] = useState('');
  const [score, setScore] = useState(0);
  const [mistakes, setMistakes] = useState(0);
  const [timeLeft, setTimeLeft] = useState(gameTime);
  const [totalCommands, setTotalCommands] = useState(0);

  const endGame = useCallback(() => {
    // スコアを保存
    axios.post('/api/game/progress', {
      user_id: 1,
      level: parseInt(level),
      score: score
    });
    
    navigate('/result', { 
      state: { 
        score,
        level,
        mistakes,
        totalCommands
      }
    });
  }, [score, level, mistakes, totalCommands, navigate]);

  useEffect(() => {
    fetchNextCommand();
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          endGame();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [level, endGame]);

  useEffect(() => {
    setTimeLeft(gameTime);
  }, [gameTime]);

  const fetchNextCommand = async () => {
    try {
      const response = await axios.get(`/api/game/generate-question/1/${level}`);
      setCurrentCommand(response.data);
    } catch (error) {
      console.error('コマンドの取得に失敗しました:', error);
    }
  };

  const handleInputChange = (e) => {
    const input = e.target.value;
    setUserInput(input);

    // 入力が完了したら自動的に判定
    if (input === currentCommand.command) {
      setScore(prev => prev + 10);
      setTotalCommands(prev => prev + 1);
      setUserInput('');
      fetchNextCommand();
    }
  };

  const handleMistake = () => {
    setMistakes(prev => prev + 1);
    // 苦手なコマンドとして記録
    axios.post('/api/game/weak-points', {
      user_id: 1,
      command: currentCommand.command,
      difficulty_level: level
    });
  };

  if (!currentCommand) {
    return <LinearProgress />;
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          レベル {level}
        </Typography>
        
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            残り時間: {timeLeft}秒
          </Typography>
          <Typography variant="h6" gutterBottom>
            スコア: {score}
          </Typography>
          <Typography variant="h6" gutterBottom>
            ミス: {mistakes}
          </Typography>
        </Paper>

        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h5" gutterBottom>
            問題
          </Typography>
          {showCommand && (
            <Typography variant="h6" gutterBottom color="primary">
              コマンド: {currentCommand.command}
            </Typography>
          )}
          <Typography variant="body1" gutterBottom>
            説明: {currentCommand.description || '説明が見つかりません'}
          </Typography>
          <Box sx={{ mt: 3 }}>
            <TextField
              fullWidth
              label="コマンドを入力"
              value={userInput}
              onChange={handleInputChange}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  if (userInput !== currentCommand.command) {
                    handleMistake();
                  }
                  setUserInput('');
                }
              }}
              variant="outlined"
              autoFocus
            />
          </Box>
        </Paper>
      </Box>
    </Container>
  );
}

export default Game;
