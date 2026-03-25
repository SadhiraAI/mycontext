// v0.10.0
import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const isProduction = process.env.NODE_ENV === 'production';

const config: Config = {
  title: 'mycontext-ai',
  tagline: 'Context engineering for LLMs. Build once, run anywhere, measure everything.',
  favicon: 'img/favicon.ico',

  url: 'https://mycontext-docs.pages.dev',
  baseUrl: '/',

  organizationName: 'SadhiraAI',
  projectName: 'mycontext',

  onBrokenLinks: 'throw',

  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
    mermaid: true,
  },

  themes: ['@docusaurus/theme-mermaid'],

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/SadhiraAI/mycontext/tree/main/website/',
          showLastUpdateTime: true,
          exclude: isProduction ? ['**/research/**'] : [],
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          editUrl: 'https://github.com/SadhiraAI/mycontext/tree/main/website/',
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  plugins: [
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      {
        hashed: true,
        language: ['en'],
        indexDocs: true,
        indexBlog: true,
        indexPages: false,
        docsRouteBasePath: '/docs',
        blogRouteBasePath: '/blog',
        searchResultLimits: 8,
        searchResultContextMaxLength: 50,
        highlightSearchTermsOnTargetPage: true,
        explicitSearchResultPath: true,
        removeDefaultStopWordFilter: false,
        removeDefaultStemmer: false,
      },
    ],
  ],

  headTags: [
    {
      tagName: 'script',
      attributes: {
        defer: 'true',
        src: 'https://static.cloudflareinsights.com/beacon.min.js',
        'data-cf-beacon': '{"token": "9907e76623d747808e8ec4fdd9523f06"}',
      },
    },
  ],

  themeConfig: {
    image: 'img/mycontext-social-card.png',
    mermaid: {
      theme: { light: 'neutral', dark: 'dark' },
      options: { fontFamily: 'inherit', useMaxWidth: true },
    },
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    announcementBar: {
      id: 'v0_10_0',
      content:
        '<b>mycontext-ai v0.10.0</b> — <code>suggest_routes()</code> for multi-agent planning, smarter template integration (GENERIC_PROMPT fingerprints, <code>integration_rationale</code>), catalog <code>PRODUCES</code> hints, and <code>build_workflow_chain()</code> deprecation. <a href="/docs/getting-started/installation">Install →</a>',
      isCloseable: true,
    },
    navbar: {
      title: 'mycontext',
      style: 'dark',
      hideOnScroll: true,
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Docs',
        },
        {
          to: '/docs/api/overview',
          label: 'API',
          position: 'left',
        },
        {
          to: '/patterns',
          label: 'Patterns',
          position: 'left',
        },
        {
          to: '/docs/use-cases/overview',
          label: 'Use Cases',
          position: 'left',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {
          href: 'https://pypi.org/project/mycontext-ai/',
          label: 'PyPI',
          position: 'right',
        },
        {
          href: 'https://github.com/SadhiraAI/mycontext',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Learn',
          items: [
            {label: 'Getting Started', to: '/docs/getting-started/installation'},
            {label: 'Quick Start', to: '/docs/getting-started/quickstart'},
            {label: 'Core Concepts', to: '/docs/getting-started/core-concepts'},
            {label: 'Cognitive Patterns', to: '/docs/cognitive-patterns/overview'},
          ],
        },
        {
          title: 'Guides',
          items: [
            {label: 'Intelligence Layer', to: '/docs/intelligence/overview'},
            {label: 'Async Execution', to: '/docs/intelligence/async-execution'},
            {label: 'Token-Budget Assembly', to: '/docs/intelligence/token-budget'},
            {label: 'Quality Metrics', to: '/docs/quality/quality-metrics'},
            {label: 'Security & Reliability', to: '/docs/advanced/reliability'},
            {label: 'Integrations', to: '/docs/integrations/overview'},
            {label: 'Use Cases', to: '/docs/use-cases/overview'},
          ],
        },
        {
          title: 'Community',
          items: [
            {label: 'GitHub', href: 'https://github.com/SadhiraAI/mycontext'},
            {label: 'PyPI', href: 'https://pypi.org/project/mycontext-ai/'},
            {label: 'Issues', href: 'https://github.com/SadhiraAI/mycontext/issues'},
          ],
        },
        {
          title: 'Company',
          items: [
            {label: 'SadhiraAI', href: 'https://sadhiraai.com'},
            {label: 'mycontext App', href: 'https://mycontext.sadhiraai.com'},
            {label: 'Blog', to: '/blog'},
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} SadhiraAI. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'json', 'yaml', 'toml'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
