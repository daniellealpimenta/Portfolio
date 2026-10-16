<template>
  <ul v-if="socials.length" class="flex items-center gap-1 text-muted" aria-label="Redes sociais">
    <li v-for="s in socials" :key="s.label">
      <a
        :href="s.href"
        target="_blank"
        rel="noopener noreferrer"
        :aria-label="s.label"
        class="grid place-items-center w-10 h-10 rounded-full transition-colors duration-fast ease-out hover:text-text hover:bg-surface-hover"
      >
        <span class="icon-mask w-5 h-5" :style="{ maskImage: `url(${s.icon})`, WebkitMaskImage: `url(${s.icon})` }" aria-hidden="true"></span>
      </a>
    </li>
  </ul>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { usePortfolioApi } from '~/composables/usePortfolioApi'

const { user } = usePortfolioApi()

const socials = computed(() => [
  { label: 'GitHub', href: user.value?.github_url, icon: '/icons/github-logo.png' },
  { label: 'LinkedIn', href: user.value?.linkedin_url, icon: '/icons/linkedin-logo.svg' },
  { label: 'Instagram', href: user.value?.instagram_url, icon: '/icons/instagram-logo.svg' },
  { label: 'Medium', href: user.value?.medium_url, icon: '/icons/medium-logo.svg' },
].filter(s => s.href))
</script>
