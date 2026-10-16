<template>
  <div class="project-cover relative overflow-hidden bg-surface" :style="{ '--tone': `var(${tone})` }">
    <img
      v-if="image"
      :src="image"
      :alt="''"
      loading="lazy"
      class="absolute inset-0 w-full h-full object-cover"
    />
    <template v-else>
      <!-- Hachura em linha, a mesma do avatar, na cor da categoria -->
      <svg class="absolute inset-0 w-full h-full" aria-hidden="true" preserveAspectRatio="none">
        <defs>
          <pattern :id="patternId" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">
            <line x1="0" y1="0" x2="0" y2="9" stroke="var(--tone)" stroke-width="1.2" />
          </pattern>
        </defs>
        <rect class="hatch" x="-10%" y="0" width="120%" height="100%" :fill="`url(#${patternId})`" />
      </svg>
      <span
        class="relative z-[1] rounded-sm bg-surface px-3 py-0.5 font-bold small-caps tracking-wide leading-tight"
        :class="large ? 'text-5xl md:text-6xl' : 'text-4xl'"
        :style="{ color: 'var(--tone)' }"
        aria-hidden="true"
      >{{ initials }}</span>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, useId } from 'vue'

const props = defineProps<{
  title: string
  categories?: string[]
  image?: string | null
  large?: boolean
}>()

const patternId = `hatch-${useId()}`

// Cor da categoria principal (tokens da paleta ativa, então segue tema e modo)
const TONES: Record<string, string> = {
  mobile: '--color-accent-1',
  frontend: '--color-primary',
  backend: '--color-secondary',
  fullstack: '--color-secondary',
  datascience: '--color-accent-3',
  gamedev: '--color-accent-2',
}
const tone = computed(() => {
  const first = (props.categories?.[0] || '').toLowerCase()
  return TONES[first] || '--color-muted'
})

// Iniciais das duas primeiras palavras com letra (ignora "-", ":", parênteses)
const initials = computed(() =>
  props.title
    .replace(/[^\p{L}\p{N}\s]/gu, ' ')
    .split(/\s+/)
    .filter(w => /\p{L}/u.test(w))
    .slice(0, 2)
    .map(w => w[0].toUpperCase())
    .join(''),
)
</script>

<style scoped>
.project-cover {
  display: grid;
  place-items: center;
}
.hatch {
  opacity: 0.55;
  transition: transform var(--dur-slow) var(--ease-out);
}
</style>

<style>
/* Fora do bloco scoped de propósito: com :global() o Vue compilava só ".group:hover"
   e todo elemento com a classe "group" (ex: os botões da órbita) andava 12px pro lado.
   Aqui a regra só alcança a hachura da capa (MASTER.md: a hachura desliza no hover). */
.group:hover .project-cover .hatch,
.group:focus-within .project-cover .hatch {
  transform: translateX(-12px);
}
</style>
