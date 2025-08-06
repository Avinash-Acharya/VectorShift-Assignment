#!/usr/bin/env python3
"""
Development setup and run script for VectorShift Integrations.
This script helps with environment setup and running the application.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description, check=True):
    """Run a shell command with error handling."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"   {result.stdout.strip()}")
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False

def check_env_file():
    """Check if .env file exists and create from example if not."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("📝 Creating .env file from .env.example...")
            shutil.copy(env_example, env_file)
            print("✅ .env file created")
            print("⚠️  Please edit .env file with your actual credentials before continuing")
            return False
        else:
            print("❌ Neither .env nor .env.example file found")
            return False
    return True

def validate_environment():
    """Validate environment configuration."""
    print("🔍 Validating environment...")
    return run_command("python validate_env.py", "Environment validation")

def check_redis():
    """Check if Redis is running."""
    print("🗄️ Checking Redis connection...")
    return run_command("redis-cli ping", "Redis connectivity check", check=False)

def install_dependencies():
    """Install Python dependencies."""
    print("📦 Installing dependencies...")
    return run_command("pip install -r requirements.txt", "Installing requirements")

def start_application():
    """Start the FastAPI application."""
    print("🚀 Starting application...")
    print("   Application will be available at: http://localhost:8000")
    print("   API documentation: http://localhost:8000/docs")
    print("   Press Ctrl+C to stop the server")
    print("-" * 50)
    
    os.system("uvicorn main:app --reload")

def main():
    """Main development script."""
    print("🎯 VectorShift Integrations - Development Setup")
    print("=" * 50)
    
    # Change to backend directory
    if Path("backend").exists():
        os.chdir("backend")
        print("📁 Changed to backend directory")
    elif not Path("main.py").exists():
        print("❌ Please run this script from the project root or backend directory")
        sys.exit(1)
    
    # Step 1: Check/create .env file
    if not check_env_file():
        print("\n💡 Next steps:")
        print("   1. Edit the .env file with your actual credentials")
        print("   2. Run this script again")
        print("   3. See ENV_SETUP.md for detailed instructions")
        sys.exit(1)
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Step 3: Validate environment
    if not validate_environment():
        print("❌ Environment validation failed")
        print("💡 Please check your .env file and fix any issues")
        sys.exit(1)
    
    # Step 4: Check Redis
    if not check_redis():
        print("⚠️  Redis is not running or not accessible")
        print("💡 Please start Redis with: redis-server")
        print("   Continue anyway? (y/N): ", end="")
        if input().lower() != 'y':
            sys.exit(1)
    
    print("\n✅ All checks passed!")
    print("-" * 50)
    
    # Step 5: Start application
    start_application()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
