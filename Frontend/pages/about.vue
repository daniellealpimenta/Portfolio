<template>
  <main class="max-w-4xl mx-auto px-6 pb-24" ref="containerRef">

    <!-- ABOUT SECTION -->
    <section id="about" class="flex flex-col md:flex-row items-start gap-8 mb-16">
      <div ref="avatarRef" class="flex flex-col items-center gap-3 shrink-0">
        <div class="w-32 h-32 rounded-full overflow-hidden bg-surface border border-border flex items-center justify-center">
          <img v-if="user?.avatar_url" :src="fileUrl(user.avatar_url)" alt="Avatar" class="w-full h-full object-cover" />
          <svg v-else width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#8FA0C4" stroke-width="1.4"><circle cx="12" cy="8" r="4"/><path d="M4 20c1-4 4-6 8-6s7 2 8 6"/></svg>
        </div>
        <button @click="handleDownload" data-magnetic class="text-meta text-xs px-4 py-2 rounded-full border border-border text-muted hover:text-text transition inline-flex items-center gap-1.5">
          <PhArrowLineDown :size="14" /> Currículo PDF
        </button>
      </div>
      <div ref="aboutInfoRef">
        <h1 class="text-h1 mb-3">{{ user?.name || 'Daniel' }}</h1>
        <p class="text-body text-muted whitespace-pre-line mb-4">
          {{ user?.description || 'Carregando informações do servidor...' }}
        </p>
      </div>
    </section>

    <!-- RADIAL ORBITAL TIMELINE / SKILLS ORBIT -->
    <section class="mb-20" ref="orbitalSectionRef">
      <div class="mb-6 text-center">
        <span class="eyebrow">Visualização Interativa 3D</span>
        <h2 class="font-display text-2xl small-caps text-text font-semibold mt-1">Mapa de Trajetória & Habilidades</h2>
        <p class="text-xs text-muted mt-1">Clique nos nós para expandir detalhes, níveis de domínio e conexões.</p>
      </div>
      <RadialOrbitalTimeline :timeline-data="orbitalData" />
    </section>

    <!-- EXPERIENCE TIMELINE SECTION -->
    <section id="resume" class="mb-20" ref="timelineSectionRef">
      <h2 class="font-display text-2xl small-caps text-text mb-8 font-semibold">Linha do Tempo de Experiência</h2>
      <div id="experiences-timeline">
        <ExperienceTimeline :experiences="experiences" />
      </div>
    </section>

    <!-- CERTIFICATES SECTION -->
    <section ref="certSectionRef" class="mb-20">
      <div class="flex items-center gap-2 mb-8">
        <PhGraduationCap :size="28" weight="fill" class="text-text" />
        <h2 class="font-display text-2xl small-caps text-text font-semibold">Certificados & Cursos</h2>
      </div>
      <CertificateList :certificates="certificates" />
    </section>

    <!-- VALORES & POR QUE ME CONTRATAR -->
    <section class="grid md:grid-cols-2 gap-12" ref="extraSectionRef">
      <!-- VALORES -->
      <div>
        <div class="flex items-center gap-2 mb-6">
          <PhSeal :size="28" weight="fill" class="text-text" />
          <h2 class="font-display text-2xl small-caps text-text font-semibold">Valores e Hobbies</h2>
        </div>
        <p class="text-body text-muted leading-relaxed">
          Acredito que a tecnologia deve simplificar a vida e resolver problemas reais. Fora da tela, valorizo a criatividade, aprendizado contínuo e colaboração em equipe. Meus hobbies incluem explorar novas ferramentas de design, ler sobre empreendedorismo e participar de comunidades open-source.
        </p>
      </div>

      <!-- POR QUE ME CONTRATAR -->
      <div>
        <div class="flex items-center gap-2 mb-6">
          <PhMagnifyingGlass :size="28" class="text-text" />
          <h2 class="font-display text-2xl small-caps text-text font-semibold">Por que me contratar?</h2>
        </div>
        <p class="text-body text-muted leading-relaxed mb-4">
          Combino disciplina técnica com comunicação clara: cada projeto começa com um entendimento honesto do problema, segue com decisões documentadas e termina com um sistema que o cliente entende e consegue manter.
        </p>
        <p class="text-body text-muted leading-relaxed">
          Estou sempre estudando — o que aprendo na graduação entra direto nos projetos freelance, e o que aprendo com clientes reais volta para a sala de aula.
        </p>
      </div>
    </section>

  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { gsap } from 'gsap'
import { PhCalendar, PhCode, PhFileText, PhUser, PhClock, PhGraduationCap, PhSeal, PhMagnifyingGlass, PhArrowLineDown } from '@phosphor-icons/vue'
import { usePortfolioApi } from '~/composables/usePortfolioApi'
import { useFileUrl } from '~/composables/useFileUrl'
import RadialOrbitalTimeline, { type TimelineItem } from '~/components/ui/RadialOrbitalTimeline.vue'
import { useLanguage } from '~/composables/useLanguage'

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
const extraSectionRef = ref<HTMLElement | null>(null)
const orbitalSectionRef = ref<HTMLElement | null>(null)

useGsap(containerRef, () => {
  if (avatarRef.value) gsap.fromTo(avatarRef.value, { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.6 })
  if (aboutInfoRef.value) gsap.fromTo(aboutInfoRef.value, { opacity: 0, x: 20 }, { opacity: 1, x: 0, duration: 0.6, delay: 0.15 })

  if (orbitalSectionRef.value) {
    gsap.fromTo(orbitalSectionRef.value, { opacity: 0, y: 30 }, {
      opacity: 1, y: 0, duration: 0.7,
      scrollTrigger: { trigger: orbitalSectionRef.value, start: 'top 85%' }
    })
  }

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

  if (extraSectionRef.value) {
    gsap.fromTo(extraSectionRef.value, { opacity: 0, y: 30 }, {
      opacity: 1, y: 0, duration: 0.7,
      scrollTrigger: { trigger: extraSectionRef.value, start: 'top 85%' }
    })
  }
})

onMounted(() => {
  loadData('daniel.pimenta')
})
</script>
