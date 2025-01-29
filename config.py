import os

# MySQL Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
DB_NAME = os.getenv("DB_NAME", "faq_assistant")

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
