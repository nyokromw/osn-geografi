import Image from 'next/image'
import Link from 'next/link'
import type { ReactNode } from 'react'
import { ArrowLeft, LoaderCircle } from 'lucide-react'

export function Brand() {
  return (
    <Link href="/" className="atlas-brand" aria-label="OSNGEO.id, beranda">
      <Image src="/brand/logo-mark.svg" width={36} height={36} alt="" unoptimized />
      <span>OSNGEO<span>.id</span></span>
    </Link>
  )
}

export function AtlasMap({ priority = false }: { priority?: boolean }) {
  return (
    <figure className="atlas-map">
      <Image src="/brand/atlas-indonesia.png" alt="Peta Kepulauan Indonesia dan negara di sekitarnya"
        width={1160} height={690} unoptimized preload={priority}
        sizes="(max-width: 704px) 100vw, 55vw" />
      <figcaption>
        <strong>Kepulauan Indonesia</strong>
        <a href="https://www.naturalearthdata.com/downloads/50m-cultural-vectors/" target="_blank"
          rel="noreferrer" className="atlas-link">Natural Earth</a>
      </figcaption>
    </figure>
  )
}

export function WorkspaceHeader({ title, children }: { title?: string; children?: ReactNode }) {
  return (
    <header className="atlas-topbar">
      <div className="atlas-container atlas-topbar-inner">
        <div className="flex min-w-0 items-center">
          <Brand />
          {title && <span className="atlas-top-title">{title}</span>}
        </div>
        {children && <div className="atlas-top-actions">{children}</div>}
      </div>
    </header>
  )
}

export function AuthShell({ title, description, children }: { title: string; description: string; children: ReactNode }) {
  return (
    <>
      <WorkspaceHeader>
        <Link href="/" className="atlas-link inline-flex items-center gap-1.5 text-sm">
          <ArrowLeft size={15} aria-hidden="true" /> Beranda
        </Link>
      </WorkspaceHeader>
      <main className="atlas-container atlas-auth-grid">
        <AtlasMap />
        <section className="atlas-card atlas-auth-card" aria-labelledby="auth-title">
          <h1 className="atlas-title" id="auth-title">{title}</h1>
          <p className="mt-2 text-sm text-gray-500">{description}</p>
          {children}
        </section>
      </main>
    </>
  )
}

export function Notice({ children, error = false }: { children: ReactNode; error?: boolean }) {
  return <p className="atlas-notice" data-error={error} role={error ? 'alert' : 'status'}>{children}</p>
}

export function PageLoading({ children }: { children: ReactNode }) {
  return (
    <main className="grid min-h-screen place-items-center px-4">
      <div className="flex flex-col items-center gap-5">
        <Brand />
        <p className="flex items-center gap-2 text-sm text-gray-500" role="status">
          <LoaderCircle size={16} className="motion-safe:animate-spin" aria-hidden="true" /> {children}
        </p>
      </div>
    </main>
  )
}
