<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vitepress'

const router = useRouter()
const basePath = router.route.path || '/'
const abc = 'def'
</script>


<template>
  <img :src="`${basePath}img/banner.png`">
</template>

