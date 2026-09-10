import React from 'react'

export default function Card({ children, className = '' }) {
  return (
    <div className={`bg-white rounded-[var(--radius)] shadow-sm p-6 md:p-8 ${className}`}>
      {children}
    </div>
  )
}
