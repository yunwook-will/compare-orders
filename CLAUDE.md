# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Quick Start (One-Click)
```bash
python3 run.py                    # Starts both backend and frontend automatically
python3 manager.py                # Interactive start/stop/status manager
```

### Individual Services
```bash
# Backend (FastAPI)
cd backend
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload     # Runs on http://localhost:8000

# Frontend (React + TypeScript)
cd frontend
npm install
npm start                         # Runs on http://localhost:3000
npm run build                     # Production build
npm test                          # Run tests
```

### Alternative Deployment
```bash
docker-compose up --build         # Docker deployment
./start.sh                        # Shell script startup
./stop.sh                         # Clean shutdown
```

## Architecture Overview

### Core Application Structure
- **Backend**: Single FastAPI app (`backend/app/main.py`) with embedded Excel comparison logic
- **Frontend**: React SPA with TypeScript, using Ant Design components
- **Communication**: REST API with file upload endpoints, no database required
- **Data Flow**: Excel files → Pandas DataFrames → Comparison analysis → JSON API → React UI

### Key Components

**Backend (`ExcelComparator` class)**:
- `get_summary()`: Basic file statistics (rows, orders, common/different counts)
- `get_exclusive_orders()`: Orders that exist in only one file
- `get_shipping_differences()`: Order-level shipping fee analysis
- `get_amount_differences()`: Field-level amount comparisons
- `get_column_comparison()`: Column structure differences

**Frontend (Single Page App)**:
- Main comparison interface with file upload (drag & drop)
- Four analysis tabs: Shipping Differences, Amount Comparison, Exclusive Orders, Column Comparison
- Uses `ComparisonResult` interface for type-safe API responses

### API Configuration
- CORS configured for `localhost:3000` in development
- Frontend API URL configurable via `REACT_APP_API_URL` environment variable
- See `frontend/.env.example` for configuration template

### Excel Processing Logic
The comparison engine expects Korean Excel files with these standard columns:
- `주문번호` (Order Number) - Primary key for comparison
- `배송비` (Shipping Fee) - For shipping analysis
- `판매액`, `공급단가`, `공급가액` (Sales amounts) - For financial comparison
- `상품코드`, `수취인명` (Product code, Customer name) - For order details

### Deployment Options
Multiple packaging scripts available:
- `deploy.py`: Creates portable single Python file
- `create_package.py`: ZIP package with installer
- `build_executable.py`: PyInstaller executable
- `create_electron_app.py`: Desktop application

## Development Notes

### File Upload Handling
- Backend processes uploaded Excel files in temporary directories
- Files are automatically cleaned up after processing
- Supports both .xlsx and .xls formats

### Error Handling
- Backend validates file formats and provides descriptive error messages
- Frontend displays loading states and error alerts
- CORS issues commonly occur when API URL configuration is incorrect

### Korean Language Support
- UI and data processing designed for Korean Excel files
- CSV exports use `utf-8-sig` encoding for proper Korean character display
- Column names and data expected in Korean

### Environment Configuration
- Development: Uses localhost URLs
- Production: Configure `REACT_APP_API_URL` environment variable
- No authentication or user management implemented