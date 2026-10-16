<template>
  <div class="relative">
    <!-- Multidão desenhada andando no pé da página (assinatura desta página).
         Faixa de altura fixa: as pessoas são desenhadas no tamanho da imagem,
         então a faixa não deve depender da altura do PDF. -->
    <div class="absolute inset-x-0 bottom-0 h-[75vh] min-h-[560px] -z-10 overflow-hidden pointer-events-none" aria-hidden="true">
      <ClientOnly>
        <CrowdCanvas src="/images/peeps/all-peeps.png" class="w-full h-full opacity-90" />
      </ClientOnly>
    </div>

    <div class="container-page pt-12 md:pt-20 pb-24">
      <SectionHeading as="h1" :eyebrow="t('resume.eyebrow')" :title="t('resume.title')">
        <template #action>
          <a v-if="pdfUrl" :href="pdfUrl" target="_blank" rel="noopener" class="btn btn-primary" data-magnetic>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m0 0-4-4m4 4 4-4M4 19h16" /></svg>
            {{ t('resume.download') }}
          </a>
        </template>
      </SectionHeading>

      <!-- Currículo no tamanho natural e a análise ATS ao lado; os dois rolam com a página -->
      <div class="grid gap-8 items-start lg:grid-cols-[minmax(0,48rem)_minmax(0,1fr)]">
        <div class="card overflow-hidden p-2 md:p-3">
          <ClientOnly>
            <VuePdfEmbed v-if="pdfUrl" :source="pdfUrl" class="resume-pdf w-full" />
            <template #fallback>
              <p class="text-muted p-10 text-center" role="status">{{ t('resume.loading') }}</p>
            </template>
          </ClientOnly>
          <p v-if="!pdfUrl" class="text-muted p-10 text-center">{{ t('resume.none') }}</p>
        </div>

      <!-- Análise ATS -->
      <section class="card p-6 md:p-8 flex flex-col gap-8" aria-labelledby="ats-title">
        <div class="flex flex-col gap-4">
          <div class="flex flex-col gap-1.5">
            <h2 id="ats-title" class="title-section">{{ t('resume.atsTitle') }}</h2>
            <p class="text-muted max-w-prose">{{ t('resume.atsLead') }}</p>
          </div>
          <button v-if="pdfUrl" type="button" class="btn btn-secondary self-start" :disabled="analyzing" @click="runAnalysis">
            {{ analyzing ? t('resume.analyzing') : (analysis ? t('resume.analyzeAgain') : t('resume.analyze')) }}
          </button>
        </div>

        <p v-if="analysisError" class="text-sm text-danger" role="alert">{{ analysisError }}</p>

        <div v-if="analysis" class="flex flex-col gap-8">
          <div class="flex items-center gap-5">
            <div class="w-20 h-20 rounded-full border-2 grid place-items-center shrink-0 font-semibold text-2xl tabular-nums" :class="scoreColorClasses">
              {{ analysis.score }}
            </div>
            <div class="flex flex-col gap-1">
              <p class="title-item">{{ scoreLabel }}</p>
              <p class="text-sm text-muted tabular-nums">{{ analysis.word_count }} {{ t('resume.words') }}</p>
            </div>
          </div>

          <div v-for="group in findingGroups" :key="group.key" class="flex flex-col gap-3">
            <h3 class="eyebrow" :class="group.tone">{{ group.label }}</h3>
            <ul class="grid gap-3">
              <li v-for="(f, i) in group.items" :key="i" class="rounded-sm border border-divider bg-surface p-4 flex flex-col gap-1 border-l-2" :class="group.border">
                <span class="text-sm small-caps tracking-wide font-semibold" :class="group.tone">{{ f.category }}</span>
                <span class="text-sm text-text leading-relaxed">{{ f.message }}</span>
              </li>
            </ul>
          </div>

          <div v-if="analysis.positives.length" class="flex flex-col gap-3">
            <h3 class="eyebrow text-success">{{ t('resume.positives') }}</h3>
            <ul class="flex flex-col gap-2">
              <li v-for="(pos, i) in analysis.positives" :key="'p' + i" class="text-sm text-muted flex items-start gap-2">
                <span class="text-success" aria-hidden="true">✓</span> {{ pos }}
              </li>
            </ul>
          </div>
        </div>
      </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import VuePdfEmbed from 'vue-pdf-embed'
import CrowdCanvas from '~/components/ui/CrowdCanvas.vue'
import { useI18n } from '~/composables/useI18n'
import SectionHeading from '~/components/ui/SectionHeading.vue'
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
const { t, lang } = useI18n()
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
  if (s >= 80) return t('resume.score.good')
  if (s >= 50) return t('resume.score.fair')
  return t('resume.score.poor')
})

const findingGroups = computed(() => {
  if (!analysis.value) return []
  return [
    { key: 'critical', label: t('resume.critical'), items: analysis.value.critical, tone: 'text-danger', border: 'border-l-danger' },
    { key: 'suggestions', label: t('resume.suggestions'), items: analysis.value.suggestions, tone: 'text-warning', border: 'border-l-warning' },
  ].filter(g => g.items.length)
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
    analysisError.value = e?.data?.detail || t('resume.error')
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
<style scoped>
/* Páginas do PDF separadas por um respiro, com a borda do card em volta */
.resume-pdf :deep(.vue-pdf-embed__page) {
  margin-bottom: 0.75rem;
  border-radius: 8px;
  overflow: hidden;
}
.resume-pdf :deep(.vue-pdf-embed__page:last-child) {
  margin-bottom: 0;
}
</style>
