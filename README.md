# VectorShift Integrations Platform

<div align="center">

![VectorShift](https://img.shields.io/badge/VectorShift-Integrations-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11+-green.svg)
![React](https://img.shields.io/badge/React-19.1.1-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-green.svg)
![Redis](https://img.shields.io/badge/Redis-6.3.0-red.svg)

*A modern, scalable integration platform connecting popular productivity tools through secure OAuth flows.*

</div>

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
- [Local Setup Guide](#-local-setup-guide)
- [How to Run](#-how-to-run)
- [File Structure](#-file-structure)
- [Environment Configuration](#-environment-configuration)
- [OAuth Integrations](#-oauth-integrations)
- [Development Tools](#-development-tools)

## 🎯 Project Overview

VectorShift Integrations is a comprehensive platform designed to connect and manage integrations with popular productivity and CRM tools. Built as part of a technical assessment, this platform demonstrates modern web development practices, secure OAuth implementation, and scalable architecture patterns.

## 🏛️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   External      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   APIs          │
│                 │    │                 │    │                 │
│ • OAuth UI      │    │ • OAuth Flow    │    │ • HubSpot       │
│ • Integration   │    │ • API Endpoints │    │ • Notion        │
│ • Data Display  │    │ • Data Processing│   │ • Airtable      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │     Redis       │
                       │   (Caching)     │
                       │                 │
                       │ • OAuth States  │
                       │ • Credentials   │
                       │ • Session Data  │
                       └─────────────────┘
```

## 🚀 Local Setup Guide

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** - [Download Python](https://python.org/downloads)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/download)
- **Redis Server** - [Redis Installation Guide](https://redis.io/download)
  - **Windows Users**: Redis is not natively supported on Windows. Use Docker to run Redis:
    ```bash
    docker run -d -p 6379:6379 redis:latest
    ```
- **Git** - [Download Git](https://git-scm.com/downloads)

### 📥 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Avinash-Acharya/VectorShift-Assignment.git
   cd VectorShift-Assignment
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   
   # Create virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Setup environment variables
   cp .env.example .env
   # Edit .env file with your actual credentials (see Environment Configuration)
   ```

3. **Frontend Setup:**
   ```bash
   cd ../frontend
   
   # Install dependencies
   npm install
   ```

4. **Redis Setup:**
   ```bash
   # For Linux/macOS:
   redis-server
   
   # For Windows (using Docker):
   docker run -d -p 6379:6379 redis:latest
   
   # Verify Redis is running (in another terminal)
   redis-cli ping  # For Linux/macOS
   docker exec -it <container_id> redis-cli ping  # For Windows Docker
   # Should return: PONG
   ```

## 🎮 How to Run

### 🔧 Quick Start (Automated)

Use the automated development script:

```bash
# From project root
python dev_setup.py
```

This script will:
- ✅ Validate environment configuration
- ✅ Check Redis connectivity
- ✅ Install dependencies
- ✅ Start the backend server

### 🔧 Manual Start

**Terminal 1 - Redis:**
```bash
# For Linux/macOS:
redis-server

# For Windows:
docker run -d -p 6379:6379 redis:latest
```

**Terminal 2 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm start
```

### 🔍 Verify Installation

1. **Backend Health Check:**
   ```bash
   curl http://localhost:8000/
   # Expected: {"Ping": "Pong"}
   ```

2. **Frontend Access:**
   - Open: `http://localhost:3000`
   - Should display the integration selection interface

3. **API Documentation:**
   - Open: `http://localhost:8000/docs`
   - Interactive Swagger documentation

## 📁 File Structure

```
VectorShift-Assignment/
├── 📁 backend/                     # FastAPI Backend
│   ├── 📁 integrations/            # Integration modules
│   │   ├── 🐍 airtable.py         # Airtable OAuth & API
│   │   ├── 🐍 hubspot.py          # HubSpot OAuth & API (New)
│   │   ├── 🐍 notion.py           # Notion OAuth & API
│   │   └── 🐍 integration_item.py # Data model
│   ├── 🐍 main.py                 # FastAPI app & endpoints
│   ├── 🐍 config.py               # Environment configuration
│   ├── 🐍 redis_client.py         # Redis connection & utilities
│   ├── 🐍 validate_env.py         # Environment validation script
│   ├── 📄 requirements.txt        # Python dependencies
│   ├── 📄 .env.example           # Environment template
│   └── 📄 .env                   # Environment variables (create this)
│
├── 📁 frontend/                    # React Frontend
│   ├── 📁 src/
│   │   ├── 📁 integrations/       # Integration components
│   │   │   ├── ⚛️ airtable.js    # Airtable UI component
│   │   │   ├── ⚛️ hubspot.js     # HubSpot UI component (New)
│   │   │   ├── ⚛️ notion.js      # Notion UI component
│   │   │   └── ⚛️ slack.js       # Placeholder
│   │   ├── ⚛️ App.js             # Main application
│   │   ├── ⚛️ integration-form.js # Integration selection
│   │   ├── ⚛️ data-form.js       # Data loading interface
│   │   ├── ⚛️ index.js           # App entry point
│   │   └── 🎨 index.css          # Global styles
│   ├── 📁 public/                 # Static assets
│   └── 📄 package.json           # Node.js dependencies
│
├── 🐍 dev_setup.py               # Development automation script
├── 📄 ENV_SETUP.md              # Environment setup guide
├── 📄 README.md                 # This file
├── 📄 .gitignore               # Git ignore rules
└── 📄 assignment.md            # Original assignment instructions
```

### 🔍 Key Components

#### Backend (`/backend`)
- **`main.py`** - FastAPI application with CORS and route definitions
- **`config.py`** - Centralized environment variable management
- **`integrations/`** - OAuth implementations for each platform
- **`redis_client.py`** - Redis connection and utility functions
- **`validate_env.py`** - Environment validation and setup verification

#### Frontend (`/frontend/src`)
- **`App.js`** - Main React application component
- **`integration-form.js`** - Integration selection and configuration UI
- **`data-form.js`** - Data loading and display interface
- **`integrations/`** - Platform-specific UI components for OAuth flows

## 🔐 Environment Configuration

### Required Environment Variables

Create a `.env` file in the `/backend` directory:

```bash
# HubSpot OAuth Credentials (Required)
HUBSPOT_CLIENT_ID=your-hubspot-client-id
HUBSPOT_CLIENT_SECRET=your-hubspot-client-secret

# Optional: Other Integrations
NOTION_CLIENT_ID=your-notion-client-id
NOTION_CLIENT_SECRET=your-notion-client-secret
AIRTABLE_CLIENT_ID=your-airtable-client-id
AIRTABLE_CLIENT_SECRET=your-airtable-client-secret

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Environment
ENVIRONMENT=development
```

### 🔑 Getting OAuth Credentials

#### HubSpot (Required)
1. Visit [HubSpot Developer Portal](https://developers.hubspot.com/)
2. Create a new app
3. Configure OAuth:
   - **Redirect URL**: `http://localhost:8000/integrations/hubspot/oauth2callback`
   - **Scopes**: `crm.objects.contacts.read`, `crm.objects.companies.read`, `crm.objects.deals.read`
   - ⚠️ **Important**: The redirect URL must point to the backend (port 8000), not the frontend (port 3000)
4. Copy Client ID and Secret to `.env`

#### Notion (Optional)
1. Visit [Notion Developers](https://developers.notion.com/)
2. Create a new integration
3. Configure OAuth redirect: `http://localhost:8000/integrations/notion/oauth2callback`

#### Airtable (Optional)
1. Visit [Airtable Developers](https://airtable.com/developers/web/api/oauth-reference)
2. Create a new OAuth app
3. Configure redirect: `http://localhost:8000/integrations/airtable/oauth2callback`

## 🛠️ Development Tools

### Environment Validation
```bash
cd backend
python validate_env.py
```

### Automated Setup
```bash
python dev_setup.py
```

### API Testing
```bash
# Health check
curl http://localhost:8000/

# Interactive docs
open http://localhost:8000/docs
```

### Development Mode
- **Backend**: Auto-reload enabled with `--reload`
- **Frontend**: Hot reload with React development server
- **Redis**: Persistent data storage for development

---

<div align="center">

**Built with ❤️ for VectorShift**

[Report Bug](https://github.com/Avinash-Acharya/VectorShift-Assignment/issues) • [Request Feature](https://github.com/Avinash-Acharya/VectorShift-Assignment/issues)

</div>
