import type {ReactNode} from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

export default function NotFound(): ReactNode {
  return (
    <Layout title="Page Not Found">
      <main
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '60vh',
          textAlign: 'center',
          padding: '2rem',
        }}>
        <h1 style={{fontSize: '4rem', marginBottom: '0.5rem'}}>404</h1>
        <p
          style={{
            fontSize: '1.25rem',
            color: 'var(--ifm-font-color-secondary)',
            maxWidth: '480px',
            marginBottom: '2rem',
          }}>
          This page doesn't exist — but 88 cognitive patterns do.
        </p>
        <div style={{display: 'flex', gap: '1rem', flexWrap: 'wrap', justifyContent: 'center'}}>
          <Link
            to="/"
            style={{
              padding: '0.75rem 1.5rem',
              borderRadius: '8px',
              fontWeight: 600,
              background: 'var(--ifm-color-primary)',
              color: '#fff',
              textDecoration: 'none',
            }}>
            Go Home
          </Link>
          <Link
            to="/docs/getting-started/quickstart"
            style={{
              padding: '0.75rem 1.5rem',
              borderRadius: '8px',
              fontWeight: 600,
              border: '1px solid var(--ifm-color-primary)',
              color: 'var(--ifm-color-primary)',
              textDecoration: 'none',
            }}>
            Quick Start
          </Link>
          <Link
            to="/docs/cognitive-patterns/overview"
            style={{
              padding: '0.75rem 1.5rem',
              borderRadius: '8px',
              fontWeight: 600,
              border: '1px solid var(--ifm-color-primary)',
              color: 'var(--ifm-color-primary)',
              textDecoration: 'none',
            }}>
            Browse Patterns
          </Link>
        </div>
      </main>
    </Layout>
  );
}
