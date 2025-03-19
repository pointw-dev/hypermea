import {
  Fragment,
  computed,
  createBaseVNode,
  createBlock,
  createElementBlock,
  createTextVNode,
  createVNode,
  defineComponent,
  normalizeClass,
  onMounted,
  openBlock,
  ref,
  renderList,
  renderSlot,
  resolveComponent,
  resolveDynamicComponent,
  toDisplayString,
  unref
} from "./chunk-VJWGEPT5.js";

// node_modules/@pointw/vitepress-component-bundle/dist/vitepress-component-bundle.es.js
(function() {
  "use strict";
  try {
    if (typeof document < "u") {
      var t = document.createElement("style");
      t.appendChild(document.createTextNode('.edit-link-icon{margin-right:8px;margin-bottom:5px;width:16px;height:16px;fill:currentColor}.edit-link-button{display:flex;align-items:center;border:0;line-height:32px;font-size:14px;font-weight:500;color:var(--vp-c-brand);transition:color .25s}.edit-link-button:hover{color:var(--vp-c-brand-dark)}.centered-text[data-v-78f01fca]{text-align:center}.centered[data-v-78f01fca]{display:block;margin-left:auto;margin-right:auto}.caption[data-v-78f01fca]{color:gray;display:block;margin-top:.5rem}.rounded[data-v-78f01fca]{border-radius:1rem}.footer[data-v-7cd1e16b]{border-top:1px solid var(--vp-c-brand-soft);padding:23px 24px 24px;margin-top:24px}.link[data-v-7cd1e16b]{color:var(--vp-pointw-primary)}.copyright[data-v-7cd1e16b]{text-align:center;line-height:20px;font-size:12px;font-weight:500;color:var(--vp-pointw-accent)}.question[data-v-3b9d3e26]:before{content:"Q: ";font-weight:700}.answer[data-v-3b9d3e26]:before{content:"A: "}.question[data-v-3b9d3e26]{font-weight:700}.question[data-v-3b9d3e26],.answer[data-v-3b9d3e26]{display:block;text-indent:-1.3em;margin-left:1.5em}.NotFound[data-v-5ab5d36b]{padding:64px 24px 96px;text-align:center}@media (min-width: 768px){.NotFound[data-v-5ab5d36b]{padding:96px 32px 168px}}.code[data-v-5ab5d36b]{line-height:64px;font-size:64px;font-weight:600}.title[data-v-5ab5d36b]{padding-top:12px;letter-spacing:2px;line-height:20px;font-size:20px;font-weight:700}.divider[data-v-5ab5d36b]{margin:24px auto 18px;width:64px;height:1px;background-color:var(--vp-c-divider)}.quote[data-v-5ab5d36b]{margin:0 auto;max-width:256px;font-size:14px;font-weight:500;color:var(--vp-c-text-2)}.action[data-v-5ab5d36b]{padding-top:20px}.link[data-v-5ab5d36b]{display:inline-block;border:1px solid var(--vp-c-brand-1);border-radius:16px;padding:3px 16px;font-size:14px;font-weight:500;color:var(--vp-c-brand-1);transition:border-color .25s,color .25s}.link[data-v-5ab5d36b]:hover{border-color:var(--vp-c-brand-2);color:var(--vp-c-brand-2)}')), document.head.appendChild(t);
    }
  } catch (a) {
    console.error("vite-plugin-css-injected-by-js", a);
  }
})();
var u = (n, t) => {
  const o = n.__vccOpts || n;
  for (const [e, a] of t)
    o[e] = a;
  return o;
};
var I = {};
var C = {
  xmlns: "http://www.w3.org/2000/svg",
  viewBox: "0 0 32 32"
};
function S(n, t) {
  return openBlock(), createElementBlock("svg", C, t[0] || (t[0] = [
    createBaseVNode("path", { d: "M28.16 32H2.475V20.58H5.32v8.575h19.956V20.58h2.884z" }, null, -1),
    createBaseVNode("path", { d: "M8.477 19.8l13.993 2.923.585-2.806-13.993-2.923zm1.832-6.704l12.94 6.04 1.208-2.572-12.94-6.08zm3.586-6.353l10.99 9.12 1.832-2.183-10.99-9.12zM20.99 0l-2.3 1.715 8.536 11.46 2.3-1.715zM8.166 26.27H22.43v-2.845H8.166v2.845z" }, null, -1)
  ]));
}
var p = u(I, [["render", S]]);
var x = { class: "edit-info" };
var F = { class: "edit-link" };
var O = ["href"];
var M = defineComponent({
  __name: "AskStackOverflow",
  props: {
    frontmatter: {},
    theme: {}
  },
  setup(n) {
    const t = n;
    let o = [];
    t.theme.value.stackOverflowTags && (o = t.theme.value.stackOverflowTags), t.frontmatter.value.stackOverflowTags && (o = o.concat(t.frontmatter.value.stackOverflowTags)), o.length == 0 && t.theme.value.siteTitle && (o = [t.theme.value.siteTitle]);
    let e = "";
    for (const a of o)
      e.length > 0 && (e += "&"), e += `tags=${a}`;
    return e.length > 0 && (e = "?" + e), (a, r) => (openBlock(), createElementBlock("div", x, [
      createBaseVNode("div", F, [
        createBaseVNode("a", {
          class: "VPLink link edit-link-button",
          href: "https://stackoverflow.com/questions/ask" + unref(e),
          target: "_blank",
          rel: "noreferrer"
        }, [
          createVNode(p, { class: "edit-link-icon" }),
          r[0] || (r[0] = createTextVNode(" Ask a question on StackOverflow "))
        ], 8, O)
      ])
    ]));
  }
});
var N = { class: "centered-text" };
var z = ["src", "width"];
var A = { class: "caption" };
var B = defineComponent({
  __name: "CenteredImage",
  props: {
    src: {},
    width: {},
    rounded: { type: Boolean }
  },
  setup(n) {
    const t = n, o = ref(t.src);
    return onMounted(async () => {
      try {
        const e = await import("vitepress");
        typeof e.withBase == "function" && (o.value = e.withBase(t.src));
      } catch {
        console.warn("[CenteredImage] Failed to load withBase from vitepress — using raw src");
      }
    }), (e, a) => (openBlock(), createElementBlock("p", N, [
      createBaseVNode("img", {
        class: normalizeClass(["centered", e.rounded ? "rounded" : "not_rounded"]),
        src: o.value,
        width: e.width
      }, null, 10, z),
      createBaseVNode("span", A, [
        renderSlot(e.$slots, "default", {}, void 0, true)
      ])
    ]));
  }
});
var D = u(B, [["__scopeId", "data-v-78f01fca"]]);
var V = defineComponent({
  __name: "CommentsSection",
  props: {
    repo: {},
    repoId: {},
    category: {},
    categoryId: {}
  },
  setup(n) {
    const t = ref({});
    return onMounted(async () => {
      try {
        const { useData: o } = await import("vitepress"), e = o();
        t.value = e.title.value;
      } catch {
        console.warn("[CommentsSection] useData() not available - not running in VitePress context.");
      }
    }), (o, e) => (openBlock(), createElementBlock("div", {
      key: t.value,
      class: "giscus"
    }, [
      (openBlock(), createBlock(resolveDynamicComponent("script"), {
        src: "https://giscus.app/client.js",
        "data-repo": o.repo,
        "data-repo-id": o.repoId,
        "data-category": o.category,
        "data-category-id": o.categoryId,
        "data-mapping": "pathname",
        "data-strict": "0",
        "data-reactions-enabled": "1",
        "data-emit-metadata": "0",
        "data-input-position": "top",
        "data-lang": "en",
        "data-theme": "transparent_dark",
        "data-loading": "lazy",
        async: ""
      }, null, 8, ["data-repo", "data-repo-id", "data-category", "data-category-id"]))
    ]));
  }
});
var j = { class: "footer" };
var L = { class: "copyright" };
var P = defineComponent({
  __name: "Copyright",
  props: {
    message: {}
  },
  setup(n) {
    return (t, o) => (openBlock(), createElementBlock("div", j, [
      createBaseVNode("p", L, "Copyright © " + toDisplayString(t.message), 1)
    ]));
  }
});
var E = u(P, [["__scopeId", "data-v-7cd1e16b"]]);
var H = {};
var W = { class: "question" };
var G = { class: "answer" };
function J(n, t) {
  return openBlock(), createElementBlock("div", null, [
    createBaseVNode("p", W, [
      renderSlot(n.$slots, "question", {}, void 0, true)
    ]),
    createBaseVNode("p", G, [
      renderSlot(n.$slots, "answer", {}, void 0, true)
    ])
  ]);
}
var R = u(H, [["render", J], ["__scopeId", "data-v-3b9d3e26"]]);
var K = defineComponent({
  __name: "FutureLanguages",
  setup(n) {
    const t = [
      "Java",
      "C#",
      "PHP",
      "Go",
      "R"
    ];
    return (o, e) => {
      const a = resolveComponent("Tab");
      return openBlock(), createElementBlock(Fragment, null, renderList(t, (r) => createVNode(a, {
        key: r,
        name: r,
        "is-disabled": true
      }, null, 8, ["name"])), 64);
    };
  }
});
var Q = { class: "NotFound" };
var U = { class: "code" };
var Y = { class: "title" };
var X = { class: "quote" };
var Z = { class: "action" };
var ee = ["aria-label"];
var te = defineComponent({
  __name: "NotFound",
  setup(n) {
    const t = ref({});
    onMounted(
      async () => {
        try {
          const { useData: a } = await import("vitepress"), r = a();
          t.value = r.site.value;
        } catch {
          console.warn("[NotFound] useData() not available - not running in VitePress context.");
        }
        window.location.pathname.replace(t.value.base, "").replace(/(^.*?\/).*$/, "/$1");
      }
    );
    const o = [
      {
        quote: "It's okay to get lost every once in a while, sometimes getting lost is how we find ourselves.",
        by: "Robert Tew"
      },
      "We're lost, yes.....but we're making good time.",
      {
        quote: "The Truth is, we all get lost as we try to find our way.  Perhaps the key is to stop, take a look around and enjoy the scenery as we go.",
        by: "JaTawny Mulkelvene Chatmon"
      },
      {
        quote: "It is not how many times we get lost, but how many times we seek the path, again and again, that determines our level of consciousness.",
        by: "Vironika Tugaleva"
      },
      {
        quote: "When you lose your path, a surge of excitement comes to both your mind and body; your calm shores begin to be beaten by the waves! This vitality created by being lost is a good incentive to get lost!",
        by: "Mehmet Murat ildan"
      },
      {
        quote: "I suppose sometimes it takes getting lost to enjoy the joy of being found.",
        by: "Tricia Goyer"
      },
      {
        quote: "Getting lost along your path is part of finding the path you are meant to be on.",
        by: "Robin Sharma"
      },
      {
        quote: `I don't know why it's called "getting lost."  Even when you turn down the wrong street, when you find yourself at the ded end of a chain-link fence or a a road that turned to sand, you are somewhere.  It just isn't where you expected to be.`,
        by: "Jodi Picoult"
      },
      {
        quote: "The getting lost and recovering - that is the meditation",
        by: "Dan Harris"
      },
      {
        quote: "Getting lost is not fatal. Almost every time, it will make your world bigger.",
        by: "Julian Smith"
      },
      {
        quote: "The ultimate point of view is that there is nothing to understand, so when we try to understand, we are only indulging in acrobatics of the mind.  Whatever you have understood, you are not.  Why are you getting lost in concepts?  You are not what you know, you are the knower.",
        by: "Sri Nisargadatta Majaraj"
      },
      {
        quote: "All that is gold does not glitter, not all those who wander are lost; the old that is strong does not wither, deep roots are not reached by the frost.",
        by: "J.R.R. Tolkiein"
      },
      {
        quote: "We lose ourselves in things we love.  We find ourselves there, too.",
        by: "Kristen Martz"
      },
      {
        quote: "Not until we are lost do we begin to understand ourselves.",
        by: "Henry David Thoreau"
      },
      {
        quote: "I long, as does every human being, to be at home wherever I find myself.",
        by: "Maya Angelou"
      }
    ];
    ref({
      link: "/",
      index: "root"
    });
    const e = computed({
      get() {
        const a = o[Math.floor(Math.random() * o.length)];
        let r = "";
        return typeof a == "object" ? r = a.quote + `
- ` + a.by : r = a, {
          code: 404,
          title: "PAGE NOT FOUND",
          quote: r,
          linkLabel: "go home",
          linkText: "Back to the home page"
        };
      }
    });
    return (a, r) => (openBlock(), createElementBlock("div", Q, [
      createBaseVNode("p", U, toDisplayString(e.value.code), 1),
      createBaseVNode("h1", Y, toDisplayString(e.value.title), 1),
      r[0] || (r[0] = createBaseVNode("div", { class: "divider" }, null, -1)),
      createBaseVNode("blockquote", X, toDisplayString(e.value.quote), 1),
      createBaseVNode("div", Z, [
        createBaseVNode("a", {
          class: "link",
          href: "/",
          "aria-label": e.value.linkLabel
        }, toDisplayString(e.value.linkText), 9, ee)
      ])
    ]));
  }
});
var oe = u(te, [["__scopeId", "data-v-5ab5d36b"]]);
var ae = {
  install(n) {
    n.component("AskStackOverflow", M), n.component("CenteredImage", D), n.component("CommentsSection", V), n.component("Copyright", E), n.component("FaqEntry", R), n.component("FutureLanguages", K), n.component("NotFound", oe), n.component("StackOverflowIcon", p);
  }
};
export {
  M as AskStackOverflow,
  D as CenteredImage,
  V as CommentsSection,
  E as Copyright,
  R as FaqEntry,
  K as FutureLanguages,
  oe as NotFound,
  p as StackOverflowIcon,
  ae as default
};
//# sourceMappingURL=@pointw_vitepress-component-bundle.js.map
