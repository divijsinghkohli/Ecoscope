'use client'

import { useState } from 'react'
import { ChevronDown, ChevronRight, ExternalLink, Calendar, FileText } from 'lucide-react'
import { Company } from '../services/api'

interface CompanyTableProps {
  companies: Company[]
}

export default function CompanyTable({ companies }: CompanyTableProps) {
  const [expandedRows, setExpandedRows] = useState<Set<number>>(new Set())

  const toggleRow = (companyId: number) => {
    const newExpanded = new Set(expandedRows)
    if (newExpanded.has(companyId)) {
      newExpanded.delete(companyId)
    } else {
      newExpanded.add(companyId)
    }
    setExpandedRows(newExpanded)
  }

  const getRiskLevel = (score: number) => {
    if (score < 0.3) return { level: 'Low', color: 'text-green-600', bgColor: 'bg-green-100' }
    if (score < 0.7) return { level: 'Medium', color: 'text-yellow-600', bgColor: 'bg-yellow-100' }
    return { level: 'High', color: 'text-red-600', bgColor: 'bg-red-100' }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (companies.length === 0) {
    return (
      <div className="p-8 text-center text-gray-500">
        <FileText className="w-12 h-12 mx-auto mb-4 text-gray-300" />
        <p className="text-lg">No companies analyzed yet</p>
        <p className="text-sm">Use the search box above to analyze your first company</p>
      </div>
    )
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Company
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Overall Risk
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Environmental
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Social
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Governance
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Articles
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Last Analyzed
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {companies.map((company) => {
            const isExpanded = expandedRows.has(company.id)
            const overallRisk = getRiskLevel(company.overall_score)
            
            return (
              <>
                <tr key={company.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <button
                        onClick={() => toggleRow(company.id)}
                        className="mr-2 p-1 hover:bg-gray-200 rounded"
                      >
                        {isExpanded ? (
                          <ChevronDown className="w-4 h-4" />
                        ) : (
                          <ChevronRight className="w-4 h-4" />
                        )}
                      </button>
                      <div className="text-sm font-medium text-gray-900">
                        {company.name}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${overallRisk.bgColor} ${overallRisk.color}`}>
                        {overallRisk.level}
                      </span>
                      <span className="ml-2 text-sm text-gray-600">
                        {(company.overall_score * 100).toFixed(1)}%
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {(company.environmental_score * 100).toFixed(1)}%
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {(company.social_score * 100).toFixed(1)}%
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {(company.governance_score * 100).toFixed(1)}%
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {company.total_articles}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    <div className="flex items-center">
                      <Calendar className="w-4 h-4 mr-1" />
                      {formatDate(company.last_analyzed)}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button className="text-primary-600 hover:text-primary-900 flex items-center">
                      <ExternalLink className="w-4 h-4 mr-1" />
                      View Details
                    </button>
                  </td>
                </tr>
                {isExpanded && (
                  <tr>
                    <td colSpan={8} className="px-6 py-4 bg-gray-50">
                      <div className="space-y-4">
                        <div>
                          <h4 className="text-sm font-medium text-gray-900 mb-2">Risk Breakdown</h4>
                          <div className="grid grid-cols-3 gap-4">
                            <div className="bg-white p-3 rounded border">
                              <div className="text-xs text-gray-500">Environmental</div>
                              <div className="text-lg font-semibold text-green-600">
                                {(company.environmental_score * 100).toFixed(1)}%
                              </div>
                            </div>
                            <div className="bg-white p-3 rounded border">
                              <div className="text-xs text-gray-500">Social</div>
                              <div className="text-lg font-semibold text-blue-600">
                                {(company.social_score * 100).toFixed(1)}%
                              </div>
                            </div>
                            <div className="bg-white p-3 rounded border">
                              <div className="text-xs text-gray-500">Governance</div>
                              <div className="text-lg font-semibold text-purple-600">
                                {(company.governance_score * 100).toFixed(1)}%
                              </div>
                            </div>
                          </div>
                        </div>
                        <div>
                          <h4 className="text-sm font-medium text-gray-900 mb-2">Analysis Summary</h4>
                          <p className="text-sm text-gray-600">
                            Analyzed {company.total_articles} articles. Last updated on{' '}
                            {formatDate(company.last_analyzed)}. Overall risk level is{' '}
                            <span className={`font-medium ${overallRisk.color}`}>
                              {overallRisk.level}
                            </span>.
                          </p>
                        </div>
                      </div>
                    </td>
                  </tr>
                )}
              </>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
