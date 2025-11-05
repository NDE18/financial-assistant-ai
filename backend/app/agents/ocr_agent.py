from crewai import Agent, Task
from langchain_openai import ChatOpenAI
from app.config import get_settings
from typing import Dict
import base64

settings = get_settings()

class OCRAgent:
    """Agent specialized in invoice OCR using GPT-4 Vision"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL_VISION,
            temperature=0.1
        )
    
    def create_agent(self) -> Agent:
        return Agent(
            role="Invoice OCR Specialist",
            goal="Extract accurate financial data from invoice images and PDFs",
            backstory="""You are an expert in document analysis and data extraction. 
            You specialize in reading invoices, receipts, and financial documents from 
            various formats. You can identify key information like vendor names, amounts, 
            dates, invoice numbers, and line items with high accuracy. You validate 
            extracted data for consistency and flag any uncertainties.""",
            llm=self.llm,
            verbose=settings.AGENT_VERBOSE,
            allow_delegation=False
        )
    
    def extract_invoice_data(self, image_path: str, image_base64: str) -> Task:
        """Extract data from invoice image"""
        return Task(
            description=f"""
            Analyze this invoice image and extract all relevant financial information:
            
            Image: {image_path}
            
            Extract:
            1. Vendor/Company name
            2. Invoice number
            3. Invoice date (format: YYYY-MM-DD)
            4. Due date (format: YYYY-MM-DD)
            5. Total amount (numeric value)
            6. Tax/VAT amount (if present)
            7. Currency
            8. Line items (description and amounts)
            9. Payment terms
            10. Vendor contact information
            
            Also provide:
            - Extracted raw text
            - Confidence score for each field (0-1)
            - Any unclear or missing fields
            - Document quality assessment
            
            Return structured JSON with all fields.
            If any field is unclear, mark it with low confidence and explain why.
            """,
            expected_output="JSON with extracted invoice data and confidence scores",
            agent=self.create_agent()
        )
    
    def validate_invoice_data(self, extracted_data: Dict) -> Task:
        """Validate extracted invoice data for consistency"""
        return Task(
            description=f"""
            Validate the extracted invoice data for consistency and completeness:
            
            Extracted Data: {extracted_data}
            
            Check:
            1. Date logic (invoice date <= due date)
            2. Amount calculations (line items sum to total)
            3. Required fields present
            4. Format validity (dates, amounts)
            5. Reasonable values (not negative, not excessively large)
            
            Flag any issues and suggest corrections.
            Provide validation status and confidence level.
            """,
            expected_output="JSON with validation results and any issues found",
            agent=self.create_agent()
        )