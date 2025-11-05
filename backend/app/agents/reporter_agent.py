from crewai import Agent, Task
from langchain_openai import ChatOpenAI
from app.config import get_settings
from typing import Dict, List

settings = get_settings()

class ReporterAgent:
    """Agent specialized in generating financial reports"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL_GPT4,
            temperature=0.4
        )
    
    def create_agent(self) -> Agent:
        return Agent(
            role="Financial Reporter",
            goal="Create comprehensive, clear, and actionable financial reports",
            backstory="""You are an experienced financial reporter who creates 
            professional reports for individuals and small businesses. You excel at 
            synthesizing complex financial data into clear narratives, highlighting 
            key metrics, and presenting actionable insights in an easy-to-understand format.
            Your reports are known for being thorough yet concise.""",
            llm=self.llm,
            verbose=settings.AGENT_VERBOSE,
            allow_delegation=True
        )
    
    def generate_monthly_report(self, data: Dict) -> Task:
        """Generate a comprehensive monthly financial report"""
        return Task(
            description=f"""
            Create a professional monthly financial report with the following data:
            
            {data}
            
            Report Structure:
            1. Executive Summary (key highlights and alerts)
            2. Income Statement (total income, breakdown by source)
            3. Expense Analysis (total expenses, breakdown by category)
            4. Cash Flow Summary (opening balance, inflows, outflows, closing balance)
            5. Budget Performance (vs budget comparison)
            6. Key Metrics (savings rate, expense ratio, burn rate)
            7. Trends & Patterns (MoM comparison, notable changes)
            8. Recommendations (top 3-5 actionable items)
            9. Outlook (next month projections)
            
            Format: Structured markdown with clear sections and bullet points.
            Include specific numbers and percentages.
            """,
            expected_output="Comprehensive monthly report in markdown format",
            agent=self.create_agent()
        )
    
    def create_category_report(self, category: str, transactions: List[Dict]) -> Task:
        """Generate detailed report for a specific category"""
        return Task(
            description=f"""
            Create detailed analysis report for category: {category}
            
            Transactions: {transactions}
            
            Include:
            1. Total spending in this category
            2. Number of transactions
            3. Average transaction amount
            4. Largest and smallest transactions
            5. Spending trend over time
            6. Percentage of total budget
            7. Comparison with previous periods
            8. Notable transactions
            9. Optimization suggestions
            
            Make it specific to this category with actionable insights.
            """,
            expected_output="Category-specific report in markdown",
            agent=self.create_agent()
        )
    
    def generate_executive_summary(self, period_data: Dict) -> Task:
        """Create high-level executive summary"""
        return Task(
            description=f"""
            Create concise executive summary for decision-makers:
            
            Data: {period_data}
            
            Include (max 500 words):
            1. Financial Health Score (0-100)
            2. Top 3 Key Achievements
            3. Top 3 Concerns/Risks
            4. Critical Actions Required
            5. One-sentence overall assessment
            
            Use clear, business-oriented language.
            Prioritize actionable information.
            """,
            expected_output="Executive summary in markdown",
            agent=self.create_agent()
        )