from langchain.chat_models import AzureChatOpenAI
import openai
import os
from langchain import LLMChain, PromptTemplate
from pydantic import BaseModel, Field
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_RESOURCE")
openai.api_version = "2022-12-01"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")


from langchain.output_parsers import PydanticOutputParser


class Classification:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            deployment_name="gpt_turbo",
            openai_api_key=os.getenv("AZURE_OPENAI_KEY"),
            openai_api_base="https://testprojekt.openai.azure.com/",
            openai_api_version="2023-07-01-preview",
            openai_api_type="azure",
            temperature=0
        )

        self.response_schemas = [
            ResponseSchema(name="category", description="Die Klasse der Kategorie"),
            ResponseSchema(name="prob", description="Die Wahrscheinlichkeit, mit der du die Klasse vergibst."),
            ResponseSchema(name="prob_all_classes", description="Die Wahrscheinlichkeit, mit der du alle Klassen vergibst als Liste.")
        ]

        self.category_prompt = PromptTemplate.from_template("""
            Klassifiziere die folgende E-Mail in eine von drei Kategorien: 'Jobanfrage', 'Spam' oder 'Sonstiges'...
            Klassifiziere diese Email: {email_content}   
            Hier noch ein Hinweise zur Ausgabe deines Outputs:
            {format_instructions}
        """)

    def process_email(self, email_content):
        output_parser = StructuredOutputParser.from_response_schemas(self.response_schemas)
        format_instructions = output_parser.get_format_instructions()
        chain = self.category_prompt | self.llm | output_parser

        result = chain.invoke({"email_content": email_content, "format_instructions": format_instructions})
        return result