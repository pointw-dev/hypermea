<script setup lang="ts">
import { withBase } from 'vitepress'

const props = defineProps<{
  src: string
  width?: string
  rounded?: boolean
}>()

</script>

<template>
  <p align="center">
    <img :src="withBase(props.src)" :width="width" :class="props.rounded? 'rounded' : 'not_rounded'" />
    <span class="caption"><slot /></span>
  </p>
</template>

<style scoped>
.caption {
  color: gray;
}

.rounded {
  border-radius: 1rem;
}

</style>
