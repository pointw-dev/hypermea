import { defineConfig, withBase } from 'vitepress'
import { fileURLToPath, URL } from 'node:url'
const pkg = require('../../version_stamp.json')

const hostname = 'https://pointw-dev.github.io'
const basePath = 'hypermea'
const seoLogo = 'https://pointw-dev.github.io/hypermea/img/hypermea-card.png'
const title = 'hypermea'
const tagline = 'Simple Commands, Serious APIs'

const calculatedBasePath = (basePath? `/${basePath}/` : '/')
const siteUrl = hostname + calculatedBasePath

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: title,
  description: tagline,
  
  themeConfig: {
    siteTitle: title,
    stackOverflowTags: ['hypermea', 'hypermedia', 'rest', 'api'],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/pointw-dev/hypermea' },
      { icon: 'discord', link: 'https://discord.gg/HMen85bVUe' }
    ],
    logo: '/img/hero.svg',
  
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Quickstart', link: '/introduction/quickstart' },
      { text: pkg.version, link: null }
    ],

    outline: 'deep',
    sidebar: getSidebar(),
    search: {
        provider: 'local',
        options: {
            detailedView: true
        }
    },
    footer: {
      message: 'Released under the <a target="_blank" class="link" href="https://raw.githubusercontent.com/pointw-dev/hypermea/refs/heads/main/LICENSE">MIT License</a>.',
      copyright: 'Copyright © 2019-2025 Michael Ottoson (pointw.com)'
    }
  },
  
  base: calculatedBasePath,
  head: [
    ['link', { rel: 'icon', href: `/${calculatedBasePath}/favicon.ico` }],

    // test with https://www.opengraph.xyz/url/
    ['meta', {property: 'og:image', content: seoLogo}],
    ['meta', {property: "og:url", content: siteUrl}],
    ['meta', {property: "og:description", content: tagline}],
    ['meta', {property: 'og:type', content: 'website'}],

    ['meta', {name: "twitter:card", content: "summary_large_image"}],
    ['meta', {name: 'twitter:image', content: seoLogo}],
    ['meta', {property: "twitter:domain", content: "pointw.com"}],
    ['meta', {property: "twitter:url", content: siteUrl}],
    ['meta', {name: "twitter:title", content: title}],
    ['meta', {name: "twitter:description", content: tagline}]
  ],
  srcDir: 'src',
  vite: {
    resolve: {
      alias: [
        {
          find: /^.*\/VPFeature\.vue$/,
          replacement: fileURLToPath(new URL('./overrides/VPFeature.vue', import.meta.url))
        }
      ]
    }
  },
  sitemap: {
    hostname: siteUrl
  },
  transformPageData(pageData) {
    const canonicalUrl = siteUrl + `${pageData.relativePath}`
        .replace(/index\.md$/, '')
        .replace(/\.md$/, '.html')

    pageData.frontmatter.head ??= []
    pageData.frontmatter.head.push([
      'link',
      { rel: 'canonical', href: canonicalUrl }
    ])
  }
})


function getSidebar() {
    return [
      {
        text: 'Introduction',
        link: '/introduction/',
        items: [
          { text: 'What is hypermea?', link: '/introduction/what-is' },
          { text: 'Getting started', link: '/introduction/quickstart' }
        ]
      },
      {
        text: 'Basic concepts',
        link: '/concepts/',
      },
      {
        text: 'Features',
        link: '/features/',
        items: [
          {
            text: 'Scaffolding tools',
            link: '/features/scaffolding-tools',
            items: [
              {
                text: '<span class="code">api</span>',
                link: '/features/scaffolding-tools/api',
              },
              {
                text: '<span class="code">resource</span>',
                link: '/features/scaffolding-tools/resource',
              },
              {
                text: '<span class="code">link</span>',
                link: '/features/scaffolding-tools/link',
              },
              {
                text: '<span class="code">affordance</span>',
                link: '/features/scaffolding-tools/affordance',
              },
              {
                text: '<span class="code">endpoint</span>',
                link: '/features/scaffolding-tools/endpoint',
              },
              {
                text: '<span class="code">docker</span>',
                link: '/features/scaffolding-tools/docker',
              },
              {
                text: '<span class="code">integration</span>',
                link: '/features/scaffolding-tools/integration',
              },
              {
                text: '<span class="code">setting</span>',
                link: '/features/scaffolding-tools/setting',
              },
              {
                text: '<span class="code">run</span>',
                link: '/features/scaffolding-tools/run',
              },
              {
                text: 'Hypermea Core Library',
                link: '/features/scaffolding-tools/hypermea-core',
              },
              {
                text: 'Miscellaneous',
                link: '/features/scaffolding-tools/misc',
              }
            ]
          },
          {
            text: 'Runtime capabilities',
            link: '/features/runtime-capabilities',
            items: [
              {
                text: 'CRUD',
                link: '/features/runtime-capabilities/crud',
              },
              {
                text: 'Validation',
                link: '/features/runtime-capabilities/validation',
              },
              {
                text: 'Search collections',
                link: '/features/runtime-capabilities/search-collections/',
                items: [
                  {
                    text: 'Filtering',
                    link: '/features/runtime-capabilities/search-collections/filtering',
                  },
                  {
                    text: 'Sorting',
                    link: '/features/runtime-capabilities/search-collections/sorting',
                  },
                  {
                    text: 'Pagination',
                    link: '/features/runtime-capabilities/search-collections/pagination',
                  },
                ]
              },
              {
                text: 'Data shaping',
                link: '/features/runtime-capabilities/data-shaping',
                items: [
                  {
                    text: 'Projections',
                    link: '/features/runtime-capabilities/data-shaping/projections',
                  },
                  {
                    text: 'Pretty printing',
                    link: '/features/runtime-capabilities/data-shaping/pretty-printing',
                  },
                  {
                    text: 'Embed related resources',
                    link: '/features/runtime-capabilities/data-shaping/embed',
                  }
                ]
              },
              {
                text: 'Forms',
                link: '/features/runtime-capabilities/forms',
              },
              {
                text: 'Enhanced Logging',
                link: '/features/runtime-capabilities/enhanced-logging',
              },
              {
                text: 'Authentication',
                link: '/features/runtime-capabilities/authentication',
              },
              {
                text: 'Rate limiting',
                link: '/features/runtime-capabilities/rate-limiting',
              },
              {
                text: 'CORS',
                link: '/features/runtime-capabilities/cors',
              },
              {
                text: 'Bulk inserts',
                link: '/features/runtime-capabilities/bulk-inserts',
              },
              {
                text: 'Cache control',
                link: '/features/runtime-capabilities/cache-control',
              },
              {
                text: 'Conditional requests',
                link: '/features/runtime-capabilities/conditional-requests',
              },
              {
                text: 'Optimistic concurrency',
                link: '/features/runtime-capabilities/optimistic-concurrency',
              },
              {
                text: 'Soft delete',
                link: '/features/runtime-capabilities/soft-delete',
              },
              {
                text: 'Document versioning',
                link: '/features/runtime-capabilities/document-versioning',
              },
              {
                text: 'GeoJSON',
                link: '/features/runtime-capabilities/geo-json',
              },
              {
                text: 'Custom ID fields',
                link: '/features/runtime-capabilities/custom-id-fields',
              },
              {
                text: 'File storage',
                link: '/features/runtime-capabilities/file-storage',
              },
              {
                text: 'Settings management',
                link: '/features/runtime-capabilities/settings-management',
              },
              {
                text: 'Swagger',
                link: '/features/runtime-capabilities/swagger',
              },
              {
                text: 'Allure reporting',
                link: '/features/runtime-capabilities/allure-reporting',
              },
              {
                text: 'Echo endpoint',
                link: '/features/runtime-capabilities/echo',
              },
              {
                text: 'Gateway Registration',
                link: '/features/runtime-capabilities/gateway-registration'
              }
            ]
          }
        ]
      }
    ]
}