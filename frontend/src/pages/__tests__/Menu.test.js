import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter, useNavigate } from 'react-router-dom';
import Menu from '../Menu';

// useNavigateをモック化
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: jest.fn()
}));

describe('Menu Component', () => {
  let mockNavigate;

  beforeEach(() => {
    mockNavigate = jest.fn();
    useNavigate.mockReturnValue(mockNavigate);
  });

  test('renders menu title', () => {
    render(
      <BrowserRouter>
        <Menu />
      </BrowserRouter>
    );
    expect(screen.getByText('Vim学習ゲーム')).toBeInTheDocument();
    expect(screen.getByText('レベルを選択してください')).toBeInTheDocument();
  });

  test('renders all level buttons', () => {
    render(
      <BrowserRouter>
        <Menu />
      </BrowserRouter>
    );

    // レベル1から10までのボタンが存在することを確認
    for (let i = 1; i <= 10; i++) {
      expect(screen.getByText(`レベル ${i}`)).toBeInTheDocument();
    }
  });

  test('navigates to correct level when button is clicked', () => {
    render(
      <BrowserRouter>
        <Menu />
      </BrowserRouter>
    );
    
    // レベル5のボタンをクリック
    const button = screen.getByText('レベル 5');
    fireEvent.click(button);
    
    // 正しいパスに遷移することを確認
    expect(mockNavigate).toHaveBeenCalledWith('/game/5');
  });
});
