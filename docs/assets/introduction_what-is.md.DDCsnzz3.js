import{_ as r,C as o,c as n,o as l,j as a,al as s,G as t,a as h}from"./chunks/framework.CEo5TfsR.js";const v=JSON.parse('{"title":"What is hypermea?","description":"","frontmatter":{"layout":"doc","prev":false,"next":{"text":"Getting started","link":"/introduction/quickstart"}},"headers":[],"relativePath":"introduction/what-is.md","filePath":"introduction/what-is.md"}'),p={name:"introduction/what-is.md"},d={class:"tip custom-block"};function c(m,e,u,k,y,g){const i=o("centered-image");return l(),n("div",null,[e[3]||(e[3]=a("h1",{id:"what-is-hypermea",tabindex:"-1"},[h("What is hypermea? "),a("a",{class:"header-anchor",href:"#what-is-hypermea","aria-label":'Permalink to "What is hypermea?"'},"​")],-1)),e[4]||(e[4]=a("p",null,"Hypermea (hy-PER-me-a) is a toolkit that lets you rapidly create production ready, hypermedia driven, microservice compatible APIs.",-1)),a("div",d,[e[0]||(e[0]=a("p",{class:"custom-block-title"},"Note",-1)),e[1]||(e[1]=a("p",null,"We have been using hypermea internally for years to create real-life production microservice clusters. We are in the process of shrink-wrapping the package and polishing the documentation.",-1)),e[2]||(e[2]=a("p",null,"Version 1.0.0 is coming soon. Until its release, proceed with caution.",-1)),t(i,{src:"/img/work-in-progress.png"})]),e[5]||(e[5]=s('<h2 id="production-ready" tabindex="-1">Production Ready <a class="header-anchor" href="#production-ready" aria-label="Permalink to &quot;Production Ready&quot;">​</a></h2><p>When you build your API service with hypermea, out of the box your service has:</p><ul><li>a managed settings configuration system, organized along integration lines</li><li>sophisticated error handling</li><li>expressive logging</li><li>optional git integration</li><li>optional docker integration</li><li>and so much more</li></ul><p>The code generated by hypermea has been battle tested in the most demanding production environments. You can trust that your services will be robust and reliable.</p><p>To learn more about what hypermea does for you, check out [[TODO]].</p><h2 id="hypermedia-driven" tabindex="-1">Hypermedia-Driven <a class="header-anchor" href="#hypermedia-driven" aria-label="Permalink to &quot;Hypermedia-Driven&quot;">​</a></h2><p>Hypermedia means using links to navigate and operate an API. Clients do not need to know how your services are architected. Client code is truly decoupled from your services. This lets the back-end team change things server-side without requiring clients to change along.</p><p>How is this possible? The idea is simple - so simple that it&#39;s hard to believe it works.</p><p><a href="https://pointw-dev.github.io/hypermedia-docs" target="_blank" rel="noreferrer">Learn more about hypermedia</a>.</p><h2 id="microservice-compatible" tabindex="-1">Microservice Compatible <a class="header-anchor" href="#microservice-compatible" aria-label="Permalink to &quot;Microservice Compatible&quot;">​</a></h2><p>A good microservice is a small, independently deployable service, and does one thing well. A developer can hold the entire microservice in her head. Because they are so small, you will need many of them to drive your business. This solves many problems, but it also creates new ones.</p><ul><li>How do you manage such a large number of services? <ul><li>Hypermea adopts the <a href="https://microservices.io/patterns/apigateway.html" target="_blank" rel="noreferrer">API Gateway pattern</a> which guides clients to the resources they use without having to know anything in advance about your service architecture.</li></ul></li><li>What happens if a microservice starts out small then grows over time and needs to split into smaller microservices? <ul><li>Because your services are hypermedia-driven, you can refactor, re-architect, and rearrange at any time without breaking your clients.</li></ul></li></ul><h1 id="okay-but-what-is-hypermea" tabindex="-1">Okay, but what <em>is</em> hypermea? <a class="header-anchor" href="#okay-but-what-is-hypermea" aria-label="Permalink to &quot;Okay, but what *is* hypermea?&quot;">​</a></h1><p>Hypermea is a package that consists of:</p><ul><li>command-line tools for generating new services and managing existing ones</li><li>a core library that adds features to your services</li></ul><h2 id="command-line-tools" tabindex="-1">Command-line tools <a class="header-anchor" href="#command-line-tools" aria-label="Permalink to &quot;Command-line tools&quot;">​</a></h2><p>Use simple commands to create your services. For example, let&#39;s start with this resource model:</p>',17)),t(i,{src:"/img/simple-resource-model.png",rounded:""}),e[6]||(e[6]=s(`<p>To implement this in a single service, first create the API:</p><div class="language-bash vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">bash</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">hypermea</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> api</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> create</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> order-processing</span></span></code></pre></div><div class="tip custom-block"><p class="custom-block-title">Note</p><p>The <code>hypermea</code> is aliased to <code>hy</code>. You can use whichever you prefer.</p></div><p>And now to build the resource model above:</p><div class="language-bash vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">bash</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">hy</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> resource</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> create</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> customers</span></span>
<span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">hy</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> resource</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> create</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> orders</span></span>
<span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">hy</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> link</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> create</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> customers</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> orders</span></span></code></pre></div><p>To learn about the commands, command has multi-level help:</p><div class="language-bash vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">bash</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">hy</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> --help</span></span>
<span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">hy</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> api</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> --help</span></span>
<span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">hy</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> api</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> create</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> --help</span></span></code></pre></div><p>To learn more, check out [[TODO]].</p><h2 id="core-library" tabindex="-1">Core library <a class="header-anchor" href="#core-library" aria-label="Permalink to &quot;Core library&quot;">​</a></h2><p>Hypermea&#39;s core library is an independently distributable package. It is separate from the command-line tools so your shippable packages are as lean as possible. The core library&#39;s purpose is primarily to power the functionality of your <code>hypermea_service</code>. It also provides an expanding set of methods to make your customizations easier: for example, access the database, standardize error messages, customize resource representations, and more. To learn more, check out [[TODO]].</p>`,10))])}const F=r(p,[["render",c]]);export{v as __pageData,F as default};
