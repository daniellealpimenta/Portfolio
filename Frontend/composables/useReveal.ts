import { nextTick, onMounted, onUnmounted, watch, type Ref, type WatchSource } from 'vue'
import { gsap } from 'gsap'

/**
 * Revela uma vez, no scroll, todo elemento com `data-reveal` dentro de `root`
 * (MASTER.md: 560ms, sobe 24px, stagger 60ms, power3.out). Com "reduzir
 * movimento", vira só um fade de 200ms.
 *
 * Os dados das páginas chegam da API depois do mount, então passe em `source`
 * o que faz novos elementos aparecerem (ex: () => projects.value.length):
 * a cada mudança, os elementos novos entram na fila.
 */
export function useReveal(root: Ref<HTMLElement | null>, source?: WatchSource) {
  let ctx: gsap.Context | null = null
  const seen = new WeakSet<Element>()

  async function scan() {
    if (!import.meta.client || !root.value) return
    await nextTick()
    const { ScrollTrigger } = await import('gsap/ScrollTrigger')
    gsap.registerPlugin(ScrollTrigger)
    if (!root.value) return

    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    document.documentElement.classList.add('reveal-ready')

    const fresh = Array.from(root.value.querySelectorAll('[data-reveal]')).filter(el => !seen.has(el))
    if (!fresh.length) return
    fresh.forEach(el => seen.add(el))

    if (!ctx) ctx = gsap.context(() => {}, root.value)
    ctx.add(() => {
      ScrollTrigger.batch(fresh, {
        start: 'top 88%',
        once: true,
        onEnter: batch => {
          gsap.fromTo(
            batch,
            reduce ? { opacity: 0 } : { opacity: 0, y: 24 },
            {
              opacity: 1,
              y: 0,
              duration: reduce ? 0.2 : 0.56,
              ease: 'power3.out',
              stagger: 0.06,
              onComplete() {
                // Libera o elemento pro CSS (hover dos cards usa transform)
                batch.forEach(el => el.setAttribute('data-revealed', ''))
                gsap.set(batch, { clearProps: 'opacity,transform' })
              },
            },
          )
        },
      })
    })
    ScrollTrigger.refresh()
  }

  onMounted(scan)
  if (source) watch(source, scan, { flush: 'post' })
  onUnmounted(() => ctx?.revert())

  return { refresh: scan }
}
