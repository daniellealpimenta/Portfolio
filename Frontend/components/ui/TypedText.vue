<template>
  <!-- O texto completo fica para leitores de tela e para o SSR; só a cópia visual é "digitada". -->
  <span class="typed">
    <span class="sr-only">{{ text }}</span>
    <span aria-hidden="true">{{ shown }}<span class="cursor-blink"></span></span>
  </span>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'

const props = withDefaults(defineProps<{ text: string; speed?: number; delay?: number }>(), {
  speed: 45,  // ms por letra (MASTER.md)
  delay: 250,
})

// No servidor (e sem JS) o texto já aparece inteiro; a digitação roda uma vez no cliente.
const shown = ref(props.text)
let timer: ReturnType<typeof setTimeout> | null = null

function stop() {
  if (timer) clearTimeout(timer)
  timer = null
}

function play() {
  stop()
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    shown.value = props.text
    return
  }
  shown.value = ''
  let i = 0
  const step = () => {
    i++
    shown.value = props.text.slice(0, i)
    if (i < props.text.length) timer = setTimeout(step, props.speed)
  }
  timer = setTimeout(step, props.delay)
}

onMounted(play)
// O texto real chega da API depois do mount (ou muda de idioma): digita de novo.
watch(() => props.text, (next, prev) => { if (next !== prev) play() })
onUnmounted(stop)
</script>
