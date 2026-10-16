<template>
  <div ref="pageRef" class="section pt-12 md:pt-20">
    <div class="container-page">
      <SectionHeading as="h1" :eyebrow="t('work.eyebrow')" :title="t('work.pageTitle')" :lead="t('work.pageLead')" />

      <!-- Filtros: categorias reais dos projetos, na ordem em que mais aparecem -->
      <div class="flex flex-wrap gap-2 mb-10" role="group" :aria-label="t('work.pageTitle')" data-reveal>
        <button
          v-for="tab in tabs"
          :key="tab.id"
          type="button"
          class="filter"
          :aria-pressed="activeFilter === tab.id"
          @click="setFilter(tab.id)"
        >
          {{ tab.label }}
          <span class="tabular-nums text-xs opacity-70">{{ tab.count }}</span>
        </button>
      </div>

      <div ref="gridRef" class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="(project, i) in filteredProjects"
          :key="project.id"
          data-reveal
          :class="i === 0 && activeFilter === 'all' && filteredProjects.length > 2 ? 'sm:col-span-2' : ''"
        >
          <ProjectCard
            :project="project"
            :to="`${base}/projects/${project.id}`"
            :large="i === 0 && activeFilter === 'all' && filteredProjects.length > 2"
          />
        </div>
      </div>
      <p v-if="filteredProjects.length === 0" class="py-16 text-center text-muted">{{ t('work.empty') }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { gsap } from 'gsap'
import { useRoute } from 'vue-router'
import { usePortfolioApi } from '~/composables/usePortfolioApi'
import { useI18n } from '~/composables/useI18n'
import { useReveal } from '~/composables/useReveal'
import SectionHeading from '~/components/ui/SectionHeading.vue'
import ProjectCard from '~/components/ProjectCard.vue'

const { projects, loadData } = usePortfolioApi()
const { t } = useI18n()
const route = useRoute()
const base = computed(() => `/${route.params.user_id}`)

const activeFilter = ref('all')

// O mais curtido abre a lista; o resto segue do mais recente pro mais antigo
const ordered = computed(() => {
  const list = [...projects.value]
  const topIndex = list.reduce((best, p, i) => (p.likes > list[best].likes ? i : best), 0)
  if (list.length && list[topIndex].likes > 0) list.unshift(...list.splice(topIndex, 1))
  return list
})

const tabs = computed(() => {
  const counts = new Map<string, number>()
  projects.value.forEach(p => p.categories.forEach(c => counts.set(c, (counts.get(c) || 0) + 1)))
  const cats = [...counts.entries()].sort((a, b) => b[1] - a[1]).map(([id, count]) => ({ id, label: id, count }))
  return [{ id: 'all', label: t('work.filterAll'), count: projects.value.length }, ...cats]
})

const filteredProjects = computed(() =>
  activeFilter.value === 'all' ? ordered.value : ordered.value.filter(p => p.categories.includes(activeFilter.value)),
)

const pageRef = ref<HTMLElement | null>(null)
const gridRef = ref<HTMLElement | null>(null)
useReveal(pageRef, () => projects.value.length)

async function setFilter(id: string) {
  if (id === activeFilter.value) return
  activeFilter.value = id
  await nextTick()
  if (!gridRef.value) return
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const items = Array.from(gridRef.value.children)
  items.forEach(el => el.setAttribute('data-revealed', ''))
  gsap.fromTo(items,
    reduce ? { opacity: 0 } : { opacity: 0, y: 16 },
    { opacity: 1, y: 0, duration: reduce ? 0.2 : 0.32, ease: 'power3.out', stagger: 0.04, clearProps: 'opacity,transform' },
  )
}

onMounted(() => {
  loadData(route.params.user_id as string)
})
</script>

<style scoped>
.filter {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  border-radius: 999px;
  border: 1px solid var(--color-border);
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  font-variant: small-caps;
  letter-spacing: 0.05em;
  color: var(--color-muted);
  transition: background-color var(--dur-fast) var(--ease-out), color var(--dur-fast) var(--ease-out), border-color var(--dur-fast) var(--ease-out);
}
.filter:hover { color: var(--color-text); border-color: var(--color-primary); }
.filter:active { transform: scale(0.97); }
.filter[aria-pressed='true'] {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-background);
}
</style>
