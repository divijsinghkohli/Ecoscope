'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { Company } from '../services/api'

interface RiskChartProps {
  companies: Company[]
}

export default function RiskChart({ companies }: RiskChartProps) {
  // Prepare data for bar chart
  const barData = companies.map(company => ({
    name: company.name,
    overall: company.overall_score * 100,
    environmental: company.environmental_score * 100,
    social: company.social_score * 100,
    governance: company.governance_score * 100,
  }))

  // Prepare data for pie chart (risk distribution)
  const riskDistribution = [
    {
      name: 'Low Risk',
      value: companies.filter(c => c.overall_score < 0.3).length,
      color: '#10b981'
    },
    {
      name: 'Medium Risk',
      value: companies.filter(c => c.overall_score >= 0.3 && c.overall_score < 0.7).length,
      color: '#f59e0b'
    },
    {
      name: 'High Risk',
      value: companies.filter(c => c.overall_score >= 0.7).length,
      color: '#ef4444'
    }
  ]

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-semibold text-gray-900">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.dataKey}: {entry.value.toFixed(1)}%
            </p>
          ))}
        </div>
      )
    }
    return null
  }

  return (
    <div className="space-y-8">
      {/* Bar Chart */}
      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Risk Scores by Company</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={barData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="name" 
              angle={-45}
              textAnchor="end"
              height={80}
              fontSize={12}
            />
            <YAxis 
              domain={[0, 100]}
              tickFormatter={(value) => `${value}%`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="overall" fill="#0ea5e9" name="Overall Risk" />
            <Bar dataKey="environmental" fill="#10b981" name="Environmental" />
            <Bar dataKey="social" fill="#3b82f6" name="Social" />
            <Bar dataKey="governance" fill="#8b5cf6" name="Governance" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Pie Chart */}
      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Risk Distribution</h3>
        <div className="flex items-center justify-center">
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={riskDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value, percent }) => `${name}: ${value} (${(percent * 100).toFixed(0)}%)`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {riskDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-green-50 p-4 rounded-lg border border-green-200">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
            <span className="text-sm font-medium text-green-800">Low Risk</span>
          </div>
          <div className="text-2xl font-bold text-green-900 mt-1">
            {riskDistribution[0].value}
          </div>
          <div className="text-xs text-green-600">
            {companies.length > 0 ? ((riskDistribution[0].value / companies.length) * 100).toFixed(1) : 0}% of companies
          </div>
        </div>

        <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></div>
            <span className="text-sm font-medium text-yellow-800">Medium Risk</span>
          </div>
          <div className="text-2xl font-bold text-yellow-900 mt-1">
            {riskDistribution[1].value}
          </div>
          <div className="text-xs text-yellow-600">
            {companies.length > 0 ? ((riskDistribution[1].value / companies.length) * 100).toFixed(1) : 0}% of companies
          </div>
        </div>

        <div className="bg-red-50 p-4 rounded-lg border border-red-200">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
            <span className="text-sm font-medium text-red-800">High Risk</span>
          </div>
          <div className="text-2xl font-bold text-red-900 mt-1">
            {riskDistribution[2].value}
          </div>
          <div className="text-xs text-red-600">
            {companies.length > 0 ? ((riskDistribution[2].value / companies.length) * 100).toFixed(1) : 0}% of companies
          </div>
        </div>
      </div>
    </div>
  )
}
