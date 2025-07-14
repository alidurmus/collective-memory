#!/usr/bin/env python3
"""
🏗️ Context Engineering - Project Setup
Collective Memory System Initialization
"""

import os
import subprocess
import sys
import json


def setup_environment():
    """Setup the development environment"""
    print("🚀 Setting up Collective Memory environment...")
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        sys.exit(1)
    
    # Install dependencies
    print("📦 Installing dependencies...")
    subprocess.run([
        sys.executable, "-m", "pip", "install", "-r",
        "../collective-memory-app/requirements.txt"
    ])
    
    # Setup frontend
    print("🎨 Setting up frontend...")
    os.chdir("../collective-memory-app/frontend")
    subprocess.run(["npm", "install"])
    
    print("✅ Setup complete!")
    print("🌐 Run 'npm run dev' in collective-memory-app/frontend to start")


def create_config():
    """Create default configuration"""
    config = {
        "project_name": "Collective Memory",
        "version": "2.1.0",
        "context_engineering": True,
        "test_framework": "pytest + playwright",
        "ui_framework": "Context7"
    }
    
    with open("../context-engineering/context/config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("⚙️ Configuration created at context/config.json")


if __name__ == "__main__":
    setup_environment()
    create_config() 