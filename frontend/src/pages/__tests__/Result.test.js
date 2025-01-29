import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Result from '../Result';

// モックのナビゲーション関数
const mockNavigate = jest.fn();

// react-router-domのuseLocationとuseNavigateをモック化
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useLocation: () => ({
    state: {
      score: 100,
      level: 5,
      mistakes: 2,
      totalCommands: 12
    }
  }),
  useNavigate: () => mockNavigate,
}));

describe('Result Component', () => {
  beforeEach(() => {
    // 各テストの前にモックをリセット
    mockNavigate.mockReset();
  });

  test('renders result information', () => {
    render(
      <BrowserRouter>
        <Result />
      </BrowserRouter>
    );
    
    expect(screen.getByText('ゲーム結果')).toBeInTheDocument();
    expect(screen.getByText(/レベル: 5/)).toBeInTheDocument();
    expect(screen.getByText(/最終スコア: 100/)).toBeInTheDocument();
    expect(screen.getByText(/正解数: 12/)).toBeInTheDocument();
    expect(screen.getByText(/正確性: 83%/)).toBeInTheDocument();
  });

  test('retry button navigates to game', () => {
    render(
      <BrowserRouter>
        <Result />
      </BrowserRouter>
    );
    
    fireEvent.click(screen.getByText('もう一度挑戦'));
    expect(mockNavigate).toHaveBeenCalledWith('/game/5');
  });

  test('menu button navigates to home', () => {
    render(
      <BrowserRouter>
        <Result />
      </BrowserRouter>
    );
    
    fireEvent.click(screen.getByText('メニューに戻る'));
    expect(mockNavigate).toHaveBeenCalledWith('/');
  });
});
