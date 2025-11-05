from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from app.config import get_settings
from typing import Dict, List, Any
from app.agents.classifier_agent import ClassifierAgent
from app.agents.analyst_agent import AnalystAgent
from app.agents.reporter_agent import ReporterAgent
from app.agents.ocr_agent import OCRAgent

settings = get_settings()

class OrchestratorAgent:
    """Main orchestrator for collaborative agent workflows"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL_GPT4,
            temperature=0.3
        )
        
        # Initialize specialized agents
        self.classifier = ClassifierAgent()
        self.analyst = AnalystAgent()
        self.reporter = ReporterAgent()
        self.ocr = OCRAgent()
    
    def create_agent(self) -> Agent:
        return Agent(
            role="Financial Assistant Orchestrator",
            goal="Coordinate specialized agents to fulfill complex financial tasks efficiently",
            backstory="""You are the main coordinator of a team of financial AI agents.
            You understand user requests, break them down into subtasks, delegate to 
            specialized agents, and synthesize their outputs into coherent responses.
            You ensure all agents work collaboratively and efficiently.""",
            llm=self.llm,
            verbose=settings.AGENT_VERBOSE,
            allow_delegation=True
        )
    
    def process_transactions_workflow(self, transactions: List[Dict]) -> Crew:
        """Collaborative workflow: classify and analyze transactions"""
        
        # Create tasks
        classify_task = self.classifier.batch_classify_transactions(transactions)
        analyze_task = self.analyst.analyze_spending_patterns(
            transactions, 
            period="current"
        )
        
        # Create crew with collaborative process
        crew = Crew(
            agents=[
                self.classifier.create_agent(),
                self.analyst.create_agent()
            ],
            tasks=[classify_task, analyze_task],
            process=Process.sequential,  # Classifier first, then analyst
            verbose=settings.AGENT_VERBOSE
        )
        
        return crew
    
    def generate_comprehensive_report_workflow(self, data: Dict) -> Crew:
        """Collaborative workflow: analyze and generate report"""
        
        # Create tasks
        analysis_task = self.analyst.analyze_spending_patterns(
            data.get('transactions', []),
            data.get('period', 'monthly')
        )
        
        insights_task = self.analyst.generate_insights(data)
        
        report_task = self.reporter.generate_monthly_report({
            'analysis': '{{analysis_task.output}}',
            'insights': '{{insights_task.output}}',
            'raw_data': data
        })
        
        # Create crew
        crew = Crew(
            agents=[
                self.analyst.create_agent(),
                self.reporter.create_agent()
            ],
            tasks=[analysis_task, insights_task, report_task],
            process=Process.sequential,
            verbose=settings.AGENT_VERBOSE
        )
        
        return crew
    
    def process_invoice_workflow(self, image_path: str, image_base64: str) -> Crew:
        """Collaborative workflow: OCR and categorize invoice"""
        
        # Create tasks
        ocr_task = self.ocr.extract_invoice_data(image_path, image_base64)
        validate_task = self.ocr.validate_invoice_data('{{ocr_task.output}}')
        
        # Classify the transaction
        classify_task = self.classifier.classify_transaction({
            'description': '{{ocr_task.output.vendor}}',
            'amount': '{{ocr_task.output.total_amount}}',
            'type': 'expense',
            'date': '{{ocr_task.output.invoice_date}}'
        })
        
        # Create crew
        crew = Crew(
            agents=[
                self.ocr.create_agent(),
                self.classifier.create_agent()
            ],
            tasks=[ocr_task, validate_task, classify_task],
            process=Process.sequential,
            verbose=settings.AGENT_VERBOSE
        )
        
        return crew