import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const LogoutPage = ({ handleLogout }) => {
  const navigate = useNavigate();

  useEffect(() => {
    handleLogout(); // Clear authentication status
    navigate("/"); // Redirect to the login page
  }, [handleLogout, navigate]);

  return <p>Logging out...</p>;
};

export default LogoutPage;
