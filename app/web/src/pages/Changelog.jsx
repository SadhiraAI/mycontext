import { CHANGELOG_ENTRIES } from "../data/changelog";
import "./Changelog.css";

function isNew(dateStr) {
  const d = new Date(dateStr);
  const now = new Date();
  return (now - d) < 7 * 24 * 60 * 60 * 1000;
}

export default function Changelog() {
  return (
    <div className="changelog-page">
      <h1>What's New</h1>
      <p className="changelog-intro">Latest updates and improvements to mycontext.</p>

      <div className="changelog-list">
        {CHANGELOG_ENTRIES.map((entry, i) => (
          <div key={i} className="changelog-entry">
            <div className="changelog-date">
              <span>{entry.date}</span>
              {isNew(entry.date) && <span className="changelog-new-badge">New</span>}
            </div>
            <h3>{entry.title}</h3>
            <ul>
              {entry.items.map((item, j) => (
                <li key={j}>{item}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
