<template>
  <div class="grid gap-6 md:grid-cols-2">
    <figure
      v-for="item in recommendations"
      :key="item.id"
      class="card p-7 md:p-8 flex flex-col gap-6"
      data-reveal
    >
      <svg width="32" height="24" viewBox="0 0 34 24" class="text-primary shrink-0" aria-hidden="true">
        <path fill="currentColor" d="M0 24V14.4C0 6.6 4.2 1.8 12.6 0l1.5 3C9.9 4.4 7.6 7 7.2 10.8H13V24H0Zm18.9 0V14.4C18.9 6.6 23.1 1.8 31.5 0L33 3c-4.2 1.4-6.5 4-6.9 7.8h5.8V24H18.9Z" />
      </svg>

      <blockquote class="text-base md:text-[1.0625rem] leading-relaxed text-text flex-1">
        <p>{{ item.quote }}</p>
      </blockquote>

      <figcaption class="flex items-center gap-3 pt-5 border-t border-divider">
        <img
          v-if="item.recommender_avatar_url && !broken[item.id]"
          :src="item.recommender_avatar_url"
          alt=""
          loading="lazy"
          class="w-11 h-11 rounded-full object-cover border border-divider shrink-0"
          @error="broken[item.id] = true"
        />
        <span
          v-else
          class="w-11 h-11 rounded-full bg-surface-hover text-primary border border-divider grid place-items-center font-semibold text-sm shrink-0"
          aria-hidden="true"
        >{{ getInitials(item.name) }}</span>

        <div class="flex flex-col min-w-0">
          <a
            v-if="item.linkedin_recommender_url"
            :href="item.linkedin_recommender_url"
            target="_blank"
            rel="noopener noreferrer"
            class="title-item link-underline self-start"
          >{{ item.name }}</a>
          <span v-else class="title-item">{{ item.name }}</span>
          <span v-if="item.date" class="text-sm text-muted tabular-nums">{{ formatDate(item.date) }}</span>
        </div>
      </figcaption>
    </figure>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import type { Testimonial } from '~/composables/usePortfolioApi'
import { useI18n } from '~/composables/useI18n'

defineProps<{
  recommendations: Testimonial[]
}>()

const { locale } = useI18n()
// Fotos de perfil do LinkedIn expiram ou são bloqueadas fora do LinkedIn: cai pras iniciais.
const broken = reactive<Record<string | number, boolean>>({})

function getInitials(name: string): string {
  const parts = name.trim().split(/\s+/).filter(Boolean)
  if (parts.length === 0) return '?'
  if (parts.length === 1) return parts[0][0].toUpperCase()
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
}

function formatDate(iso: string) {
  const d = new Date(`${iso.substring(0, 10)}T12:00:00`)
  return isNaN(d.getTime()) ? iso : d.toLocaleDateString(locale.value, { month: 'long', year: 'numeric' })
}
</script>
