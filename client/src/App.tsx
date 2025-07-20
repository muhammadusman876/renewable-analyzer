import React from 'react';
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  ThemeProvider,
  createTheme,
  CssBaseline,
} from '@mui/material';
import { SolarPower } from '@mui/icons-material';
import Home from './components/Home';

const theme = createTheme({
  palette: {
    primary: {
      main: '#2e7d32', // Green for renewable energy
    },
    secondary: {
      main: '#ffa726', // Orange for solar energy
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    h2: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 500,
    },
  },
});

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1, bgcolor: 'background.default', minHeight: '100vh' }}>
        <AppBar position="static" elevation={0}>
          <Toolbar>
            <SolarPower sx={{ mr: 2 }} />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Renewable Energy Investment Analyzer
            </Typography>
            <Typography variant="subtitle1">
              🇩🇪 Germany Solar Calculator
            </Typography>
          </Toolbar>
        </AppBar>

        <Home />
      </Box>
    </ThemeProvider>
  );
};

export default App;
