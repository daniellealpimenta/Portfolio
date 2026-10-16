<template>
  <NuxtLayout>
    <NuxtPage :transition="{ name: 'page', mode: 'out-in' }" />
  </NuxtLayout>
</template>

<script setup lang="ts">
import { useI18n } from '~/composables/useI18n'

const { lang } = useI18n()
useHead(() => ({ htmlAttrs: { lang: lang.value === 'en' ? 'en' : 'pt-BR' } }))
</script>
