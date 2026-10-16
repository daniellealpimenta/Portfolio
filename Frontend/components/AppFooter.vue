<template>
  <footer class="border-t border-divider">
    <div class="container-page py-12 flex flex-col gap-8 md:flex-row md:items-center md:justify-between">
      <div class="flex flex-col gap-1">
        <span class="font-semibold small-caps tracking-wide text-text">{{ user?.name || 'Daniel' }}</span>
        <span class="text-sm text-muted">{{ t('hero.role') }} · © {{ year }}</span>
      </div>

      <div class="flex flex-wrap items-center gap-x-8 gap-y-4">
        <SocialLinks />
        <a href="#main" class="btn btn-ghost text-sm" @click.prevent="toTop">{{ t('footer.top') }} ↑</a>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { usePortfolioApi } from '~/composables/usePortfolioApi'
import { useI18n } from '~/composables/useI18n'
import SocialLinks from '~/components/SocialLinks.vue'

const { user } = usePortfolioApi()
const { t } = useI18n()
const year = new Date().getFullYear()

function toTop() {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' })
}
</script>
