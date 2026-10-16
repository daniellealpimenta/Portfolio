<template>
  <article class="group card card-interactive relative flex flex-col overflow-hidden h-full focus-within:border-primary">
    <ProjectCover
      :title="project.title"
      :categories="project.categories"
      :large="large"
      class="border-b border-divider"
      :class="large ? 'aspect-[16/9] md:aspect-auto md:flex-1 md:min-h-[18rem]' : 'aspect-[16/10]'"
    />

    <!-- No card grande a capa cresce e ocupa a altura; no pequeno, o texto ocupa -->
    <div class="flex flex-col gap-3 p-5" :class="large ? 'md:p-7' : 'flex-1'">
      <div class="flex items-center justify-between text-sm text-muted tabular-nums">
        <span>{{ project.year }}</span>
        <!-- Botão fica acima do link que cobre o card (z-10), pra curtir sem abrir o projeto -->
        <button
          type="button"
          class="relative z-10 -m-2 p-2 flex items-center gap-1.5 rounded-full transition-colors duration-fast ease-out hover:text-primary"
          :class="project.liked ? 'text-primary' : ''"
          :aria-pressed="!!project.liked"
          :aria-label="project.liked ? t('work.unlike') : t('work.like')"
          @click="toggleLike"
        >
          <svg width="15" height="15" viewBox="0 0 24 24" :fill="project.liked ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
          </svg>
          {{ project.likes }}
        </button>
      </div>

      <h3 :class="large ? 'title-section' : 'title-item'">
        <NuxtLink :to="to" class="after:absolute after:inset-0 after:content-[''] focus:outline-none">
          {{ project.title }}
        </NuxtLink>
      </h3>

      <p v-if="project.desc" class="text-sm text-muted leading-relaxed" :class="large ? 'line-clamp-4' : 'line-clamp-3'">
        {{ plainDesc }}
      </p>

      <div v-if="project.categories.length" class="mt-auto pt-1 flex flex-wrap gap-1.5">
        <span v-for="cat in project.categories" :key="cat" class="chip">{{ cat }}</span>
      </div>
    </div>
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { usePortfolioApi, type Project } from '~/composables/usePortfolioApi'
import { useI18n } from '~/composables/useI18n'
import ProjectCover from '~/components/ui/ProjectCover.vue'

const props = defineProps<{
  project: Project
  to: string
  large?: boolean
}>()

const { likeProject } = usePortfolioApi()
const { t } = useI18n()

// A descrição é Markdown (renderizada na página do projeto); no card, só o texto.
const plainDesc = computed(() =>
  props.project.desc
    .replace(/!\[[^\]]*\]\([^)]*\)/g, '')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/[#>*_`~-]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim(),
)

async function toggleLike() {
  const p = props.project as any
  const wasLiked = !!p.liked
  p.liked = !wasLiked
  p.likes += wasLiked ? -1 : 1

  try {
    const res: any = await likeProject(p.id, p.liked)
    if (res && typeof res.likes === 'number') p.likes = res.likes
  } catch (e) {
    console.error('Failed to update likes', e)
    p.liked = wasLiked
    p.likes += wasLiked ? 1 : -1
  }
}
</script>
