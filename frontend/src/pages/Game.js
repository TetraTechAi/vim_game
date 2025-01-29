import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Paper,
  Box,
  TextField,
  LinearProgress,
  Button
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
  const [isGameOver, setIsGameOver] = useState(false);
  const timerRef = useRef(null);

  const endGame = useCallback(() => {
    if (isGameOver) return;
    setIsGameOver(true);

    // スコアを保存
    const token = localStorage.getItem('token');
    if (token) {
      axios.post('/api/game/progress', {
        level: parseInt(level),
        score: score
      }, {
        headers: { 
          Authorization: `Bearer ${token}`,
          'X-Token': token
        }
      });
    }
    
    navigate('/result', { 
      state: { 
        score,
        level,
        mistakes,
        totalCommands
      }
    });
  }, [score, level, mistakes, totalCommands, navigate, isGameOver]);

  // 初期化時に最初の問題を取得
  useEffect(() => {
    fetchNextCommand();
  }, [level]);

  // タイマーの設定
  useEffect(() => {
    timerRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timerRef.current);
          endGame();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [endGame]);

  // ゲーム時間が変更された場合
  useEffect(() => {
    setTimeLeft(gameTime);
  }, [gameTime]);

  const fetchNextCommand = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        navigate('/login');
        return;
      }

      const response = await axios.get(`/api/game/generate-question/${level}`, {
        headers: { 
          Authorization: `Bearer ${token}`,
          'X-Token': token
        }
      });
      setCurrentCommand(response.data);
    } catch (error) {
      console.error('コマンドの取得に失敗しました:', error);
      if (error.response?.status === 401) {
        navigate('/login');
      }
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
      fetchNextCommand(); // 正解時に新しい問題を取得
    }
  };

  const handleMistake = async () => {
    setMistakes(prev => prev + 1);
    fetchNextCommand(); // 間違えた時も新しい問題を取得
    
    // 苦手なコマンドとして記録
    const token = localStorage.getItem('token');
    if (token) {
      try {
        await axios.post('/api/game/weak-points', {
          command: currentCommand.command,
          difficulty_level: level
        }, {
          headers: { 
            Authorization: `Bearer ${token}`,
            'X-Token': token
          }
        });
      } catch (error) {
        console.error('苦手なコマンドの記録に失敗しました:', error);
      }
    }
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

        <Box sx={{ mt: 3, textAlign: 'center' }}>
          <Button
            variant="contained"
            color="secondary"
            onClick={endGame}
          >
            ゲームを終了
          </Button>
        </Box>
      </Box>
    </Container>
  );
}

export default Game;
