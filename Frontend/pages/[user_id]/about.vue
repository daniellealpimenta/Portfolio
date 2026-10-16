<template>
  <div ref="pageRef">
    <!-- PERFIL -->
    <section class="pt-12 pb-20 md:pt-20 md:pb-28">
      <div class="container-page grid items-center gap-12 md:grid-cols-[auto_1fr] md:gap-20">
        <div ref="photoRef" class="mx-auto md:mx-0 w-52 h-52 md:w-72 md:h-72 rounded-full p-2 border border-divider">
          <img
            v-if="user?.avatar_url"
            :src="fileUrl(user.avatar_url)"
            :alt="user?.name || ''"
            class="w-full h-full rounded-full object-cover bg-surface"
          />
          <div v-else class="w-full h-full rounded-full bg-surface grid place-items-center text-muted" aria-hidden="true">
            <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="8" r="4" /><path d="M4 20c1-4 4-6 8-6s7 2 8 6" /></svg>
          </div>
        </div>

        <div class="flex flex-col gap-5 max-w-prose">
          <span class="eyebrow" data-hero>{{ t('about.eyebrow') }}</span>
          <h1 class="hero-statement font-semibold small-caps text-text text-balance" data-hero>{{ user?.name || 'Daniel' }}</h1>
          <p class="text-lead whitespace-pre-line" data-hero>{{ user?.description }}</p>
          <div class="flex flex-wrap items-center gap-3 pt-2" data-hero>
            <a v-if="user?.curriculum_url" :href="fileUrl(user.curriculum_url)" target="_blank" rel="noopener" class="btn btn-primary" data-magnetic>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m0 0-4-4m4 4 4-4M4 19h16" /></svg>
              {{ t('about.resumePt') }}
            </a>
            <a v-if="user?.curriculum_en_url" :href="fileUrl(user.curriculum_en_url)" target="_blank" rel="noopener" class="btn btn-secondary">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m0 0-4-4m4 4 4-4M4 19h16" /></svg>
              {{ t('about.resumeEn') }}
            </a>
          </div>
          <SocialLinks class="-ml-2.5" data-hero />
        </div>
      </div>
    </section>

    <!-- EXPERIÊNCIA -->
    <section v-if="experiences.length" class="section border-t border-divider" aria-labelledby="exp-title">
      <div class="container-page grid gap-12 md:grid-cols-[minmax(0,1fr)_minmax(0,2fr)] md:gap-16">
        <div class="md:sticky md:top-28 self-start">
          <SectionHeading id="exp-title" :eyebrow="t('journey.eyebrow')" :title="t('about.experience')" />
        </div>
        <ExperienceTimeline :experiences="experiences" />
      </div>
    </section>

    <!-- CERTIFICADOS (só aparece quando há algum cadastrado) -->
    <section v-if="certificates.length" class="section border-t border-divider" aria-labelledby="cert-title">
      <div class="container-page">
        <SectionHeading id="cert-title" :title="t('about.certificates')" />
        <CertificateList :certificates="certificates" />
      </div>
    </section>

    <!-- VALORES E HOBBIES -->
    <section class="section border-t border-divider" aria-labelledby="values-title">
      <div class="container-page">
        <SectionHeading id="values-title" :title="t('about.values')" />
        <div data-reveal>
          <RadialOrbitalTimeline :timeline-data="orbitalData" />
        </div>
      </div>
    </section>

    <!-- POR QUE ME CONTRATAR -->
    <section class="section border-t border-divider" aria-labelledby="why-title">
      <div class="container-page grid items-start gap-10 md:grid-cols-[minmax(0,1fr)_minmax(0,2fr)] md:gap-16">
        <SectionHeading id="why-title" :title="t('about.whyMe')" />
        <div class="flex flex-col gap-5 text-lg leading-relaxed text-text max-w-prose" data-reveal>
          <p>{{ t('about.whyMe1') }}</p>
          <p class="text-muted">{{ t('about.whyMe2') }}</p>
          <div class="pt-3">
            <NuxtLink :to="{ path: `/${route.params.user_id}`, hash: '#contato' }" class="btn btn-primary" data-magnetic>
              {{ t('contact.title') }}
            </NuxtLink>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { gsap } from 'gsap'
import { useRoute } from 'vue-router'
import { PhCalendar, PhCode, PhFileText, PhUser, PhClock } from '@phosphor-icons/vue'
import { usePortfolioApi } from '~/composables/usePortfolioApi'
import { useFileUrl } from '~/composables/useFileUrl'
import { useI18n } from '~/composables/useI18n'
import { useReveal } from '~/composables/useReveal'
import RadialOrbitalTimeline, { type TimelineItem } from '~/components/ui/RadialOrbitalTimeline.vue'
import SectionHeading from '~/components/ui/SectionHeading.vue'
import ExperienceTimeline from '~/components/ExperienceTimeline.vue'
import CertificateList from '~/components/CertificateList.vue'
import SocialLinks from '~/components/SocialLinks.vue'

const route = useRoute()
const { user, experiences, certificates, loadData } = usePortfolioApi()
const { t, lang } = useI18n()
const fileUrl = useFileUrl()

const orbitalData = computed<TimelineItem[]>(() => {
  const en = lang.value === 'en'
  return [
    {
      id: 1,
      title: en ? 'Planning & Thesis' : 'Planejamento & TCC',
      date: '2026',
      content: en
        ? 'Building AgroBot, the final project of my Software Engineering degree, in Swift.'
        : 'Desenvolvimento do AgroBot, projeto final do curso de Engenharia de Software em Swift.',
      category: en ? 'Engineering' : 'Engenharia',
      icon: PhCalendar,
      relatedIds: [2, 3],
      status: 'in-progress',
      energy: 100,
    },
    {
      id: 2,
      title: en ? 'Swift Mobile Dev' : 'Dev. Mobile Swift',
      date: '2025-2026',
      content: en
        ? 'Native iOS apps with Swift, SwiftUI and SwiftData at the Apple Developer Academy.'
        : 'Construção de aplicativos iOS nativos com Swift, SwiftUI e SwiftData na Apple Developer Academy.',
      category: 'Mobile',
      icon: PhCode,
      relatedIds: [1, 4],
      status: 'completed',
      energy: 95,
    },
    {
      id: 3,
      title: en ? 'Web Systems & APIs' : 'Sistemas Web & APIs',
      date: '2024-2025',
      content: en
        ? 'Rebuilding systems in Angular, FastAPI/Node.js APIs and process automation.'
        : 'Reconstrução de sistemas em Angular, APIs FastAPI/Node.js e automação de processos.',
      category: 'Backend',
      icon: PhFileText,
      relatedIds: [1, 5],
      status: 'completed',
      energy: 90,
    },
    {
      id: 4,
      title: en ? 'UI/UX & Prototypes' : 'UI/UX & Protótipos',
      date: '2024',
      content: en
        ? 'Interface design in Figma with a focus on user experience and usability.'
        : 'Design de interfaces no Figma com foco em experiência do usuário e usabilidade.',
      category: 'Design',
      icon: PhUser,
      relatedIds: [2],
      status: 'completed',
      energy: 85,
    },
    {
      id: 5,
      title: en ? 'Software Eng. Degree' : 'Graduação Eng. Software',
      date: en ? '2023-Present' : '2023-Presente',
      content: en
        ? 'An education that brings together systems engineering, databases and IT governance.'
        : 'Formação acadêmica unindo engenharia de sistemas, bancos de dados e governança de TI.',
      category: en ? 'Academic' : 'Acadêmico',
      icon: PhClock,
      relatedIds: [3],
      status: 'completed',
      energy: 80,
    },
  ]
})

const pageRef = ref<HTMLElement | null>(null)
const photoRef = ref<HTMLElement | null>(null)

useGsap(pageRef, () => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const lines = pageRef.value?.querySelectorAll('[data-hero]') || []
  if (reduce) {
    gsap.fromTo([photoRef.value, ...lines], { opacity: 0 }, { opacity: 1, duration: 0.2 })
    return
  }
  gsap.timeline({ defaults: { ease: 'power3.out' } })
    .fromTo(photoRef.value, { opacity: 0, scale: 0.94 }, { opacity: 1, scale: 1, duration: 0.56 })
    .fromTo(lines, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.56, stagger: 0.06, clearProps: 'transform' }, '-=0.36')
})

useReveal(pageRef, () => [experiences.value.length, certificates.value.length])

onMounted(() => {
  loadData(route.params.user_id as string)
})
</script>
