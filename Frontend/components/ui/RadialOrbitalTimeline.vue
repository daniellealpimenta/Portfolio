<template>
  <!-- Em telas estreitas a órbita não cabe com os rótulos: vira uma lista -->
  <ul v-if="narrow" ref="listRef" class="flex flex-col gap-4">
    <li v-for="item in timelineData" :key="item.id" class="card p-5 flex gap-4">
      <span class="w-11 h-11 shrink-0 rounded-full grid place-items-center border border-border text-primary">
        <component :is="item.icon" :size="18" weight="fill" aria-hidden="true" />
      </span>
      <div class="flex flex-col gap-1 min-w-0">
        <div class="flex flex-wrap items-center gap-x-3 gap-y-1">
          <h3 class="title-item">{{ item.title }}</h3>
          <span class="text-sm text-muted tabular-nums">{{ item.date }}</span>
        </div>
        <p class="text-sm text-muted leading-relaxed">{{ item.content }}</p>
      </div>
    </li>
  </ul>

  <div
    v-else
    ref="containerRef"
    class="relative w-full flex items-center justify-center"
    :style="{ height: `${radius * 2 + 220}px` }"
    @click="handleContainerClick"
  >
    <div ref="orbitRef" class="absolute inset-0 flex items-center justify-center">
      <!-- Centro: as iniciais, estático (sem pulso/ping) -->
      <div class="absolute w-16 h-16 rounded-full border border-divider bg-surface grid place-items-center z-10" aria-hidden="true">
        <span class="w-3 h-3 rounded-full bg-primary"></span>
      </div>

      <!-- Órbita -->
      <div
        class="absolute rounded-full border border-dashed border-divider"
        :style="{ width: `${radius * 2}px`, height: `${radius * 2}px` }"
        aria-hidden="true"
      ></div>

      <!-- Nós -->
      <div
        v-for="(item, index) in timelineData"
        :key="item.id"
        class="node absolute"
        :style="getNodeStyle(index, timelineData.length, item.id)"
      >
        <button
          type="button"
          class="group relative flex flex-col items-center gap-2"
          :aria-expanded="!!expandedItems[item.id]"
          @click.stop="toggleItem(item.id)"
        >
          <span
            class="w-11 h-11 rounded-full grid place-items-center border transition-colors duration-fast ease-out"
            :class="expandedItems[item.id]
              ? 'bg-primary text-background border-primary'
              : isRelatedToActive(item.id)
                ? 'bg-surface text-primary border-primary'
                : 'bg-surface text-text border-border group-hover:border-primary group-hover:text-primary'"
          >
            <component :is="item.icon" :size="18" weight="fill" aria-hidden="true" />
          </span>
          <span
            class="whitespace-nowrap text-sm font-semibold small-caps tracking-wide transition-colors duration-fast ease-out"
            :class="expandedItems[item.id] ? 'text-primary' : 'text-text group-hover:text-primary'"
          >{{ item.title }}</span>
        </button>

        <!-- Detalhe do nó -->
        <Transition name="pop">
          <div
            v-if="expandedItems[item.id]"
            class="card absolute top-[5.5rem] left-1/2 -translate-x-1/2 w-72 p-5 z-50 text-left flex flex-col gap-2"
            @click.stop
          >
            <div class="flex items-center justify-between gap-3">
              <span class="chip" :class="item.status === 'in-progress' ? 'text-primary border-primary' : ''">{{ statusLabel(item.status) }}</span>
              <span class="text-sm text-muted tabular-nums">{{ item.date }}</span>
            </div>
            <h4 class="title-item">{{ item.title }}</h4>
            <p class="text-sm text-muted leading-relaxed">{{ item.content }}</p>

            <div v-if="item.relatedIds.length > 0" class="pt-3 mt-1 border-t border-divider flex flex-col gap-2">
              <span class="text-xs small-caps tracking-wide text-muted">{{ lang === 'en' ? 'Related' : 'Relacionados' }}</span>
              <div class="flex flex-wrap gap-1.5">
                <button
                  v-for="relId in item.relatedIds"
                  :key="relId"
                  type="button"
                  class="chip hover:border-primary hover:text-primary transition-colors duration-fast ease-out"
                  @click.stop="toggleItem(relId)"
                >
                  {{ getRelatedItemTitle(relId) }} →
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, type Component } from 'vue'
import { useI18n } from '~/composables/useI18n'

export interface TimelineItem {
  id: number
  title: string
  date: string
  content: string
  category: string
  icon: Component
  relatedIds: number[]
  status: 'completed' | 'in-progress' | 'pending'
  energy?: number
}

const props = defineProps<{
  timelineData: TimelineItem[]
}>()

const { lang } = useI18n()

const expandedItems = ref<Record<number, boolean>>({})
// Parada por padrão (MASTER.md: nada em loop). Só gira, uma vez, para trazer o nó clicado ao topo.
const rotationAngle = ref<number>(-90)
const activeNodeId = ref<number | null>(null)
const containerRef = ref<HTMLDivElement | null>(null)
const orbitRef = ref<HTMLDivElement | null>(null)
const listRef = ref<HTMLUListElement | null>(null)

// Raio acompanha a largura (a órbita fixa de 512px estourava no celular)
const radius = ref(256)
const narrow = ref(false)
function measure() {
  const w = (containerRef.value || listRef.value)?.parentElement?.clientWidth || window.innerWidth
  narrow.value = w < 640
  radius.value = Math.max(160, Math.min(256, w / 2 - 110))
}
onMounted(() => {
  measure()
  window.addEventListener('resize', measure)
})
onUnmounted(() => window.removeEventListener('resize', measure))

function handleContainerClick(e: MouseEvent) {
  if (e.target === containerRef.value || e.target === orbitRef.value) {
    expandedItems.value = {}
    activeNodeId.value = null
  }
}

function toggleItem(id: number) {
  if (expandedItems.value[id]) {
    expandedItems.value = {}
    activeNodeId.value = null
    return
  }
  expandedItems.value = { [id]: true }
  activeNodeId.value = id
  centerViewOnNode(id)
}

function centerViewOnNode(nodeId: number) {
  const index = props.timelineData.findIndex(item => item.id === nodeId)
  if (index === -1) return
  const targetAngle = (index / props.timelineData.length) * 360
  // Menor caminho até o topo (-90°), pra não dar a volta inteira
  let next = -90 - targetAngle
  while (next - rotationAngle.value > 180) next -= 360
  while (rotationAngle.value - next > 180) next += 360
  rotationAngle.value = next
}

function getNodeStyle(index: number, total: number, itemId: number) {
  const radian = (((index / total) * 360 + rotationAngle.value) * Math.PI) / 180
  const x = radius.value * Math.cos(radian)
  const y = radius.value * Math.sin(radian)
  const dimmed = activeNodeId.value !== null && !expandedItems.value[itemId] && !isRelatedToActive(itemId)
  return {
    transform: `translate(${x}px, ${y}px)`,
    zIndex: expandedItems.value[itemId] ? 200 : 100,
    opacity: dimmed ? 0.45 : 1,
  }
}

function isRelatedToActive(itemId: number): boolean {
  if (!activeNodeId.value) return false
  return props.timelineData.find(i => i.id === activeNodeId.value)?.relatedIds.includes(itemId) ?? false
}

function getRelatedItemTitle(id: number): string {
  return props.timelineData.find(item => item.id === id)?.title ?? String(id)
}

function statusLabel(status: TimelineItem['status']) {
  const en = lang.value === 'en'
  if (status === 'completed') return en ? 'completed' : 'concluído'
  if (status === 'in-progress') return en ? 'in progress' : 'em andamento'
  return en ? 'planned' : 'planejado'
}
</script>

<style scoped>
/* Girar até o nó clicado: transform + opacidade, 560ms power3.out */
.node {
  transition: transform var(--dur-slow) var(--ease-out), opacity var(--dur-base) var(--ease-out);
}
.pop-enter-active { transition: opacity var(--dur-base) var(--ease-out), transform var(--dur-base) var(--ease-out); }
.pop-leave-active { transition: opacity var(--dur-fast) ease-in; }
.pop-enter-from { opacity: 0; transform: translate(-50%, 8px); }
.pop-leave-to { opacity: 0; }
</style>
