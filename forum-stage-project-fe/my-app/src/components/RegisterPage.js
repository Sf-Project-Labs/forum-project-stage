import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/HomePage.css";

const RegisterPage = () => {
  const [userType, setUserType] = useState("startup");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate();

  const userTypeOptions = ["startup", "investor", "both"];

  const handleSubmit = (e) => {
    e.preventDefault();
    // Replace with actual API call
    if (email && password && confirmPassword && userType) {
      fetch("http://127.0.0.1:8000/register/", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_type: userType,
          email: email,
          password: password,
          confirm_password: confirmPassword,
        }),
      })
        .then((res) => res.json())
        .then((data) => console.log(data));

      alert("Registration successful!");
      navigate("/login");
    } else {
      alert("Please fill in all fields");
    }
  };

  return (
    <div className="auth-form">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <input
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
        <select value={userType} onChange={(e) => setUserType(e.target.value)}>
          <option value={userTypeOptions[0]}>Start Up</option>
          <option value={userTypeOptions[1]}>Investor</option>
          <option value={userTypeOptions[2]}>Both</option>
        </select>
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default RegisterPage;
