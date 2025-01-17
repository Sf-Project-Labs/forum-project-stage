import { FaDiscord, FaTelegram, FaEnvelope } from "react-icons/fa";

function Footer() {
  return (
    <footer className="footer">
      <a
        href="https://discord.com"
        target="_blank"
        rel="noopener noreferrer"
        className="footer-icon"
      >
        <FaDiscord />
      </a>
      <a href="mailto:example@gmail.com" className="footer-icon">
        <FaEnvelope />
      </a>
      <a
        href="https://telegram.org"
        target="_blank"
        rel="noopener noreferrer"
        className="footer-icon"
      >
        <FaTelegram />
      </a>
    </footer>
  );
}

export default Footer;
