<template>
  <main class="max-w-4xl mx-auto px-6 pb-24" ref="containerRef">

    <!-- ABOUT SECTION -->
    <section id="about" class="flex flex-col md:flex-row items-start gap-12 md:gap-16 mb-24 pt-12">
      <!-- Left side: Avatar + Currículo -->
      <div ref="avatarRef" class="flex flex-col items-center gap-6 shrink-0 w-full md:w-auto">
        <div class="w-48 h-48 md:w-64 md:h-64 rounded-full overflow-hidden bg-surface border-4 border-text flex items-center justify-center">
          <img v-if="user?.avatar_url" :src="fileUrl(user.avatar_url)" alt="Avatar" class="w-full h-full object-cover rounded-full border-4 border-background" />
          <svg v-else width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="8" r="4"/><path d="M4 20c1-4 4-6 8-6s7 2 8 6"/></svg>
        </div>
        <button @click="handleDownload" class="font-display uppercase text-sm px-8 py-3 rounded-xl border-2 border-text text-text hover:bg-text hover:text-background transition-colors flex items-center justify-center gap-2 font-semibold min-w-[200px]">
          <PhArrowLineDown :size="18" />
          CURRÍCULO
        </button>
      </div>

      <!-- Right side: Title + Desc -->
      <div ref="aboutInfoRef" class="pt-4 md:pt-8 w-full">
        <h1 class="text-3xl md:text-5xl font-display font-bold uppercase text-text mb-6 tracking-wide leading-tight">
          {{ user?.name || 'Daniel' }}
        </h1>
        <div class="prose prose-invert max-w-none text-text leading-relaxed whitespace-pre-line text-base md:text-lg">
          {{ user?.description || 'Carregando informações do servidor...' }}
        </div>
      </div>
    </section>

    <section id="resume" class="mb-24" ref="timelineSectionRef">
      <div class="flex items-center gap-4 mb-10">
        <PhBriefcase :size="40" weight="fill" class="text-text shrink-0" title="Experiências" />
        <h2 class="font-display text-2xl md:text-3xl font-semibold uppercase tracking-wider text-text">Experiências</h2>
      </div>
      <div id="experiences-timeline" class="pl-4">
        <ExperienceTimeline :experiences="experiences" />
      </div>
    </section>

    <section class="mb-24" ref="certSectionRef">
      <div class="flex items-center gap-4 mb-10">
        <PhGraduationCap :size="40" weight="fill" class="text-text shrink-0" title="Certificados" />
        <h2 class="font-display text-2xl md:text-3xl font-semibold uppercase tracking-wider text-text">Certificados</h2>
      </div>
      <CertificateList :certificates="certificates" />
    </section>

    <section class="mb-24" ref="orbitalSectionRef">
      <div class="flex items-center gap-4 mb-12">
        <PhSeal :size="40" weight="fill" class="text-text shrink-0" title="Valores e Hobbies" />
        <h2 class="font-display text-2xl md:text-3xl font-semibold uppercase tracking-wider text-text">Valores e Hobbies</h2>
      </div>
      <RadialOrbitalTimeline :timeline-data="orbitalData" />
    </section>

    <section class="mb-24" ref="hireSectionRef">
      <div class="flex items-center gap-4 mb-8">
        <PhMagnifyingGlass :size="40" class="text-text shrink-0" title="Por que me contratar?" />
        <h2 class="font-display text-2xl md:text-3xl font-semibold uppercase tracking-wider text-text">Por que me contratar?</h2>
      </div>
      <div class="prose prose-invert max-w-none text-text leading-relaxed text-base md:text-lg">
        <p>Estou sempre em busca de desafios que me permitam aprender novas tecnologias e aplicá-las para criar soluções reais e impactantes. Minha experiência em diferentes áreas me permite ter uma visão sistêmica dos projetos em que me envolvo.</p>
        <p class="mt-4">Minha dedicação, resiliência e foco na entrega de valor são os pilares que me guiam profissionalmente, sempre trabalhando de forma colaborativa e com atenção aos detalhes.</p>
      </div>
    </section>

  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { gsap } from 'gsap'
import { PhCalendar, PhCode, PhFileText, PhUser, PhClock, PhBriefcase, PhGraduationCap, PhSeal, PhMagnifyingGlass, PhArrowLineDown } from '@phosphor-icons/vue'
import { usePortfolioApi } from '~/composables/usePortfolioApi'
import { useFileUrl } from '~/composables/useFileUrl'
import RadialOrbitalTimeline, { type TimelineItem } from '~/components/ui/RadialOrbitalTimeline.vue'
import { useLanguage } from '~/composables/useLanguage'
import { useRoute } from 'vue-router'

const route = useRoute()
const { user, experiences, certificates, loadData } = usePortfolioApi()
const { lang } = useLanguage()
const fileUrl = useFileUrl()

async function handleDownload() {
  const url = fileUrl(lang.value === 'en' ? user.value?.curriculum_en_url : user.value?.curriculum_url)
  if (!url || url === '#') return
  
  try {
    const response = await fetch(url)
    const blob = await response.blob()
    const blobUrl = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = blobUrl
    a.download = `Curriculo_Daniel_${lang.value.toUpperCase()}.pdf`
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(blobUrl)
  } catch (error) {
    console.error('Download failed, opening in new tab', error)
    window.open(url, '_blank')
  }
}

const orbitalData: TimelineItem[] = [
  {
    id: 1,
    title: "Planejamento & TCC",
    date: "2026",
    content: "Desenvolvimento do AgroBot, projeto final do curso de Engenharia de Software em Swift.",
    category: "Engenharia",
    icon: PhCalendar,
    relatedIds: [2, 3],
    status: "in-progress",
    energy: 100,
  },
  {
    id: 2,
    title: "Dev. Mobile Swift",
    date: "2025-2026",
    content: "Construção de aplicativos iOS nativos com Swift, SwiftUI e SwiftData na Apple Developer Academy.",
    category: "Mobile",
    icon: PhCode,
    relatedIds: [1, 4],
    status: "completed",
    energy: 95,
  },
  {
    id: 3,
    title: "Sistemas Web & APIs",
    date: "2024-2025",
    content: "Reconstrução de sistemas em Angular, APIs FastAPI/Node.js e automação de processos.",
    category: "Backend",
    icon: PhFileText,
    relatedIds: [1, 5],
    status: "completed",
    energy: 90,
  },
  {
    id: 4,
    title: "UI/UX & Protótipos",
    date: "2024",
    content: "Design de interfaces no Figma com foco em experiência do usuário e usabilidade.",
    category: "Design",
    icon: PhUser,
    relatedIds: [2],
    status: "completed",
    energy: 85,
  },
  {
    id: 5,
    title: "Graduação Eng. Software",
    date: "2023-Presente",
    content: "Formação acadêmica unindo engenharia de sistemas, bancos de dados e governança de TI.",
    category: "Acadêmico",
    icon: PhClock,
    relatedIds: [3],
    status: "completed",
    energy: 80,
  },
]

const containerRef = ref<HTMLElement | null>(null)
const avatarRef = ref<HTMLElement | null>(null)
const aboutInfoRef = ref<HTMLElement | null>(null)
const timelineSectionRef = ref<HTMLElement | null>(null)
const certSectionRef = ref<HTMLElement | null>(null)
const orbitalSectionRef = ref<HTMLElement | null>(null)
const hireSectionRef = ref<HTMLElement | null>(null)

useGsap(containerRef, () => {
  if (avatarRef.value) gsap.fromTo(avatarRef.value, { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.6 })
  if (aboutInfoRef.value) gsap.fromTo(aboutInfoRef.value, { opacity: 0, x: 20 }, { opacity: 1, x: 0, duration: 0.6, delay: 0.15 })

  if (timelineSectionRef.value) {
    gsap.fromTo(timelineSectionRef.value, { opacity: 0, y: 30 }, {
      opacity: 1, y: 0, duration: 0.7,
      scrollTrigger: { trigger: timelineSectionRef.value, start: 'top 85%' }
    })
  }

  if (certSectionRef.value) {
    gsap.fromTo(certSectionRef.value, { opacity: 0, y: 30 }, {
      opacity: 1, y: 0, duration: 0.7,
      scrollTrigger: { trigger: certSectionRef.value, start: 'top 85%' }
    })
  }

  if (orbitalSectionRef.value) {
    gsap.fromTo(orbitalSectionRef.value, { opacity: 0, y: 30 }, {
      opacity: 1, y: 0, duration: 0.7,
      scrollTrigger: { trigger: orbitalSectionRef.value, start: 'top 85%' }
    })
  }

  if (hireSectionRef.value) {
    gsap.fromTo(hireSectionRef.value, { opacity: 0, y: 30 }, {
      opacity: 1, y: 0, duration: 0.7,
      scrollTrigger: { trigger: hireSectionRef.value, start: 'top 85%' }
    })
  }
})

onMounted(() => {
  loadData(route.params.user_id as string)
})
</script>
