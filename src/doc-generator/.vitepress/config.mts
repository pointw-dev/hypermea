import { defineConfig, withBase } from 'vitepress'
import { fileURLToPath, URL } from 'node:url'
 const pkg = require('../../version_stamp.json')


const hostname = 'https://pointw-dev.github.io'
const basePath = 'hypermea'
const seoLogo = 'https://pointw-dev.github.io/hypermea/img/hero.svg'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: 'hypermea',
  description: 'Simple Commands, Serious APIs',
  
  themeConfig: {
    siteTitle: 'hypermea',
    stackOverflowTags: ['hypermea', 'hypermedia', 'rest', 'api'],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/pointw-dev/hypermea' }
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
  
  base: `/${basePath}/`,
  head: [
    ['link', { rel: 'icon', href: `/${basePath}/favicon.ico` }],

    // test with https://www.opengraph.xyz/url/
    ['meta', {property: 'og:image', content: seoLogo}],
    ['meta', {property: 'og:type', content: 'website'}],

    ['meta', {name: 'twitter:image', value: seoLogo}],
    ['meta', {name: 'twitter:card', value: 'summary'}]
  ],
  srcDir: 'src',
  vite: {
    resolve: {
      alias: [
        {
          find: /^.*\/VPFeature\.vue$/,
          replacement: fileURLToPath(new URL('./components/VPFeature.vue', import.meta.url))
        }
      ]
    }
  },
  sitemap: {
    hostname: hostname + (basePath? `/${basePath}/` : '')
  }
})


function getSidebar() {
    return [
      {
        text: 'Introduction',
        items: [
          { text: 'What is hypermea?', link: '/introduction/what-is' },
          { text: 'Getting started', link: '/introduction/quickstart' }
        ]
      }
    ]
}