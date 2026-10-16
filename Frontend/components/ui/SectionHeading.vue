<template>
  <header class="flex flex-wrap items-end justify-between gap-x-8 gap-y-4 mb-10 md:mb-12" data-reveal>
    <div class="flex flex-col gap-2 min-w-0">
      <span v-if="eyebrow" class="eyebrow">{{ eyebrow }}</span>
      <component :is="as" :id="id" :class="as === 'h1' ? 'title-page' : 'title-section'">
        <slot name="title">{{ title }}</slot>
      </component>
      <p v-if="lead" class="text-lead mt-1">{{ lead }}</p>
    </div>
    <div v-if="$slots.action" class="shrink-0">
      <slot name="action" />
    </div>
  </header>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  eyebrow?: string
  title?: string
  lead?: string
  as?: 'h1' | 'h2'
  id?: string
}>(), { as: 'h2' })
</script>
