<template>
  <div class="min-h-screen font-body antialiased flex flex-col justify-between relative">
    <ClientOnly>
      <TerminalLoadingScreen
        v-if="showLoader && currentUsername"
        :username="currentUsername"
        class="transition-opacity duration-500"
        :class="fadingOut ? 'opacity-0 pointer-events-none' : 'opacity-100'"
        @complete="onAnimationComplete"
      />
    </ClientOnly>
    <a href="#main" class="skip-link">{{ t('nav.skip') }}</a>
    <AppHeader />
    <main id="main" class="flex-1 pt-[4.5rem]">
      <slot />
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { usePortfolioApi } from '~/composables/usePortfolioApi'
import TerminalLoadingScreen from '~/components/ui/TerminalLoadingScreen.vue'
import { useI18n } from '~/composables/useI18n'

const { t } = useI18n()

const route = useRoute()
const { loading } = usePortfolioApi()

const currentUsername = computed(() => (route.params.user_id as string) || '')

const LOADER_SESSION_KEY = 'portfolio-loader-shown'

const showLoader = ref(true)
const fadingOut = ref(false)
const animationDone = ref(false)

const dataReady = computed(() => !loading.value)
const readyToHide = computed(() => animationDone.value && dataReady.value)

onMounted(() => {
  if (sessionStorage.getItem(LOADER_SESSION_KEY)) {
    showLoader.value = false
  }
})

watch(readyToHide, (val) => {
  if (val) {
    fadingOut.value = true
    sessionStorage.setItem(LOADER_SESSION_KEY, '1')
    setTimeout(() => {
      showLoader.value = false
    }, 500)
  }
})

function onAnimationComplete() {
  animationDone.value = true
}
</script>
