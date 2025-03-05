import{_ as s,c as a,o as n,ab as p}from"./chunks/framework.BeImCf7G.js";const y=JSON.parse('{"title":"Getting Started","description":"","frontmatter":{},"headers":[],"relativePath":"introduction/quickstart.md","filePath":"introduction/quickstart.md"}'),e={name:"introduction/quickstart.md"},t=p(`<h1 id="getting-started" tabindex="-1">Getting Started <a class="header-anchor" href="#getting-started" aria-label="Permalink to &quot;Getting Started&quot;">​</a></h1><p>Install hypermea into your Python virtual environment:</p><div class="language-bash vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">bash</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">pip</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> install</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> hypermea</span></span></code></pre></div><p>Create your API. For example, to create a service named <code>order-processing</code>:</p><div class="language-bash vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">bash</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">hy</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> api</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> create</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> order-processing</span></span></code></pre></div><p>This creates the following project folders and files:</p><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>/order-processing</span></span>
<span class="line"><span>│   hypermea_service.py</span></span>
<span class="line"><span>│   requirements.txt</span></span>
<span class="line"><span>│   run.py</span></span>
<span class="line"><span>│   settings.py</span></span>
<span class="line"><span>│   _env.conf</span></span>
<span class="line"><span>│   </span></span>
<span class="line"><span>├───affordances</span></span>
<span class="line"><span>│       __init__.py</span></span>
<span class="line"><span>│       </span></span>
<span class="line"><span>├───configuration</span></span>
<span class="line"><span>│       api_settings.py</span></span>
<span class="line"><span>│       hypermea_settings.py</span></span>
<span class="line"><span>│       __init__.py</span></span>
<span class="line"><span>│       </span></span>
<span class="line"><span>├───domain</span></span>
<span class="line"><span>│       customers.py</span></span>
<span class="line"><span>│       orders.py</span></span>
<span class="line"><span>│       _common.py</span></span>
<span class="line"><span>│       _settings.py</span></span>
<span class="line"><span>│       __init__.py</span></span>
<span class="line"><span>│       </span></span>
<span class="line"><span>└───hooks</span></span>
<span class="line"><span>        customers.py</span></span>
<span class="line"><span>        orders.py</span></span>
<span class="line"><span>        _error_handlers.py</span></span>
<span class="line"><span>        _gateway.py</span></span>
<span class="line"><span>        _logs.py</span></span>
<span class="line"><span>        _settings.py</span></span></code></pre></div><p>That&#39;s 23 files and almost a thousand lines of code that you do not have to type, ready for you to customize as you require. This is just the tip of the iceberg.</p>`,8),i=[t];function l(o,c,r,h,d,_){return n(),a("div",null,i)}const u=s(e,[["render",l]]);export{y as __pageData,u as default};
