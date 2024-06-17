// https://vitepress.dev/guide/custom-theme
import { h } from 'vue'
import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'

import { Tab, Tabs } from 'vue3-tabs-component'
import TitleImage from '../components/TitleImage.vue'
import AskStackOverflow from '../components/AskStackOverflow.vue'

import './tabs.css'
import './style.css'

export default {
  extends: DefaultTheme,
  
  Layout: () => {
    return h(DefaultTheme.Layout, null, {
      // https://vitepress.dev/guide/extending-default-theme#layout-slots
      'doc-footer-before': () => h(AskStackOverflow)
    })
  },
  
  enhanceApp({ app, router, siteData }) {
    app.component('Tab', Tab)
    app.component('Tabs', Tabs)
    app.component('AskStackOverflow', AskStackOverflow)
    app.component('TitleImage', TitleImage)
  }
} satisfies Theme
