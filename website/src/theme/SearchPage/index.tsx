import React from 'react';
import Layout from '@theme/Layout';
import SearchBar from '@theme/SearchBar';

export default function SearchPage(): JSX.Element {
  return (
    <Layout title="Search">
      <div
        style={{
          maxWidth: 800,
          margin: '0 auto',
          padding: '2rem 1rem',
        }}>
        <h1>Search</h1>
        <p style={{ color: 'var(--ifm-color-secondary-darkest)', marginBottom: '1.5rem' }}>
          Search across all documentation, guides, and blog posts.
        </p>
        <SearchBar />
      </div>
    </Layout>
  );
}
