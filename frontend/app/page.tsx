import Link from 'next/link'
import { ArrowRight, BarChart3, Shield, TrendingUp } from 'lucide-react'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            ESG Risk Analyzer
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            AI-powered ESG risk analysis that scrapes company news, analyzes risk mentions, 
            and ranks companies by ESG risk score on an intuitive dashboard.
          </p>
          <div className="flex justify-center gap-4 mb-12">
            <Link
              href="/dashboard"
              className="bg-primary-600 hover:bg-primary-700 text-white px-8 py-3 rounded-lg font-semibold flex items-center gap-2 transition-colors"
            >
              Go to Dashboard
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <div className="flex items-center mb-4">
              <BarChart3 className="w-8 h-8 text-primary-600 mr-3" />
              <h3 className="text-xl font-semibold">Risk Analysis</h3>
            </div>
            <p className="text-gray-600">
              Comprehensive ESG risk scoring based on environmental, social, and governance factors 
              extracted from recent news articles.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-lg">
            <div className="flex items-center mb-4">
              <Shield className="w-8 h-8 text-primary-600 mr-3" />
              <h3 className="text-xl font-semibold">AI-Powered</h3>
            </div>
            <p className="text-gray-600">
              Advanced NLP pipeline with sentiment analysis and named entity recognition 
              to identify ESG-related events and risks.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-lg">
            <div className="flex items-center mb-4">
              <TrendingUp className="w-8 h-8 text-primary-600 mr-3" />
              <h3 className="text-xl font-semibold">Real-time Updates</h3>
            </div>
            <p className="text-gray-600">
              Continuously updated risk scores based on the latest news and events 
              affecting your portfolio companies.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
