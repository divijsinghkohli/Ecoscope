'use client'

import { useState, useEffect } from 'react'
import { Search, TrendingUp, TrendingDown, AlertTriangle, CheckCircle } from 'lucide-react'
import CompanyTable from '../../components/CompanyTable'
import RiskChart from '../../components/RiskChart'
import { analyzeCompany, getCompanies } from '../../services/api'

interface Company {
  id: number
  name: string
  overall_score: number
  environmental_score: number
  social_score: number
  governance_score: number
  last_analyzed: string
  total_articles: number
}

export default function Dashboard() {
  const [companies, setCompanies] = useState<Company[]>([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [error, setError] = useState('')

  const fetchCompanies = async () => {
    try {
      const data = await getCompanies()
      setCompanies(data)
    } catch (err) {
      console.error('Failed to fetch companies:', err)
    }
  }

  useEffect(() => {
    fetchCompanies()
  }, [])

  const handleAnalyze = async () => {
    if (!searchTerm.trim()) {
      setError('Please enter a company name')
      return
    }

    setLoading(true)
    setError('')

    try {
      await analyzeCompany(searchTerm)
      await fetchCompanies() // Refresh the list
      setSearchTerm('')
    } catch (err) {
      setError('Failed to analyze company. Please try again.')
      console.error('Analysis failed:', err)
    } finally {
      setLoading(false)
    }
  }

  const getRiskLevel = (score: number) => {
    if (score < 0.3) return { level: 'Low', color: 'text-green-600', bgColor: 'bg-green-100' }
    if (score < 0.7) return { level: 'Medium', color: 'text-yellow-600', bgColor: 'bg-yellow-100' }
    return { level: 'High', color: 'text-red-600', bgColor: 'bg-red-100' }
  }

  const averageScore = companies.length > 0 
    ? companies.reduce((sum, company) => sum + company.overall_score, 0) / companies.length 
    : 0

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">ESG Risk Dashboard</h1>
          <p className="text-gray-600">Monitor and analyze ESG risks across your portfolio companies</p>
        </div>

        {/* Search Section */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <div className="flex gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Enter company name (e.g., Tesla, Google, Amazon)"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-900"
                />
              </div>
            </div>
            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-semibold flex items-center gap-2 transition-colors"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <TrendingUp className="w-5 h-5" />
                  Analyze
                </>
              )}
            </button>
          </div>
          {error && (
            <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
              {error}
            </div>
          )}
        </div>

        {/* Stats Cards */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Companies</p>
                <p className="text-2xl font-bold text-gray-900">{companies.length}</p>
              </div>
              <div className="p-3 bg-blue-100 rounded-full">
                <TrendingUp className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Average Risk Score</p>
                <p className="text-2xl font-bold text-gray-900">
                  {(averageScore * 100).toFixed(1)}%
                </p>
              </div>
              <div className="p-3 bg-yellow-100 rounded-full">
                <AlertTriangle className="w-6 h-6 text-yellow-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">High Risk</p>
                <p className="text-2xl font-bold text-red-600">
                  {companies.filter(c => c.overall_score >= 0.7).length}
                </p>
              </div>
              <div className="p-3 bg-red-100 rounded-full">
                <TrendingDown className="w-6 h-6 text-red-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Low Risk</p>
                <p className="text-2xl font-bold text-green-600">
                  {companies.filter(c => c.overall_score < 0.3).length}
                </p>
              </div>
              <div className="p-3 bg-green-100 rounded-full">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </div>
        </div>

        {/* Chart Section */}
        {companies.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Risk Score Distribution</h2>
            <RiskChart companies={companies} />
          </div>
        )}

        {/* Companies Table */}
        <div className="bg-white rounded-lg shadow-sm">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Company Analysis</h2>
            <p className="text-gray-600 mt-1">
              Detailed ESG risk analysis for all analyzed companies
            </p>
          </div>
          <CompanyTable companies={companies} />
        </div>
      </div>
    </div>
  )
}
