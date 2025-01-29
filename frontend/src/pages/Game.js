import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Paper,
  Box,
  TextField,
  Button,
  LinearProgress
} from '@mui/material';
import axios from 'axios';

function Game() {
  const { level } = useParams();
  const navigate = useNavigate();
  const [currentCommand, setCurrentCommand] = useState(null);
  const [userInput, setUserInput] = useState('');
  const [score, setScore] = useState(0);
  const [mistakes, setMistakes] = useState(0);
  const [timeLeft, setTimeLeft] = useState(60);

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
  }, [level]);

  const fetchNextCommand = async () => {
    try {
      const response = await axios.get(`/api/game/generate-question/1/${level}`);
      setCurrentCommand(response.data);
    } catch (error) {
      console.error('コマンドの取得に失敗しました:', error);
    }
  };

  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleSubmit = () => {
    if (userInput.trim() === currentCommand.command) {
      setScore(score + 10);
      setUserInput('');
      fetchNextCommand();
    } else {
      setMistakes(mistakes + 1);
      // 苦手なコマンドとして記録
      axios.post('/api/game/weak-points', {
        user_id: 1,
        command: currentCommand.command,
        difficulty_level: level
      });
    }
  };

  const endGame = () => {
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
        totalCommands: Math.floor(score / 10)
      }
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

        <Paper sx={{ p: 3 }}>
          <Typography variant="h5" gutterBottom>
            このコマンドを入力してください:
          </Typography>
          <Typography variant="body1" gutterBottom>
            説明: {currentCommand.description}
          </Typography>
          <Box sx={{ my: 3 }}>
            <TextField
              fullWidth
              label="コマンドを入力"
              value={userInput}
              onChange={handleInputChange}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  handleSubmit();
                }
              }}
            />
          </Box>
          <Button
            variant="contained"
            color="primary"
            onClick={handleSubmit}
            fullWidth
          >
            送信
          </Button>
        </Paper>
      </Box>
    </Container>
  );
}

export default Game;
