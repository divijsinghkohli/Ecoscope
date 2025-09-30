import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface CompanyAnalysis {
  company: string
  score: number
  risk_breakdown: {
    overall_score: number
    environmental_score: number
    social_score: number
    governance_score: number
  }
  events: Array<{
    event_type: string
    description: string
    severity: number
  }>
  articles: Array<{
    title: string
    content: string
    url: string
    published_at: string
    sentiment_score: number
    events: Array<{
      event_type: string
      description: string
      severity: number
    }>
  }>
  total_articles: number
  analyzed_at: string
}

export interface Company {
  id: number
  name: string
  overall_score: number
  environmental_score: number
  social_score: number
  governance_score: number
  last_analyzed: string
  total_articles: number
}

export const analyzeCompany = async (companyName: string): Promise<CompanyAnalysis> => {
  try {
    const response = await api.get(`/api/analyze?company=${encodeURIComponent(companyName)}`)
    return response.data
  } catch (error) {
    console.error('Error analyzing company:', error)
    throw error
  }
}

export const getCompanies = async (): Promise<Company[]> => {
  try {
    const response = await api.get('/api/companies')
    return response.data
  } catch (error) {
    console.error('Error fetching companies:', error)
    throw error
  }
}

export const getCompanyDetails = async (companyId: number): Promise<CompanyAnalysis> => {
  try {
    const response = await api.get(`/api/companies/${companyId}/details`)
    return response.data
  } catch (error) {
    console.error('Error fetching company details:', error)
    throw error
  }
}
