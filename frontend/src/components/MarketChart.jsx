import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

export default function MarketChart({ data }) {
  return (
    <div className="bg-white p-6 rounded-[var(--radius)] shadow-sm w-full flex flex-col justify-between">
      <h3 className="text-xl font-serif text-charcoal mb-3">Market Size Estimation</h3>
      
      <div className="h-[140px] w-full mb-4">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            layout="vertical"
            margin={{ top: 0, right: 20, left: 10, bottom: 0 }}
          >
            <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#E5E7EB" />
            <XAxis type="number" hide />
            <YAxis 
              dataKey="name" 
              type="category" 
              axisLine={false} 
              tickLine={false}
              tick={{ fill: 'var(--color-text)', fontFamily: 'Inter, sans-serif', fontWeight: 600 }}
              width={45}
            />
            <Tooltip 
              cursor={{ fill: 'rgba(63, 107, 79, 0.05)' }}
              contentStyle={{ 
                backgroundColor: 'var(--color-bg-card)', 
                border: 'none', 
                borderRadius: '8px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
              }}
              itemStyle={{ color: 'var(--color-primary)' }}
            />
            <Bar 
              dataKey="value" 
              fill="var(--color-primary)" 
              radius={[0, 4, 4, 0]}
              barSize={20}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="space-y-2 pt-2 border-t border-gray-100 text-xs">
        {data.map((item) => (
          <div key={item.name} className="flex flex-col gap-0.5">
            <span className="font-semibold text-charcoal tracking-wide">{item.name}:</span>
            <span className="text-charcoal-muted leading-relaxed font-sans line-clamp-2">
              {item.text || 'Quantitative estimate derived from retrieved cases.'}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
