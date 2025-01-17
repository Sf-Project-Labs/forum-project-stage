import React from "react";
import { Link } from "react-router-dom";
import "../styles/HomePage.css";
import Footer from "./Footer";

const HomePage = ({ isAuthenticated, handleLogout }) => {
  return (
    <div className="home-page">
      <nav className="navbar">
        <div className="nav-brand">My Website</div>
        <div className="nav-links">
          {isAuthenticated ? (
            <Link to="/logout" className="nav-link">
              Logout
            </Link>
          ) : (
            <>
              <Link to="/login" className="nav-link">
                Login
              </Link>
              <Link to="/register" className="nav-link">
                Register
              </Link>
            </>
          )}
        </div>
      </nav>
      <div className="main-content">
        <h1>Welcome to Home Page</h1>
      </div>
      <Footer />
    </div>
  );
};

export default HomePage;
