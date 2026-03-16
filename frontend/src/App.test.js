import { render, screen } from '@testing-library/react';
import App from './App';

test('renders currency converter title', () => {
  render(<App />);
  const titleElement = screen.getByText(/Conversor de Divisas/i);
  expect(titleElement).toBeInTheDocument();
});
