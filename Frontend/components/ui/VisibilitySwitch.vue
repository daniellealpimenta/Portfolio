<template>
  <!-- Liga/desliga se um campo do perfil aparece no site público -->
  <button
    type="button"
    role="switch"
    :aria-checked="modelValue"
    :aria-label="`${label}: ${modelValue ? 'visível no site' : 'escondido do site'}`"
    :title="modelValue ? 'Visível no site. Clique para esconder.' : 'Escondido do site. Clique para mostrar.'"
    class="group inline-flex items-center gap-2 text-xs select-none"
    @click="$emit('update:modelValue', !modelValue)"
  >
    <span
      class="relative inline-flex h-5 w-9 shrink-0 items-center rounded-full border transition-colors duration-fast ease-out"
      :class="modelValue ? 'bg-primary border-primary' : 'bg-background border-border'"
    >
      <span
        class="absolute left-0.5 h-3.5 w-3.5 rounded-full transition-transform duration-fast ease-out"
        :class="modelValue ? 'translate-x-4 bg-background' : 'translate-x-0 bg-muted'"
      ></span>
    </span>
    <span :class="modelValue ? 'text-text' : 'text-muted'">{{ modelValue ? 'Visível' : 'Escondido' }}</span>
  </button>
</template>

<script setup lang="ts">
defineProps<{ modelValue: boolean; label: string }>()
defineEmits<{ 'update:modelValue': [value: boolean] }>()
</script>
