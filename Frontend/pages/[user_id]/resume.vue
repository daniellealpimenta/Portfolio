<template>
  <div class="relative min-h-[150vh]">
    <!-- Fundo full-bleed da página (não fica preso à largura/altura do card do currículo) -->
    <div class="absolute inset-0 -z-10 overflow-hidden pointer-events-none">
      <ClientOnly>
        <CrowdCanvas src="/images/peeps/all-peeps.png" class="w-full h-full opacity-90" />
      </ClientOnly>
    </div>

    <div class="max-w-7xl mx-auto px-4 md:px-6 pt-0 h-[calc(110vh-8rem)] flex flex-col">
      <div class="flex items-center justify-between mb-4 px-2">
        <h1 class="text-2xl font-display small-caps text-text">Meu Currículo</h1>
      </div>
      <div class="flex-1 w-full border border-border rounded-2xl overflow-y-auto bg-surface flex justify-center p-4 md:p-8">
        <ClientOnly>
          <VuePdfEmbed v-if="pdfUrl" :source="pdfUrl" class="w-full max-w-3xl drop-shadow-2xl" />
          <template #fallback>
            <div class="text-muted p-10 flex items-center justify-center animate-pulse">Carregando PDF...</div>
          </template>
        </ClientOnly>
        <div v-if="!pdfUrl" class="p-6 text-muted flex items-center justify-center h-full w-full">
          Nenhum currículo cadastrado para este idioma.
        </div>
      </div>
    </div>

    <!-- Análise ATS -->
    <div class="max-w-7xl mx-auto px-4 md:px-6 pb-24 pt-10">
      <div class="border border-border rounded-2xl bg-surface p-6 md:p-8">
        <div class="flex items-center justify-between flex-wrap gap-4 mb-2">
          <div>
            <h2 class="text-xl font-display small-caps text-text">Análise ATS</h2>
            <p class="text-sm text-muted mt-1">Uma checagem automática de como esse currículo se sairia em sistemas de rastreamento de candidatos (ATS).</p>
          </div>
          <button
            v-if="pdfUrl"
            type="button"
            :disabled="analyzing"
            @click="runAnalysis"
            class="shrink-0 px-5 py-2.5 rounded-full bg-primary text-background text-sm font-display small-caps tracking-wide font-semibold hover:opacity-90 transition disabled:opacity-50"
          >
            {{ analyzing ? 'Analisando...' : (analysis ? 'Analisar novamente' : 'Analisar currículo') }}
          </button>
        </div>

        <p v-if="analysisError" class="text-sm text-danger mt-4">{{ analysisError }}</p>

        <div v-if="analysis" class="mt-6 space-y-8">
          <!-- Nota -->
          <div class="flex items-center gap-4">
            <div
              class="w-20 h-20 rounded-full border-4 flex items-center justify-center shrink-0 font-display font-bold text-2xl"
              :class="scoreColorClasses"
            >
              {{ analysis.score }}
            </div>
            <div>
              <p class="font-display small-caps text-text font-semibold">{{ scoreLabel }}</p>
              <p class="text-xs text-muted mt-1">{{ analysis.word_count }} palavras extraídas do PDF</p>
            </div>
          </div>

          <!-- Críticos -->
          <div v-if="analysis.critical.length > 0">
            <h3 class="text-sm font-display small-caps text-danger font-semibold mb-3 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-danger"></span> Críticos
            </h3>
            <div class="space-y-2">
              <div v-for="(f, i) in analysis.critical" :key="'c'+i" class="bg-danger/10 border border-danger/20 rounded-xl p-4">
                <p class="text-xs font-display small-caps text-danger font-semibold mb-1">{{ f.category }}</p>
                <p class="text-sm text-text leading-relaxed">{{ f.message }}</p>
              </div>
            </div>
          </div>

          <!-- Sugestões -->
          <div v-if="analysis.suggestions.length > 0">
            <h3 class="text-sm font-display small-caps text-warning font-semibold mb-3 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-warning"></span> Sugestões
            </h3>
            <div class="space-y-2">
              <div v-for="(f, i) in analysis.suggestions" :key="'s'+i" class="bg-warning/10 border border-warning/20 rounded-xl p-4">
                <p class="text-xs font-display small-caps text-warning font-semibold mb-1">{{ f.category }}</p>
                <p class="text-sm text-text leading-relaxed">{{ f.message }}</p>
              </div>
            </div>
          </div>

          <!-- Pontos positivos -->
          <div v-if="analysis.positives.length > 0">
            <h3 class="text-sm font-display small-caps text-success font-semibold mb-3 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-success"></span> Pontos positivos
            </h3>
            <ul class="space-y-1.5">
              <li v-for="(p, i) in analysis.positives" :key="'p'+i" class="text-sm text-muted flex items-start gap-2">
                <span class="text-success mt-0.5">✓</span> {{ p }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import VuePdfEmbed from 'vue-pdf-embed'
import CrowdCanvas from '~/components/ui/CrowdCanvas.vue'
import { useLanguage } from '~/composables/useLanguage'
import { usePortfolioApi } from '~/composables/usePortfolioApi'
import { useFileUrl } from '~/composables/useFileUrl'
import { useRoute } from 'vue-router'

interface ResumeFinding {
  category: string
  message: string
}
interface ResumeAnalysis {
  score: number
  word_count: number
  has_extractable_text: boolean
  critical: ResumeFinding[]
  suggestions: ResumeFinding[]
  positives: string[]
}

const API_BASE_URL = useRuntimeConfig().public.apiBase

const route = useRoute()
const { lang } = useLanguage()
const { user, loadData } = usePortfolioApi()

const fileUrl = useFileUrl()
const pdfUrl = computed(() => fileUrl(lang.value === 'en' ? user.value?.curriculum_en_url : user.value?.curriculum_url))

const analysis = ref<ResumeAnalysis | null>(null)
const analyzing = ref(false)
const analysisError = ref('')

const scoreColorClasses = computed(() => {
  const s = analysis.value?.score ?? 0
  if (s >= 80) return 'border-success text-success'
  if (s >= 50) return 'border-warning text-warning'
  return 'border-danger text-danger'
})

const scoreLabel = computed(() => {
  const s = analysis.value?.score ?? 0
  if (s >= 80) return 'Currículo bem otimizado para ATS'
  if (s >= 50) return 'Dá pra melhorar em alguns pontos'
  return 'Precisa de atenção antes de aplicar'
})

async function runAnalysis() {
  if (!user.value?.id) return
  analyzing.value = true
  analysisError.value = ''
  try {
    analysis.value = await $fetch<ResumeAnalysis>(`${API_BASE_URL}/resume-analysis/${user.value.id}`, {
      params: { lang: lang.value }
    })
  } catch (e: any) {
    analysis.value = null
    analysisError.value = e?.data?.detail || 'Não foi possível analisar o currículo agora. Tente de novo em alguns instantes.'
  } finally {
    analyzing.value = false
  }
}

// Se trocar o idioma do currículo, a análise anterior não vale mais pro PDF atual
watch(lang, () => {
  analysis.value = null
  analysisError.value = ''
})

onMounted(() => {
  loadData(route.params.user_id as string)
})
</script>