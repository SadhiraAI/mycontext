import { Link } from "react-router-dom";
import "./NotFound.css";

export default function NotFound() {
  return (
    <div className="notfound-page">
      <div className="notfound-content">
        <span className="notfound-code">404</span>
        <h1>Page not found</h1>
        <p>The page you're looking for doesn't exist or has been moved.</p>
        <div className="notfound-actions">
          <Link to="/" className="notfound-btn primary">Go to Launchpad</Link>
          <Link to="/templates" className="notfound-btn secondary">Browse Templates</Link>
        </div>
      </div>
    </div>
  );
}
