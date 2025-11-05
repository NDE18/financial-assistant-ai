from crewai import Agent, Task
from langchain_openai import ChatOpenAI
from app.config import get_settings
from typing import Dict, List
from datetime import datetime

settings = get_settings()

class AnalystAgent:
    """Agent specialized in financial analysis and insights generation"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL_GPT4,
            temperature=0.2
        )
    
    def create_agent(self) -> Agent:
        return Agent(
            role="Financial Analyst",
            goal="Provide deep financial insights and actionable recommendations",
            backstory="""You are a senior financial analyst with expertise in personal 
            and small business finance. You analyze spending patterns, identify trends, 
            calculate key financial metrics, and provide strategic recommendations for 
            better financial health. You're skilled at finding optimization opportunities 
            and predicting future cash flow needs.""",
            llm=self.llm,
            verbose=settings.AGENT_VERBOSE,
            allow_delegation=True
        )
    
    def analyze_spending_patterns(self, transactions: List[Dict], period: str) -> Task:
        """Analyze spending patterns over a period"""
        return Task(
            description=f"""
            Perform comprehensive spending analysis for the {period} period:
            
            Transactions: {len(transactions)} transactions
            
            Analyze:
            1. Total income vs expenses
            2. Category-wise spending breakdown
            3. Spending trends (increasing/decreasing)
            4. Top 5 expense categories
            5. Unusual spending patterns
            6. Month-over-month comparison if data available
            7. Savings rate
            
            Calculate key metrics:
            - Net cash flow
            - Savings rate
            - Expense ratio by category
            - Average transaction size
            - Burn rate
            
            Provide insights and recommendations for optimization.
            """,
            expected_output="Detailed JSON report with metrics, trends, and recommendations",
            agent=self.create_agent()
        )
    
    def budget_performance_analysis(self, budgets: List[Dict], actuals: List[Dict]) -> Task:
        """Analyze budget vs actual performance"""
        return Task(
            description=f"""
            Compare budget allocations with actual spending:
            
            Budgets: {budgets}
            Actual Spending: {actuals}
            
            For each budget category:
            1. Calculate variance (budget vs actual)
            2. Determine if over/under budget
            3. Calculate percentage used
            4. Project end-of-period status
            5. Identify categories needing attention
            
            Provide:
            - Overall budget health score (0-100)
            - Categories at risk
            - Recommendations for reallocation
            - Savings opportunities
            """,
            expected_output="JSON with budget analysis and recommendations",
            agent=self.create_agent()
        )
    
    def cash_flow_forecast(self, historical_data: List[Dict], num_months: int = 3) -> Task:
        """Forecast cash flow for upcoming months"""
        return Task(
            description=f"""
            Based on historical transaction data, forecast cash flow for the next {num_months} months:
            
            Historical Data: {historical_data}
            
            Create forecast considering:
            1. Historical income patterns
            2. Recurring expenses
            3. Seasonal variations
            4. Growth trends
            5. Known upcoming expenses
            
            For each forecasted month provide:
            - Expected income
            - Expected expenses
            - Projected balance
            - Confidence level
            - Risk factors
            
            Include recommendations for cash management.
            """,
            expected_output="JSON with monthly forecasts and confidence intervals",
            agent=self.create_agent()
        )
    
    def generate_insights(self, financial_data: Dict) -> Task:
        """Generate actionable insights from financial data"""
        return Task(
            description=f"""
            Analyze comprehensive financial data and generate insights:
            
            Data: {financial_data}
            
            Generate:
            1. Top 3 financial strengths
            2. Top 3 areas for improvement
            3. 5 actionable recommendations
            4. Potential cost savings
            5. Risk alerts
            6. Opportunities for optimization
            
            Make insights specific, actionable, and prioritized.
            """,
            expected_output="JSON with categorized insights and priority levels",
            agent=self.create_agent()
        )