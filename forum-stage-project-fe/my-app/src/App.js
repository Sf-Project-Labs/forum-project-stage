import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import HomePage from "./components/HomePage";
import LoginPage from "./components/LoginPage";
import RegisterPage from "./components/RegisterPage";
import checkIsAuthenticated from "./utils/isAuthenticated";
import LogoutPage from "./components/LogoutPage";

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Synchronize authentication state with the `checkIsAuthenticated` function
  useEffect(() => {
    setIsAuthenticated(checkIsAuthenticated());
  }, []);

  const handleLogin = () => {
    if (checkIsAuthenticated()) {
      setIsAuthenticated(true);
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem("accessToken");
  };

  return (
    <Router>
      <Routes>
        {/* Home Page */}
        <Route
          path="/"
          element={
            <HomePage
              isAuthenticated={isAuthenticated}
              handleLogout={handleLogout}
            />
          }
        />

        {/* Login Page */}
        <Route
          path="/login"
          element={
            isAuthenticated ? (
              <Navigate to="/" />
            ) : (
              <LoginPage handleLogin={handleLogin} />
            )
          }
        />

        {/* Register Page */}
        <Route
          path="/register"
          element={isAuthenticated ? <Navigate to="/" /> : <RegisterPage />}
        />

        {/* Logout Page */}
        <Route
          path="/logout"
          element={
            isAuthenticated ? (
              <LogoutPage handleLogout={handleLogout} />
            ) : (
              <Navigate to="/login" />
            )
          }
        />
      </Routes>
    </Router>
  );
};

export default App;
