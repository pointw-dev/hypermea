---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: <img src="/hypermea/img/banner.png">
  tagline: Create production-ready hypermedia APIs - <i>fast</i>
  
  image:
    src: /img/hero.svg
    alt: hypermea
  
  actions:
    - theme: brand
      text: What is hypermea?
      link: /introduction/what-is
    - theme: alt
      text: Quickstart
      link: /introduction/quickstart

features:
  - title: Scaffolding tools
    icon: 🏗
    details: "With simple commands you generate a fully functional, hypermedia-driven API code base in minutes.  No tedious setup.<br/><br/>Before opening your IDE you can add resources, links, affordances.  Configure authentication, Git, Docker, and more.<br/><br/>Start with a solid foundation and focus on what matters: your business logic."
  - title: Runtime Libraries
    icon: 📚
    details: The APIs you create leverage <b><u><a href="https://flask.palletsprojects.com/en/stable/">Flask</a></u></b>, are powered by <b><u><a href="https://www.mongodb.com/">MongoDB</a></u></b>, and are enriched by <b><u><a href="https://docs.python-eve.org/en/stable/index.html">Eve</a></u></b>.  You get the benefits of those libraries without needing to learn them first.<br/><br/>With the <b><u><a href="https://pypi.org/project/hypermea-core/">hypermea-core</a></u></b> library your API is hypermedia-based using <b><u><a href="https://dev.to/nevnet99/wtf-is-hal-hypertext-application-language-2fo6">HAL</a></u></b> to represent your resources.<br/><br/>Out of the box your APIs are feature rich, including sorting, pagination, filtering, validation, bulk inserts, and much more.   
  - title: New to hypermedia?
    icon: 🔗
    details: Hypermedia is a simple idea with powerful results.  If you are new to hypermedia, start here.
    linkText: Learn more
    link: https://pointw-dev.github.io/hypermedia-docs/
    
---
Transform your development workflow with **hypermea**, the toolkit that lets you rapidly create production-ready hypermedia-driven APIs. Equipped with advanced features, sophisticated error handling, expressive logging and much more, hypermea ensures your APIs are built to last, whether for small projects or enterprise-scale solutions. Discover the power of hypermedia APIs and how **hypermea makes it easy**.