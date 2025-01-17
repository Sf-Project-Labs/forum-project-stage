const checkisAuthenticated = () => {
  const token = localStorage.getItem("accessToken");
  return token ? true : false;
};

export default checkisAuthenticated;
