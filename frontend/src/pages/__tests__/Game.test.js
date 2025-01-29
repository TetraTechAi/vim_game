import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import axios from 'axios';
import Game from '../Game';

// Axiosをモック化
jest.mock('axios');

// react-router-domのuseParamsとuseNavigateをモック化
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useParams: () => ({ level: '1' }),
  useNavigate: () => jest.fn(),
}));

describe('Game Component', () => {
  beforeEach(() => {
    // 各テストの前にモックをリセット
    jest.clearAllMocks();
    
    // APIレスポンスのモック
    axios.get.mockResolvedValue({
      data: {
        command: 'dd',
        description: '行を削除',
        difficulty_level: 1
      }
    });
  });

  test('renders game interface', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <Game />
        </BrowserRouter>
      );
    });
    
    expect(screen.getByText(/レベル 1/)).toBeInTheDocument();
    expect(screen.getByText(/スコア: 0/)).toBeInTheDocument();
    expect(screen.getByText(/ミス: 0/)).toBeInTheDocument();
  });

  test('handles correct input', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <Game />
        </BrowserRouter>
      );
    });
    
    const input = screen.getByLabelText('コマンドを入力');
    
    await act(async () => {
      fireEvent.change(input, { target: { value: 'dd' } });
      fireEvent.keyPress(input, { key: 'Enter', code: 13, charCode: 13 });
    });
    
    expect(screen.getByText(/スコア: 10/)).toBeInTheDocument();
  });

  test('handles incorrect input', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <Game />
        </BrowserRouter>
      );
    });
    
    const input = screen.getByLabelText('コマンドを入力');
    
    await act(async () => {
      fireEvent.change(input, { target: { value: 'wrong' } });
      fireEvent.keyPress(input, { key: 'Enter', code: 13, charCode: 13 });
    });
    
    expect(screen.getByText(/ミス: 1/)).toBeInTheDocument();
  });
});
