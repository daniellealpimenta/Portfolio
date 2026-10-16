import type { Config } from 'tailwindcss'

// Tokens: veja MASTER.md. As cores são variáveis CSS definidas por paleta em assets/css/main.css.
export default <Partial<Config>>{
  theme: {
    extend: {
      colors: {
        background:      'var(--color-background)',
        surface:         'var(--color-surface)',
        'surface-hover': 'var(--color-surface-hover)',
        border:          'var(--color-border)',
        divider:         'var(--color-divider)',
        muted:           'var(--color-muted)',
        text:            'var(--color-text)',
        primary:         'var(--color-primary)',
        secondary:       'var(--color-secondary)',
        success:         'var(--color-accent-1)',
        danger:          'var(--color-accent-2)',
        warning:         'var(--color-accent-3)',
      },
      fontFamily: {
        display: ['"Plus Jakarta Sans"', '"Segoe UI"', 'system-ui', 'sans-serif'],
        body:    ['"Plus Jakarta Sans"', '"Segoe UI"', 'system-ui', 'sans-serif'],
        mono:    ['"JetBrains Mono"', 'ui-monospace', 'Consolas', 'monospace'],
      },
      fontSize: {
        xxs:  ['0.5rem',   { lineHeight: '1.4' }],   // $fontSizeXS · XXS · 8pt
        xs:   ['0.875rem', { lineHeight: '1.4' }],   // $fontSizeS  · XS  · 14pt
        s:    ['1rem',     { lineHeight: '1.5' }],   // S  · 16pt
        m:    ['1.125rem', { lineHeight: '1.6' }],   // M  · 18pt
        l:    ['1.25rem',  { lineHeight: '1.4' }],   // L  · 20pt
        xl:   ['1.5rem',   { lineHeight: '1.25' }],  // XL  · 24pt
        xxl:  ['2rem',     { lineHeight: '1.15' }],  // XXL · 32pt
        xxxl: ['2.5rem',   { lineHeight: '1.08' }],  // XXXL · 40pt
      },
      maxWidth: {
        page:  '72rem',
        prose: '42rem',
      },
      borderRadius: {
        sm: '8px',
        md: '16px',
      },
      transitionTimingFunction: {
        out: 'cubic-bezier(0.215, 0.61, 0.355, 1)', // GSAP power3.out
      },
      transitionDuration: {
        fast: '180ms',
        base: '320ms',
        slow: '560ms',
      },
    }
  }
}
