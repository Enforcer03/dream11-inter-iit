// app/fonts.ts
import { Quantico } from 'next/font/google'

export const quantico = Quantico({
  subsets: ['latin'],
  weight: ['400', '700'], // available weights: 400 (regular) and 700 (bold)
  display: 'swap',
})