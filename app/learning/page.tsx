'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import { ArrowRight, BookOpen, Crown, Loader2 } from 'lucide-react'
import { AuthUser, Enrollment, coursehubApi } from '@/lib/coursehub-api'

export default function LearningPage() {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [items, setItems] = useState<Enrollment[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([coursehubApi.me(), coursehubApi.myLearning()])
      .then(([profile, learning]) => { setUser(profile); setItems(learning) })
      .catch((reason) => setError(reason instanceof Error ? reason.message : 'Please sign in to view your learning.'))
      .finally(() => setLoading(false))
  }, [])

  return <main className="min-h-screen bg-background text-foreground">
    <header className="border-b border-border"><div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6 lg:px-10"><Link href="/" className="flex items-center gap-3"><span className="brand-mark"><Crown size={17} /></span><span className="font-serif text-xl font-semibold text-primary">CourseHub</span></Link><Link href="/" className="text-sm font-semibold text-primary">Explore courses</Link></div></header>
    <section className="mx-auto max-w-7xl px-6 py-16 lg:px-10"><p className="eyebrow">Private library</p><h1 className="mt-5 max-w-2xl font-serif text-5xl tracking-tight text-primary">{user ? `Welcome back, ${user.first_name || user.email.split('@')[0]}.` : 'Your learning, collected.'}</h1><p className="mt-5 max-w-xl text-lg leading-8 text-muted-foreground">Return to the ideas you chose and keep building a more considered practice.</p>{loading && <div className="mt-14 flex items-center gap-3 text-muted-foreground"><Loader2 className="animate-spin" size={18} /> Loading your library</div>}{error && <div className="mt-12 border border-border p-6"><p className="font-semibold text-primary">Sign in required</p><p className="mt-2 text-sm text-muted-foreground">{error}</p><Link href="/" className="button-primary mt-5 inline-flex px-5 py-3">Return to sign in <ArrowRight size={15} /></Link></div>}{!loading && !error && <div className="mt-14 grid gap-5 md:grid-cols-2 lg:grid-cols-3">{items.length ? items.map((item) => <article key={item.id} className="course-card p-7"><span className="text-xs font-semibold tracking-[0.18em] text-accent">ENROLLED</span><BookOpen className="mt-8 text-accent" size={25} /><h2 className="mt-5 font-serif text-3xl text-primary">{item.course_title}</h2><p className="mt-3 text-sm text-muted-foreground">Enrolled {new Date(item.enrolled_at).toLocaleDateString()}</p><Link href={`/courses/${item.course_id}`} className="mt-8 inline-flex items-center gap-2 text-sm font-semibold text-primary">Continue learning <ArrowRight size={15} /></Link></article>) : <div className="border border-border p-8 md:col-span-2 lg:col-span-3"><h2 className="font-serif text-3xl text-primary">Your first chapter is waiting.</h2><p className="mt-3 text-muted-foreground">Explore the collection and enroll in a course to begin.</p><Link href="/#courses" className="button-primary mt-6 inline-flex px-5 py-3">Browse courses <ArrowRight size={15} /></Link></div>}</div>}</section>
  </main>
}
