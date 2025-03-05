<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { withBase } from 'vitepress'
import { useData } from 'vitepress'
const { site } = useData()
const quotes = [
    {
        quote: "It's okay to get lost every once in a while, sometimes getting list is how we find ourselves.",
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
        quote: "I don't know why it's called \"getting lost.\"  Even when you turn down the wrong street, when you find yourself at the ded end of a chain-link fence or a a road that turned to sand, you are somewhere.  It just isn't where you expected to be.",
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
]

const locale = ref({
  link: '/',
  index: 'root'
})

onMounted(() => {
  const path = window.location.pathname
    .replace(site.value.base, '')
    .replace(/(^.*?\/).*$/, '/$1')
})

const notFound = computed({
    get() {
        const selected = quotes[Math.floor(Math.random() * quotes.length)]

        let quote = ''
        if (typeof selected === 'object') {
            quote = selected.quote + '\n\- ' +  selected.by
        } else {
            quote = selected
        }
        return {
          code: 404,
          title: 'PAGE NOT FOUND',
          quote: quote,
          linkLabel: 'go home',
          linkText: 'Back to the home page',
          ...(locale.value.index === 'root'
            ? site.value.themeConfig?.notFound
            : site.value.locales?.[locale.value.index]?.themeConfig?.notFound)
        }
    }
})
</script>

<template>
  <div class="NotFound">
    <p class="code">{{ notFound.code }}</p>
    <h1 class="title">{{ notFound.title }}</h1>
    <div class="divider" />
    <blockquote class="quote">{{ notFound.quote }}</blockquote>

    <div class="action">
      <a
        class="link"
        :href="withBase(locale.link)"
        :aria-label="notFound.linkLabel"
      >
        {{ notFound.linkText }}
      </a>
    </div>
  </div>
</template>

<style scoped>
.NotFound {
  padding: 64px 24px 96px;
  text-align: center;
}

@media (min-width: 768px) {
  .NotFound {
    padding: 96px 32px 168px;
  }
}

.code {
  line-height: 64px;
  font-size: 64px;
  font-weight: 600;
}

.title {
  padding-top: 12px;
  letter-spacing: 2px;
  line-height: 20px;
  font-size: 20px;
  font-weight: 700;
}

.divider {
  margin: 24px auto 18px;
  width: 64px;
  height: 1px;
  background-color: var(--vp-c-divider);
}

.quote {
  margin: 0 auto;
  max-width: 256px;
  font-size: 14px;
  font-weight: 500;
  color: var(--vp-c-text-2);
}

.action {
  padding-top: 20px;
}

.link {
  display: inline-block;
  border: 1px solid var(--vp-c-brand-1);
  border-radius: 16px;
  padding: 3px 16px;
  font-size: 14px;
  font-weight: 500;
  color: var(--vp-c-brand-1);
  transition:
    border-color 0.25s,
    color 0.25s;
}

.link:hover {
  border-color: var(--vp-c-brand-2);
  color: var(--vp-c-brand-2);
}
</style>
