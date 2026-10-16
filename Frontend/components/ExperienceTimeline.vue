<template>
  <ol ref="listRef" class="relative flex flex-col" :class="compact ? 'gap-8' : 'gap-12'">
    <!-- Trilho: desenhado de cima pra baixo conforme o scroll (scaleY, sem animar altura) -->
    <span class="absolute left-[5px] top-2 bottom-2 w-px bg-divider" aria-hidden="true">
      <span ref="progressRef" class="absolute inset-0 bg-primary origin-top" :style="{ transform: drawn ? 'scaleY(1)' : 'scaleY(0)' }"></span>
    </span>

    <li v-for="item in experiences" :key="item.id" class="relative pl-9" data-reveal>
      <span class="timeline-dot absolute left-0 top-[0.4rem]" aria-hidden="true"></span>

      <div class="flex flex-col gap-1.5" :class="compact ? 'md:flex-row md:items-baseline md:gap-6' : ''">
        <span class="text-sm small-caps tracking-wide text-primary font-semibold tabular-nums shrink-0" :class="compact ? 'md:w-32' : ''">
          {{ item.year }}<template v-if="item.endYear !== undefined">–{{ item.endYear ?? t('journey.present') }}</template>
        </span>
        <div class="flex flex-col gap-1 min-w-0">
          <h3 class="title-item">{{ item.title }}</h3>
          <p v-if="item.company" class="text-sm text-muted">{{ item.company }}</p>
          <p v-if="!compact && item.desc" class="text-muted leading-relaxed mt-2 max-w-prose">{{ item.desc }}</p>
        </div>
      </div>
    </li>
  </ol>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, onUnmounted } from 'vue'
import { gsap } from 'gsap'
import type { Experience } from '~/composables/usePortfolioApi'
import { useI18n } from '~/composables/useI18n'

const props = defineProps<{
  experiences: Experience[]
  compact?: boolean
}>()

const { t } = useI18n()
const listRef = ref<HTMLElement | null>(null)
const progressRef = ref<HTMLElement | null>(null)
const drawn = ref(false)
let tween: gsap.core.Tween | null = null

// Liga o desenho do trilho ao scroll quando os itens chegam da API
watch(() => props.experiences.length, async (len) => {
  if (!len || tween || !import.meta.client) return
  await nextTick()
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    drawn.value = true
    return
  }
  const { ScrollTrigger } = await import('gsap/ScrollTrigger')
  gsap.registerPlugin(ScrollTrigger)
  if (!listRef.value || !progressRef.value) return
  tween = gsap.fromTo(progressRef.value, { scaleY: 0 }, {
    scaleY: 1,
    ease: 'none',
    scrollTrigger: { trigger: listRef.value, start: 'top 75%', end: 'bottom 60%', scrub: 0.4 },
  })
}, { immediate: true })

onUnmounted(() => {
  tween?.scrollTrigger?.kill()
  tween?.kill()
})
</script>
