import { Link } from "react-router-dom";
import "./Tutorial.css";

export default function Tutorial() {
  return (
    <div className="tutorial-page">
      <div className="tutorial-header">
        <Link to="/academy" className="tutorial-back">← Back to Academy</Link>
        <h1>Context Studio Tutorial</h1>
        <p className="tutorial-intro">
          A step-by-step guide to the Context Studio web app — landing page, signup, login, Launchpad, 9-step wizard, Cognitive Studio, Chain Composer, and Settings.
        </p>
      </div>

      <section className="tutorial-section">
        <h2>Quick Start</h2>
        <table className="tutorial-table">
          <thead>
            <tr>
              <th>Step</th>
              <th>Action</th>
              <th>Where</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>1</td><td>Open the app</td><td>Homepage</td></tr>
            <tr><td>2</td><td>Sign up or log in</td><td><strong>Get started free</strong> or <strong>Log in</strong></td></tr>
            <tr><td>3</td><td>Go to Context Studio</td><td><strong>Context Studio</strong> in the nav (or Launchpad card)</td></tr>
            <tr><td>4</td><td>Build your first context</td><td>Choose <strong>Manual</strong> or <strong>Copilot</strong>, complete the 9-step wizard</td></tr>
            <tr><td>5</td><td>Export or execute</td><td><strong>Ship It!</strong> → Export or Execute</td></tr>
          </tbody>
        </table>
        <p className="tutorial-note">Authentication flow (Landing → Login → Signup):</p>
        <img src="/tutorial/auth-flow.gif" alt="Auth flow animation" className="tutorial-img" />
      </section>

      <section className="tutorial-section">
        <h2>Prerequisites</h2>
        <ul>
          <li>The Context Studio app running (e.g. <code>http://localhost:5173/</code>)</li>
          <li>Backend API running (required for signup, login, and authenticated features)</li>
        </ul>
      </section>

      <section className="tutorial-section">
        <h2>1. Landing Page</h2>
        <p>When you first visit the application, you see the <strong>mycontext.ai</strong> landing page.</p>
        <img src="/tutorial/landing-page.png" alt="Landing page" className="tutorial-img" />
        <h3>Key Elements</h3>
        <ul>
          <li><strong>Header:</strong> Logo, theme toggle (light/dark), <strong>Log in</strong>, and <strong>Get started free</strong> buttons</li>
          <li><strong>Tagline:</strong> &quot;Don&apos;t write prompts. Engineer contexts.&quot;</li>
          <li><strong>Product links:</strong> Try Context Studio, Meet the Copilot, Browse all patterns, etc.</li>
        </ul>
        <h3>User Actions</h3>
        <ul>
          <li><strong>Log in</strong> → Goes to <code>/login</code></li>
          <li><strong>Get started free</strong> → Goes to <code>/signup</code></li>
        </ul>
      </section>

      <section className="tutorial-section">
        <h2>2. Authentication Flow</h2>
        <h3>Sign Up</h3>
        <img src="/tutorial/signup-page.png" alt="Sign up page" className="tutorial-img" />
        <ol>
          <li>Click <strong>Get started free</strong> or <strong>Try Context Studio</strong> from the landing page</li>
          <li>Enter your <strong>email</strong> (no disposable emails allowed)</li>
          <li>Enter a <strong>password</strong> that meets: 8+ chars, 1 uppercase, 1 lowercase, 1 digit</li>
          <li>Click <strong>Create account</strong></li>
        </ol>
        <h3>Log In</h3>
        <img src="/tutorial/login-page.png" alt="Login page" className="tutorial-img" />
        <ol>
          <li>Click <strong>Log in</strong> from the landing page</li>
          <li>Enter your <strong>email</strong> and <strong>password</strong></li>
          <li>Click <strong>Sign in</strong></li>
          <li>You&apos;ll be redirected to the <strong>Launchpad</strong> (Dashboard)</li>
        </ol>
      </section>

      <section className="tutorial-section">
        <h2>3. Main Application Layout</h2>
        <p>After logging in, you see the main app with a persistent layout.</p>
        <table className="tutorial-table">
          <thead>
            <tr>
              <th>Route</th>
              <th>Label</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr><td><code>/</code></td><td>Launchpad</td><td>Main dashboard</td></tr>
            <tr><td><code>/custom</code></td><td>Context Studio</td><td>Build custom contexts with 9-step wizard</td></tr>
            <tr><td><code>/templates</code></td><td>Cognitive Studio</td><td>Browse 85 research-backed patterns</td></tr>
            <tr><td><code>/chains</code></td><td>Chain Composer</td><td>Compose multi-pattern analysis pipelines</td></tr>
          </tbody>
        </table>
        <p><strong>User Menu:</strong> Click your avatar in the top-right for Profile, Settings, Log out.</p>
      </section>

      <section className="tutorial-section">
        <h2>4. Launchpad (Dashboard)</h2>
        <p>Your home base after login. Includes:</p>
        <ul>
          <li>Welcome message and stats</li>
          <li><strong>Your Journey</strong> — three cards: Context Studio, Cognitive Studio, Chain Composer</li>
          <li><strong>Platform at a Glance</strong> — 85 patterns, 13 export formats, 6 quality metrics</li>
          <li><strong>Milestones</strong> — checklist to track progress</li>
        </ul>
      </section>

      <section className="tutorial-section">
        <h2>5. Context Studio</h2>
        <p><strong>Path:</strong> <Link to="/custom">/custom</Link></p>
        <p>Build prompts step-by-step with a research-backed 9-section flow.</p>
        <h3>Two Paths</h3>
        <ul>
          <li><strong>Manual</strong> — Fill each section yourself</li>
          <li><strong>AI-driven (Copilot)</strong> — Describe what you need in plain English; the Copilot suggests content</li>
        </ul>
        <h3>9-Step Wizard</h3>
        <ul className="tutorial-steps">
          <li><strong>0. Pick Your Adventure</strong> — Choose manual or Copilot</li>
          <li><strong>1. Give It a Name</strong> — Name your context</li>
          <li><strong>2. Who Should It Be?</strong> — Role and goal</li>
          <li><strong>3. House Rules</strong> — Rules the AI must follow</li>
          <li><strong>4. Teach It to Think</strong> — Thinking strategy</li>
          <li><strong>5. Shape the Answer</strong> — Output schema</li>
          <li><strong>6. Guard Rails</strong> — Constraints</li>
          <li><strong>7. The Big Ask</strong> — Task/directive</li>
          <li><strong>8. Ship It!</strong> — Save, export, or execute</li>
        </ul>
      </section>

      <section className="tutorial-section">
        <h2>6. Cognitive Studio</h2>
        <p><strong>Path:</strong> <Link to="/templates">/templates</Link></p>
        <p>Browse and use 85 research-backed cognitive patterns. Search, select a pattern, fill parameters, Build, then Export or Execute.</p>
      </section>

      <section className="tutorial-section">
        <h2>7. Chain Composer</h2>
        <p><strong>Path:</strong> <Link to="/chains">/chains</Link></p>
        <p>Compose multiple cognitive patterns into analysis pipelines. Modes: <strong>Heuristic</strong> (free), <strong>Smart</strong> (AI), <strong>Hybrid</strong> (best).</p>
      </section>

      <section className="tutorial-section">
        <h2>8. Settings</h2>
        <p><strong>Path:</strong> <Link to="/settings">/settings</Link></p>
        <p>Tabs: <strong>API Keys</strong>, <strong>License</strong>, <strong>Preferences</strong>, <strong>Legal</strong>. Add your LLM provider keys here to enable Execute.</p>
      </section>

      <section className="tutorial-section">
        <h2>Troubleshooting</h2>
        <ul>
          <li><strong>&quot;Server error&quot; on signup</strong> — Ensure the backend API is running</li>
          <li><strong>Redirect to login</strong> — Session expired; log in again</li>
          <li><strong>Execute grayed out</strong> — Add an API key in Settings → API Keys</li>
          <li><strong>Enterprise patterns locked</strong> — Activate Enterprise license in Settings → License</li>
        </ul>
      </section>

      <div className="tutorial-footer">
        <Link to="/custom" className="tutorial-cta">Try Context Studio →</Link>
        <Link to="/academy" className="tutorial-link">Back to Academy</Link>
      </div>
    </div>
  );
}
