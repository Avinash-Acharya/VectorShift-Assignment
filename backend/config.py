"""
Configuration module for environment variables and settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for application settings."""
    
    # HubSpot Configuration
    HUBSPOT_CLIENT_ID = os.getenv('HUBSPOT_CLIENT_ID')
    HUBSPOT_CLIENT_SECRET = os.getenv('HUBSPOT_CLIENT_SECRET')
    
    # Notion Configuration (optional)
    NOTION_CLIENT_ID = os.getenv('NOTION_CLIENT_ID')
    NOTION_CLIENT_SECRET = os.getenv('NOTION_CLIENT_SECRET')
    
    # Airtable Configuration (optional)
    AIRTABLE_CLIENT_ID = os.getenv('AIRTABLE_CLIENT_ID')
    AIRTABLE_CLIENT_SECRET = os.getenv('AIRTABLE_CLIENT_SECRET')
    
    # Redis Configuration
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    
    # Application Configuration
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    @classmethod
    def validate_hubspot_credentials(cls):
        """Validate that HubSpot credentials are present."""
        if not cls.HUBSPOT_CLIENT_ID or not cls.HUBSPOT_CLIENT_SECRET:
            raise ValueError(
                "Missing HubSpot credentials. Please set HUBSPOT_CLIENT_ID and "
                "HUBSPOT_CLIENT_SECRET environment variables in your .env file."
            )
        return True
    
    @classmethod
    def validate_notion_credentials(cls):
        """Validate that Notion credentials are present."""
        if not cls.NOTION_CLIENT_ID or not cls.NOTION_CLIENT_SECRET:
            raise ValueError(
                "Missing Notion credentials. Please set NOTION_CLIENT_ID and "
                "NOTION_CLIENT_SECRET environment variables in your .env file."
            )
        return True
    
    @classmethod
    def validate_airtable_credentials(cls):
        """Validate that Airtable credentials are present."""
        if not cls.AIRTABLE_CLIENT_ID or not cls.AIRTABLE_CLIENT_SECRET:
            raise ValueError(
                "Missing Airtable credentials. Please set AIRTABLE_CLIENT_ID and "
                "AIRTABLE_CLIENT_SECRET environment variables in your .env file."
            )
        return True

# Create a config instance
config = Config()
