<script setup lang="ts">
import {useData} from "vitepress";
import StackOverflowIcon from "./StackOverflowIcon.vue";

const {frontmatter, theme} = useData()

let tags = []

if (theme.value.stackOverflowTags) {
  tags = theme.value.stackOverflowTags
}
if (frontmatter.value.stackOverflowTags) {
  tags = tags.concat(frontmatter.value.stackOverflowTags)
}
if (tags.length == 0 && theme.value.siteTitle) {
  tags = [theme.value.siteTitle]
}

let tagsQueryString = ''
for (const tag of tags) {
  if (tagsQueryString.length > 0) {
    tagsQueryString += '&'
  }
  tagsQueryString += `tags=${tag}`
}

if (tagsQueryString.length > 0) {
  tagsQueryString = '?' + tagsQueryString
}
</script>


<template>
  <div class="edit-info">
    <div class="edit-link">
      <a class="VPLink link edit-link-button" :href="'https://stackoverflow.com/questions/ask' + tagsQueryString" target="_blank" rel="noreferrer">
        <StackOverflowIcon class="edit-link-icon"/>
        Ask a question on StackOverflow
      </a>
    </div>
  </div>
</template>


<style>
.edit-link-icon {
  margin-right: 8px;
  margin-bottom: 5px;
  width: 16px;
  height: 16px;
  fill: currentColor;
}

.edit-link-button {
  display: flex;
  align-items: center;
  border: 0;
  line-height: 32px;
  font-size: 14px;
  font-weight: 500;
  color: var(--vp-c-brand);
  transition: color 0.25s;
  &:hover {
    color: var(--vp-c-brand-dark);
  }
}
</style>

