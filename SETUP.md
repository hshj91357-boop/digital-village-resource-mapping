# Setup Guide - Digital Village Resource Mapping

## Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- Git

## Quick Start with Docker

### 1. Clone the Repository

```bash
git clone https://github.com/hshj91357-boop/digital-village-resource-mapping.git
cd digital-village-resource-mapping
```

### 2. Create Environment File

```bash
cp .env.example .env
```

### 3. Start All Services

```bash
docker-compose up --build
```

Services will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **PgAdmin**: http://localhost:5050

### 4. Access the Application

1. Open http://localhost:3000 in your browser
2. Explore the dashboard, map view, and analysis tools

## Local Development (Without Docker)

### Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/village_gis

# Run migrations (if any)
alembic upgrade head

# Start FastAPI server
uvicorn main:app --reload
```

### Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Set environment variables
export REACT_APP_API_URL=http://localhost:8000

# Start development server
npm start
```

## Database Setup

The database initializes automatically with Docker Compose.

To manually initialize PostGIS:

```sql
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
```

## File Structure

```
digital-village-resource-mapping/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── core/
│   │   ├── models/
│   │   └── schemas/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── styles/
│   │   └── types/
│   ├── package.json
│   └── Dockerfile.dev
├── data/
│   ├── sample_villages.geojson
│   └── sample_infrastructure.csv
├── docker-compose.yml
└── README.md
```

## Next Steps

1. **Phase 2**: Integrate GIS layers (satellite imagery, terrain, elevation)
2. **Phase 3**: Add Earth Engine API for real remote sensing data
3. **Phase 4**: Implement YOLOv11 and SAM for AI detection
4. **Phase 5**: Build analytics (flood risk maps, priority zones)
5. **Phase 6**: Add validation, reporting, and deployment

See [README.md](README.md) for full project documentation.
