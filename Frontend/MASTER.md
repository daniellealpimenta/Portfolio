# Design system: Hire Me portfolio

Single source of truth for the public site's look and motion. Every colour, size and duration in
components comes from the tokens below (CSS variables in `assets/css/main.css`, mapped into
Tailwind in `tailwind.config.ts`). Visual preview: https://claude.ai/artifact/FbqCvcvyNv6TXBWGw3N6BD

## Theses (validated 2026-10-15)

**Visual.** Preserving the existing palettes, theme switcher and logo: a navy night (with the
starfield) and a cream day, Plus Jakarta Sans as the only face with small caps as the voice of every
heading and label, an airy 8px rhythm in a single 72rem column, and flat components with a 1px
border and 16px radius. The avatar's diagonal hatching becomes the one ornament, drawn as each
project's cover when there is no screenshot.

**Interaction.** Medium timing on power3.out (180ms hovers, 320ms UI, 560ms reveals): the headline
types itself once and the underscore keeps blinking, sections rise 24px once on scroll with a 60ms
stagger, and cards lift 4px with the border turning primary while their hatching slides. No bounce,
no parallax, no pulsing or pinging rings, no scroll-jacking. Reduced motion keeps opacity only.

**Allowed patterns:** small-caps headings, blinking underscore cursor, terminal intro screen,
starfield on dark, grain overlay, hatched line-art covers, magnetic buttons. (The header blur listed
in the approved thesis was dropped during the build: the always-dark header turned grey over the
cream day mode, so it stays solid.)

## Colour

Six palettes (`data-theme` on `<body>`: refined, forest, burgundy, amber, ocean, slate), each with a
dark mode (default) and a light mode (`body.light`). Token names are public and unchanged:

| Token | Tailwind | Role |
|---|---|---|
| `--color-background` | `bg-background` | page ground |
| `--color-surface` | `bg-surface` | cards, inputs, panels |
| `--color-surface-hover` | `bg-surface-hover` | hovered surface (derived per palette) |
| `--color-border` | `border-border` | interactive outlines (buttons, inputs) |
| `--color-divider` | `border-divider` | quiet structure (card edges, rules) (derived per palette) |
| `--color-text` | `text-text` | body and headings |
| `--color-muted` | `text-muted` | secondary text |
| `--color-primary` | `primary` | actions, links, focus ring, accents |
| `--color-secondary` | `secondary` | second accent; light values added in this redesign |
| `--color-accent-1/2/3` | `success` / `danger` / `warning` | categories and status |

Text on a primary fill uses `text-background` (dark ink on the light night-primary, cream on the
dark day-primary). Measured on Refined against the background: text 17.8:1 (night) and 14.1:1
(day), muted 10.6:1 and 6.7:1, primary 9.6:1 and 6.1:1, the new day secondary #6A4BB8 5.8:1. New day
secondaries on the other palettes: forest #2F6E63 5.5:1, burgundy #8A3F66 6.4:1, amber #7A5A12
5.8:1, ocean #2A5BA8 6.2:1, slate #45556F 7.0:1.

## Type

One family: Plus Jakarta Sans (Google Fonts, `display=swap`, fallback `"Segoe UI", system-ui,
sans-serif`). JetBrains Mono only for code and the terminal intro.

| Role | Class | Size / weight |
|---|---|---|
| Hero statement | `.hero-statement` | clamp(2.5rem → 4rem) / 600, line-height 1.05 |
| Page title (h1) | `.title-page` | clamp(2rem → 2.75rem) / 600, small caps |
| Section title (h2) | `.title-section` | clamp(1.5rem → 2rem) / 600, small caps |
| Item title (h3) | `.title-item` | 1.125rem / 600, small caps |
| Eyebrow / label | `.eyebrow` | 0.8125rem / 600, small caps, tracking .08em, primary |
| Lead | `.text-lead` | 1.125rem / 400, muted |
| Body | `text-base` | 1rem / 400, line-height 1.6, max 65ch |
| Caption | `text-sm` | 0.875rem, muted |

Every heading and label is small caps. No uppercase, no icon-in-heading.

## Space and layout

- Base unit 8px (Tailwind spacing scale).
- Page column: `.container-page` = max-width 72rem (`max-w-page`), side padding 24px.
- Reading column: `max-w-prose` (42rem).
- Section rhythm: `.section` = padding-block 96px mobile, 128px from `md`.
- Section head: eyebrow, title, optional lead, optional action on the right; 40px below it.

## Shape

- Radius: `rounded-sm` 8px (chips, inputs, small tiles), `rounded-md` 16px (cards, panels),
  `rounded-full` (buttons, pills).
- Borders: 1px. Cards use `divider`; controls use `border`.
- No shadows on content, no glass on content. Elevation is shown by the border turning primary.

## Components

| Class / component | Notes |
|---|---|
| `.btn` + `.btn-primary` / `.btn-secondary` / `.btn-ghost` | 5 states: hover lifts 2px, focus ring 2px primary offset 3px, active scale .97, disabled .45 opacity |
| `.card` (+ `.card-interactive`) | surface, 1px divider, 16px radius; interactive: lift 4px, border primary |
| `.chip` | small caps, pill, divider border, muted |
| `<SectionHeading>` | eyebrow + title + lead + action slot |
| `<ProjectCover>` | screenshot when present, otherwise hatched line art in the category tone with the project's initials |
| `<TypedText>` | types a phrase once, then the blinking underscore |

## Motion

| Token | Value | Use |
|---|---|---|
| `--ease-out` / `ease-out` | cubic-bezier(0.215, 0.61, 0.355, 1) = GSAP `power3.out` | every enter and hover |
| `--dur-fast` | 180ms | hover, focus, press |
| `--dur-base` | 320ms | UI changes, page transition, card lift |
| `--dur-slow` | 560ms | scroll reveals |
| `--stagger` | 60ms | between revealed siblings |
| `--rise` | 24px | reveal travel |

- Reveals: add `data-reveal` to an element (or `data-reveal-stagger` to a parent) inside a page that
  calls `useReveal(rootRef)`. Plays once at `top 88%`.
- Headline: typed at 45ms per letter, once per visit.
- Page transition: 320ms fade + 12px rise in, 180ms fade out.
- Forbidden: bounce/elastic/back easing, parallax, scroll-jacking, `animate-pulse` / `animate-ping`
  except on real loading states, animating width/height/top/left.
- Reduced motion: reveals become a 200ms fade, typing shows the full phrase, page transition fades
  only, magnetic buttons and cursor glow are off.
