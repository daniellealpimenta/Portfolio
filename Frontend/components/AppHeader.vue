<template>
  <header
    class="site-header force-dark fixed top-0 inset-x-0 z-40 border-b border-transparent"
    :data-scrolled="scrolled || mobileMenuOpen"
  >
    <div class="container-page flex items-center justify-between gap-6 py-4">
      <NuxtLink
        :to="{ path: userPrefix, hash: '#contato' }"
        id="logo"
        class="flex items-center gap-2 text-base font-semibold small-caps tracking-wide text-text transition-colors duration-fast ease-out hover:text-primary"
      >
        <svg class="logo-bubble" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">
          <path d="M12 3C6.9 3 3 6.4 3 10.6c0 2.4 1.3 4.6 3.4 6.1-.1 1-.5 2.2-1.3 3.3 1.6-.3 3-1 4.1-1.8 .9.2 1.8.4 2.8.4 5.1 0 9-3.4 9-7.6S17.1 3 12 3Z" />
        </svg>
        {{ t('nav.hire') }}
      </NuxtLink>

      <nav class="hidden md:flex items-center gap-8 text-sm" aria-label="Principal">
        <NuxtLink
          v-for="item in nav"
          :key="item.to"
          :to="item.to"
          class="nav-link small-caps tracking-wide font-medium"
          :class="isActive(item) ? 'text-text' : 'text-muted hover:text-text'"
          :aria-current="isActive(item) ? 'page' : undefined"
        >{{ item.label }}</NuxtLink>
      </nav>

      <div class="flex items-center gap-3">
        <ThemePaletteSwitcher />
        <ThemeSwitch />

        <button
          type="button"
          class="ml-1 flex items-center gap-1 rounded-full px-2 py-1 text-sm small-caps tracking-wide"
          :aria-label="`${t('nav.language')}: ${lang === 'pt' ? 'Português' : 'English'}`"
          @click="toggleLang"
        >
          <span :class="lang === 'pt' ? 'text-text font-semibold' : 'text-muted'">pt</span>
          <span class="text-muted" aria-hidden="true">/</span>
          <span :class="lang === 'en' ? 'text-text font-semibold' : 'text-muted'">en</span>
        </button>

        <button
          type="button"
          class="md:hidden -mr-1 p-1.5 rounded-sm text-text"
          :aria-label="mobileMenuOpen ? t('nav.closeMenu') : t('nav.openMenu')"
          :aria-expanded="mobileMenuOpen"
          aria-controls="mobile-menu"
          @click="mobileMenuOpen = !mobileMenuOpen"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
            <path v-if="!mobileMenuOpen" d="M4 7h16M4 12h16M4 17h16" />
            <path v-else d="M6 6l12 12M18 6L6 18" />
          </svg>
        </button>
      </div>
    </div>

    <Transition name="menu">
      <nav v-if="mobileMenuOpen" id="mobile-menu" class="md:hidden border-t border-divider" aria-label="Principal">
        <div class="container-page flex flex-col py-3">
          <NuxtLink
            v-for="item in nav"
            :key="item.to"
            :to="item.to"
            class="py-3 text-lg small-caps tracking-wide"
            :class="isActive(item) ? 'text-primary font-semibold' : 'text-text'"
            :aria-current="isActive(item) ? 'page' : undefined"
            @click="mobileMenuOpen = false"
          >{{ item.label }}</NuxtLink>
        </div>
      </nav>
    </Transition>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import ThemeSwitch from '~/components/ui/ThemeSwitch.vue'
import ThemePaletteSwitcher from '~/components/ui/ThemePaletteSwitcher.vue'
import { useI18n } from '~/composables/useI18n'

const route = useRoute()
const { t, lang, toggleLang } = useI18n()
const mobileMenuOpen = ref(false)
const scrolled = ref(false)

const userPrefix = computed(() => {
  const userId = route.params.user_id as string
  return userId ? `/${userId}` : '/'
})

const nav = computed(() => {
  const base = userPrefix.value === '/' ? '' : userPrefix.value
  return [
    { to: base || '/', label: t('nav.home'), exact: true },
    { to: `${base}/about`, label: t('nav.about') },
    { to: `${base}/work`, label: t('nav.work') },
    { to: `${base}/resume`, label: t('nav.resume') },
  ]
})

function isActive(item: { to: string; exact?: boolean }) {
  if (item.exact) return route.path === item.to || route.path === `${item.to}/`
  // "Work" também fica ativo dentro da página de um projeto
  if (item.to.endsWith('/work')) return route.path.startsWith(item.to) || route.path.includes('/projects/')
  return route.path.startsWith(item.to)
}

function onScroll() {
  scrolled.value = window.scrollY > 8
}

watch(() => route.fullPath, () => { mobileMenuOpen.value = false })
onMounted(() => {
  onScroll()
  window.addEventListener('scroll', onScroll, { passive: true })
})
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.nav-link {
  position: relative;
  padding-block: 0.25rem;
  transition: color var(--dur-fast) var(--ease-out);
}
/* Sublinhado que "desenha" da esquerda pra direita; fica cheio na página atual */
.nav-link::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -2px;
  height: 1px;
  background: var(--color-primary);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform var(--dur-base) var(--ease-out);
}
.nav-link:hover::after,
.nav-link[aria-current='page']::after {
  transform: scaleX(1);
}

.menu-enter-active { transition: opacity var(--dur-base) var(--ease-out), transform var(--dur-base) var(--ease-out); }
.menu-leave-active { transition: opacity var(--dur-fast) ease-in; }
.menu-enter-from { opacity: 0; transform: translateY(-8px); }
.menu-leave-to { opacity: 0; }
</style>
