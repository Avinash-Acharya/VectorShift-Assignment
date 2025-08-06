"""
Startup validation script to check environment configuration.
Run this script to validate your environment setup before starting the application.
"""

from config import config
import sys

def validate_environment():
    """Validate environment configuration and provide helpful feedback."""
    print("🔍 Validating environment configuration...\n")
    
    issues = []
    warnings = []
    
    # Check HubSpot credentials (required for the assignment)
    print("🔑 Checking HubSpot credentials...")
    try:
        config.validate_hubspot_credentials()
        print("✅ HubSpot credentials are configured")
    except ValueError as e:
        issues.append(f"❌ HubSpot: {e}")
    
    # Check optional integrations
    print("\n🔑 Checking optional integration credentials...")
    
    # Notion
    try:
        config.validate_notion_credentials()
        print("✅ Notion credentials are configured")
    except ValueError:
        warnings.append("⚠️  Notion credentials not configured (optional)")
    
    # Airtable
    try:
        config.validate_airtable_credentials()
        print("✅ Airtable credentials are configured")
    except ValueError:
        warnings.append("⚠️  Airtable credentials not configured (optional)")
    
    # Check Redis configuration
    print(f"\n🗄️ Redis configuration:")
    print(f"   Host: {config.REDIS_HOST}")
    print(f"   Port: {config.REDIS_PORT}")
    print(f"   DB: {config.REDIS_DB}")
    
    # Check environment
    print(f"\n🌍 Environment: {config.ENVIRONMENT}")
    
    # Summary
    print("\n" + "="*50)
    print("📋 VALIDATION SUMMARY")
    print("="*50)
    
    if issues:
        print("\n❌ CRITICAL ISSUES (must be fixed):")
        for issue in issues:
            print(f"   {issue}")
    
    if warnings:
        print("\n⚠️  WARNINGS (optional):")
        for warning in warnings:
            print(f"   {warning}")
    
    if not issues and not warnings:
        print("\n🎉 All configurations are properly set!")
    elif not issues:
        print("\n✅ Required configurations are set. Optional warnings can be ignored.")
    
    # Instructions
    if issues:
        print(f"\n📝 TO FIX ISSUES:")
        print(f"   1. Edit the .env file in the backend/ directory")
        print(f"   2. Set the missing environment variables")
        print(f"   3. Run this script again to validate")
        print(f"   4. See ENV_SETUP.md for detailed instructions")
        return False
    
    print(f"\n🚀 Ready to start the application!")
    print(f"   Run: uvicorn main:app --reload")
    return True

if __name__ == "__main__":
    try:
        success = validate_environment()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Validation failed with error: {e}")
        print(f"💡 Make sure you have a .env file in the backend/ directory")
        sys.exit(1)
