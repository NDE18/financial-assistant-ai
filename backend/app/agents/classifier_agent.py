from crewai import Agent, Task
from langchain_openai import ChatOpenAI
from app.config import get_settings
from typing import Dict, List

settings = get_settings()

class ClassifierAgent:
    """Agent specialized in transaction classification and categorization"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL_GPT35,
            temperature=0.3
        )
        
    def create_agent(self) -> Agent:
        return Agent(
            role="Transaction Classifier",
            goal="Accurately categorize financial transactions and detect patterns",
            backstory="""You are an expert financial analyst specialized in transaction 
            categorization. You understand spending patterns, can identify transaction types, 
            and accurately assign categories based on transaction descriptions, amounts, and context.
            You also detect recurring transactions and potential duplicates.""",
            llm=self.llm,
            verbose=settings.AGENT_VERBOSE,
            allow_delegation=False
        )
    
    def classify_transaction(self, transaction_data: Dict) -> Task:
        """Create a task to classify a single transaction"""
        return Task(
            description=f"""
            Analyze and classify this transaction:
            - Description: {transaction_data.get('description')}
            - Amount: {transaction_data.get('amount')}
            - Type: {transaction_data.get('type')}
            - Date: {transaction_data.get('date')}
            
            Determine:
            1. The most appropriate category (e.g., Groceries, Transport, Salary, etc.)
            2. Relevant tags for better organization
            3. Whether this appears to be a recurring transaction
            4. Confidence score (0-1) for your classification
            5. Any notes or observations
            
            Return a JSON object with: category, tags, is_recurring, confidence_score, notes
            """,
            expected_output="A JSON object with classification results",
            agent=self.create_agent()
        )
    
    def batch_classify_transactions(self, transactions: List[Dict]) -> Task:
        """Create a task to classify multiple transactions"""
        return Task(
            description=f"""
            Analyze and classify these {len(transactions)} transactions efficiently.
            Look for patterns, recurring transactions, and similar items.
            
            Transactions:
            {transactions}
            
            For each transaction provide:
            - category
            - tags (list)
            - is_recurring (boolean)
            - confidence_score (0-1)
            - notes
            
            Also identify any potential duplicates or suspicious transactions.
            """,
            expected_output="A JSON array of classification results for all transactions",
            agent=self.create_agent()
        )
    
    def detect_anomalies(self, transaction_data: Dict, historical_data: List[Dict]) -> Task:
        """Detect unusual transactions based on historical patterns"""
        return Task(
            description=f"""
            Analyze this transaction against historical spending patterns:
            
            Current Transaction:
            {transaction_data}
            
            Historical Average Spending:
            {historical_data}
            
            Determine if this transaction is:
            1. Unusual in amount compared to similar transactions
            2. In an unexpected category for this user
            3. Potentially fraudulent
            4. Needs verification
            
            Provide anomaly score (0-1) and explanation.
            """,
            expected_output="JSON with anomaly_score, is_anomaly, reason, requires_verification",
            agent=self.create_agent()
        )
