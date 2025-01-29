import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost/api',
});

export const gameService = {
  getCommands: (level) => api.get(`/game/commands/${level}`),
  getWeakPoints: (userId) => api.get(`/game/weak-points/${userId}`),
  saveProgress: (data) => api.post('/game/progress', data),
  generateQuestion: (userId, level) => api.get(`/game/generate-question/${userId}/${level}`),
};

export const userService = {
  register: (username) => api.post('/user/register', { username }),
  getProgress: (userId) => api.get(`/user/${userId}/progress`),
  getStats: (userId) => api.get(`/user/${userId}/stats`),
};

export default {
  gameService,
  userService,
};
