import { createTheme } from "@mui/material/styles";

export const theme = createTheme({
  palette: {
    primary: {
      main: "#2E7D32", // Green for renewable energy
      light: "#4CAF50",
      dark: "#1B5E20",
    },
    secondary: {
      main: "#FFA726", // Orange for solar/energy
      light: "#FFB74D",
      dark: "#F57C00",
    },
    background: {
      default: "#F8F9FA",
      paper: "#FFFFFF",
    },
    success: {
      main: "#4CAF50",
    },
    info: {
      main: "#2196F3",
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: "2.5rem",
      fontWeight: 600,
      color: "#1B5E20",
    },
    h2: {
      fontSize: "2rem",
      fontWeight: 500,
      color: "#2E7D32",
    },
    h3: {
      fontSize: "1.5rem",
      fontWeight: 500,
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
          transition: "all 0.3s ease",
          "&:hover": {
            boxShadow: "0 6px 20px rgba(0,0,0,0.15)",
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: "none",
          fontWeight: 500,
        },
      },
    },
  },
});
