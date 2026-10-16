<template>
  <div ref="pageRef">
    <!-- HERO -->
    <section id="inicio" class="relative overflow-hidden pt-12 pb-20 md:pt-20 md:pb-28">
      <div class="absolute inset-x-0 top-0 z-0 opacity-20 text-primary pointer-events-none flex justify-center" aria-hidden="true">
        <HeroBackground class="w-[150vw] md:w-[120vw] h-[250px] md:h-[300px]" />
      </div>

      <div class="container-page relative z-10 grid items-center gap-12 md:grid-cols-[auto_1fr] md:gap-20">
        <div ref="avatarRef" class="mx-auto md:mx-0 mb-6 md:mb-0 w-[180px] md:w-[250px] aspect-square grid place-items-center">
          <InteractiveAvatar class="scale-[1.35]" />
        </div>

        <div class="flex flex-col gap-5 max-w-prose">
          <span class="eyebrow" data-hero>{{ t('hero.role') }}</span>
          <h1 class="hero-statement font-semibold text-text text-balance" data-hero>
            <TypedText :text="user?.main_phrase || t('hero.fallbackPhrase')" />
          </h1>
          <p class="text-lead whitespace-pre-line" data-hero>{{ user?.description }}</p>

          <div class="flex flex-wrap items-center gap-3 pt-2" data-hero>
            <a href="#projetos" class="btn btn-primary" data-magnetic @click.prevent="scrollTo('projetos')">
              {{ t('hero.ctaWork') }}
            </a>
            <a v-if="resumeUrl" :href="resumeUrl" target="_blank" rel="noopener" class="btn btn-secondary">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m0 0-4-4m4 4 4-4M4 19h16" /></svg>
              {{ t('hero.ctaResume') }}
            </a>
          </div>
          <SocialLinks class="-ml-2.5" data-hero />
        </div>
      </div>
    </section>

    <!-- PROJETOS -->
    <section id="projetos" class="section pt-8 md:pt-12" aria-labelledby="projetos-title">
      <div class="container-page">
        <SectionHeading id="projetos-title" :eyebrow="t('work.eyebrow')" :title="t('work.homeTitle')">
          <template #action>
            <NuxtLink :to="`${base}/work`" class="btn btn-ghost">{{ t('work.seeAll') }} →</NuxtLink>
          </template>
        </SectionHeading>

        <!-- O mais recente em destaque; os dois seguintes ao lado -->
        <div class="grid gap-6 md:grid-cols-3 md:grid-rows-2">
          <div
            v-for="(project, i) in recentProjects"
            :key="project.id"
            data-reveal
            :class="i === 0 ? 'md:col-span-2 md:row-span-2' : ''"
          >
            <ProjectCard :project="project" :to="`${base}/projects/${project.id}`" :large="i === 0" />
          </div>
        </div>
      </div>
    </section>

    <!-- O QUE EU FAÇO -->
    <section v-if="skills.length" id="atuacao" class="section border-t border-divider" aria-labelledby="atuacao-title">
      <div class="container-page grid gap-12 md:grid-cols-[minmax(0,1fr)_minmax(0,2fr)] md:gap-16">
        <div class="md:sticky md:top-28 self-start">
          <SectionHeading id="atuacao-title" :eyebrow="t('skills.eyebrow')" :title="t('skills.title')" />
        </div>

        <div class="flex flex-col gap-14">
          <dl class="grid gap-x-10 gap-y-10 sm:grid-cols-2">
            <div v-for="skill in skills" :key="skill.id" class="flex flex-col gap-2" data-reveal>
              <dt class="title-item flex items-start gap-3">
                <span class="mt-[0.55rem] h-px w-5 shrink-0 bg-primary" aria-hidden="true"></span>
                {{ skill.name }}
              </dt>
              <dd v-if="skill.desc" class="pl-8 text-muted leading-relaxed">{{ skill.desc }}</dd>
            </div>
          </dl>

          <div v-if="tools.length" class="flex flex-col gap-4" data-reveal>
            <h3 class="eyebrow">{{ t('skills.tools') }}</h3>
            <ul class="flex flex-wrap gap-2">
              <li v-for="tool in tools" :key="tool.id" class="chip text-sm text-text">{{ tool.name }}</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- TRAJETÓRIA -->
    <section v-if="experiences.length" id="trajetoria" class="section border-t border-divider" aria-labelledby="trajetoria-title">
      <div class="container-page">
        <SectionHeading id="trajetoria-title" :eyebrow="t('journey.eyebrow')" :title="t('journey.title')">
          <template #action>
            <NuxtLink :to="`${base}/about`" class="btn btn-ghost">{{ t('journey.seeAll') }} →</NuxtLink>
          </template>
        </SectionHeading>
        <ExperienceTimeline :experiences="experiences" compact />
      </div>
    </section>

    <!-- RECOMENDAÇÕES -->
    <section v-if="testimonials.length" id="recomendacoes" class="section border-t border-divider" aria-labelledby="reco-title">
      <div class="container-page">
        <SectionHeading id="reco-title" :eyebrow="t('reco.eyebrow')" :title="t('reco.title')" />
        <RecommendationList :recommendations="testimonials" />
      </div>
    </section>

    <!-- CONTATO -->
    <section id="contato" class="section border-t border-divider" aria-labelledby="contato-title">
      <div class="container-page grid gap-12 md:grid-cols-2 md:gap-16 items-start">
        <div class="flex flex-col gap-6 md:sticky md:top-28" data-reveal>
          <span class="eyebrow">{{ t('contact.eyebrow') }}</span>
          <h2 id="contato-title" class="hero-statement font-semibold text-text text-balance small-caps">{{ t('contact.title') }}</h2>
          <p class="text-lead">{{ t('contact.lead') }}</p>
          <div class="flex flex-wrap items-center gap-4 pt-2">
            <a
              v-if="whatsappLink"
              :href="whatsappLink"
              target="_blank"
              rel="noopener noreferrer"
              class="btn btn-primary btn-lg"
              data-magnetic
            >
              <span class="icon-whatsapp" aria-hidden="true"></span>
              {{ t('contact.whatsapp') }}
            </a>
            <span class="text-sm text-muted small-caps tracking-wide">{{ t('contact.orForm') }}</span>
          </div>
        </div>
        <div data-reveal>
          <ContactForm />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { gsap } from 'gsap'
import { usePortfolioApi } from '~/composables/usePortfolioApi'
import { useI18n } from '~/composables/useI18n'
import { useFileUrl } from '~/composables/useFileUrl'
import { useReveal } from '~/composables/useReveal'
import InteractiveAvatar from '~/components/ui/InteractiveAvatar.vue'
import HeroBackground from '~/components/ui/HeroBackground.vue'
import TypedText from '~/components/ui/TypedText.vue'
import SectionHeading from '~/components/ui/SectionHeading.vue'
import ProjectCard from '~/components/ProjectCard.vue'
import ExperienceTimeline from '~/components/ExperienceTimeline.vue'
import RecommendationList from '~/components/RecommendationList.vue'
import ContactForm from '~/components/ContactForm.vue'
import SocialLinks from '~/components/SocialLinks.vue'

const route = useRoute()
const { user, projects, tools, skills, experiences, testimonials, loadData } = usePortfolioApi()
const { t, lang } = useI18n()
const fileUrl = useFileUrl()

const base = computed(() => `/${route.params.user_id}`)
const recentProjects = computed(() => projects.value.slice(0, 3))

const resumeUrl = computed(() =>
  fileUrl(lang.value === 'en' ? (user.value?.curriculum_en_url || user.value?.curriculum_url) : user.value?.curriculum_url),
)

const whatsappLink = computed(() => {
  const phone = user.value?.cellphone_number?.replace(/\D/g, '')
  if (!phone) return ''
  const firstName = user.value?.name?.split(' ')[0] || 'Daniel'
  const text = lang.value === 'en'
    ? `Hi ${firstName}, I saw your portfolio and would like to talk about a project or opportunity!`
    : `Olá ${firstName}, vi o seu portfólio e gostaria de conversar sobre um projeto ou oportunidade!`
  return `https://wa.me/${phone}?text=${encodeURIComponent(text)}`
})

function scrollTo(id: string) {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  document.getElementById(id)?.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' })
}

const pageRef = ref<HTMLElement | null>(null)
const avatarRef = ref<HTMLElement | null>(null)

// Entrada do hero: avatar, depois cada linha sobe 24px (MASTER.md: 560ms, stagger 60ms)
useGsap(pageRef, () => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const lines = pageRef.value?.querySelectorAll('[data-hero]') || []
  if (reduce) {
    gsap.fromTo([avatarRef.value, ...lines], { opacity: 0 }, { opacity: 1, duration: 0.2 })
    return
  }
  gsap.timeline({ defaults: { ease: 'power3.out' } })
    .fromTo(avatarRef.value, { opacity: 0, scale: 0.94 }, { opacity: 1, scale: 1, duration: 0.56 })
    .fromTo(lines, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.56, stagger: 0.06, clearProps: 'transform' }, '-=0.36')
})

useReveal(pageRef, () => [projects.value.length, skills.value.length, experiences.value.length, testimonials.value.length])

onMounted(() => {
  loadData(route.params.user_id as string)
})
</script>

<style scoped>
.icon-whatsapp {
  display: inline-block;
  width: 1.25rem;
  height: 1.25rem;
  background-color: currentColor;
  -webkit-mask: url('~/assets/icons/whatsapp-logo.svg') center / contain no-repeat;
  mask: url('~/assets/icons/whatsapp-logo.svg') center / contain no-repeat;
}
</style>
