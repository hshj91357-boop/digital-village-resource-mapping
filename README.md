# Digital Village Resource Mapping

🏘️ **AI-powered GIS platform for Smart India Hackathon**

A comprehensive geospatial information system (GIS) platform for mapping village resources, infrastructure, and development needs using satellite imagery, computer vision, and deep learning.

## Features

### 📍 GIS Core
- Village boundary upload (GeoJSON, Shapefile, draw polygon)
- Multi-layer map visualization (satellite, terrain, roads, buildings)
- PostGIS spatial database
- QGIS compatibility

### 🤖 AI & Computer Vision
- **Building Detection**: YOLOv11 object detection
- **Land Use Segmentation**: Segment Anything Model (SAM)
- **Water Tank Detection**: Custom YOLO training
- **Road Network Analysis**: Computer vision-based extraction
- **Solar Panel Detection**: Renewable energy mapping

### 📊 Analytics & Decision Support
- Flood Risk Maps
- Water Scarcity Analysis
- Infrastructure Gap Analysis
- Accessibility Maps
- Renewable Energy Suitability
- Priority Development Zones

### 📈 Dashboard & Reporting
- Interactive KPI dashboard
- Customizable charts (flood risk, infrastructure distribution, population trends)
- PDF report generation
- GeoJSON export
- CSV export

### 🔍 Validation & Accuracy
- Compare predictions with historical records
- Expert-labeled ground truth validation
- Accuracy metrics (Precision, Recall, F1, IoU)
- Validation report generation

## Technology Stack

### Frontend
- **React 18** + TypeScript
- **Tailwind CSS** for styling
- **Leaflet** for interactive maps
- **Chart.js** for data visualization
- **Shadcn UI** for components

### Backend
- **FastAPI** (Python)
- **PostgreSQL** + **PostGIS** for spatial data
- **SQLAlchemy** ORM
- **Pydantic** for validation

### GIS & Remote Sensing
- **GeoPandas** for spatial data processing
- **Rasterio** for raster data
- **GDAL** for geospatial utilities
- **Google Earth Engine API** for satellite imagery
- **QGIS** for GIS operations

### AI & Computer Vision
- **YOLOv11** for object detection
- **Segment Anything (SAM)** for segmentation
- **PyTorch** for deep learning
- **OpenCV** for image processing

### DevOps
- **Docker** & **Docker Compose** for containerization
- **Streamlit** for demo deployment

## Quick Start

### Using Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/hshj91357-boop/digital-village-resource-mapping.git
cd digital-village-resource-mapping

# Create environment file
cp .env.example .env

# Start all services
docker-compose up --build
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Database Admin: http://localhost:5050

### Local Development

See [SETUP.md](SETUP.md) for detailed local development setup.

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/routes/       # API endpoints
│   │   ├── core/             # Config, database
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   └── services/         # Business logic
│   ├── main.py              # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/           # Page views
│   │   ├── services/        # API client
│   │   ├── styles/          # CSS styles
│   │   └── types/           # TypeScript types
│   ├── package.json
│   └── Dockerfile.dev
├── data/
│   ├── sample_villages.geojson
│   └── sample_infrastructure.csv
└── docker-compose.yml
```

## Development Roadmap

### Phase 1: ✅ UI Foundation
- [x] Folder structure
- [x] React + TypeScript frontend
- [x] FastAPI backend skeleton
- [x] PostgreSQL + PostGIS setup
- [x] Docker Compose configuration
- [x] Basic dashboard & map views

### Phase 2: 🔄 GIS Integration
- [ ] Multi-layer map implementation
- [ ] Satellite imagery integration
- [ ] Vector layer management
- [ ] Village boundary upload
- [ ] Layer controls and legends

### Phase 3: 🛰️ Remote Sensing
- [ ] Google Earth Engine integration
- [ ] Real satellite imagery retrieval
- [ ] Terrain and elevation data
- [ ] Rainfall and climate data
- [ ] NDVI and vegetation indices

### Phase 4: 🤖 AI Detection
- [ ] YOLOv11 building detection
- [ ] Segment Anything land use segmentation
- [ ] Water tank detection
- [ ] Solar panel detection
- [ ] Road network extraction
- [ ] Model fine-tuning with real data

### Phase 5: 📊 Analytics
- [ ] Flood risk map generation
- [ ] Water scarcity analysis
- [ ] Infrastructure gap analysis
- [ ] Priority development zones
- [ ] Renewable energy suitability
- [ ] Development recommendations

### Phase 6: ✔️ Validation & Deployment
- [ ] Expert ground truth integration
- [ ] Accuracy metrics calculation
- [ ] Validation report generation
- [ ] PDF/CSV export
- [ ] Streamlit demo deployment
- [ ] Testing suite

## API Endpoints

### Villages
- `GET /api/villages/` - List all villages
- `POST /api/villages/` - Create village
- `GET /api/villages/{id}` - Get village
- `DELETE /api/villages/{id}` - Delete village

### Infrastructure
- `GET /api/infrastructure/{village_id}` - List infrastructure
- `POST /api/infrastructure/` - Create infrastructure

### Analysis
- `GET /api/analysis/{village_id}` - Get analysis results
- `POST /api/analysis/trigger/{village_id}` - Trigger analysis

### AI Predictions
- `POST /api/ai/predict/buildings` - Detect buildings
- `POST /api/ai/predict/water-tanks` - Detect water tanks
- `POST /api/ai/segment/landuse` - Segment land use

Full API documentation available at `/docs` (Swagger UI)

## Data Format

### Village GeoJSON
```json
{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [...]
  },
  "properties": {
    "name": "Village Name",
    "state": "State",
    "district": "District",
    "population": 10000,
    "area_sqkm": 50
  }
}
```

### Infrastructure CSV
```csv
id,village_id,type,name,latitude,longitude,properties
1,1,school,Primary School,23.15,78.55,'{"classes": "1-5"}'
```

## Sample Data

Sample datasets included:
- `data/sample_villages.geojson` - 2 sample villages
- `data/sample_infrastructure.csv` - Infrastructure features

To use your own data:
1. Prepare village boundaries in GeoJSON or Shapefile format
2. Upload through the dashboard
3. Add infrastructure data via API
4. Run analyses

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/village_gis

# API
REACT_APP_API_URL=http://localhost:8000

# Earth Engine
EARTH_ENGINE_KEY=your_key_here

# AI Models
YOLOV11_WEIGHTS=yolov11n.pt
SAM_CHECKPOINT=sam_vit_b_01ec64.pth
```

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - see LICENSE file

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the development team

## Acknowledgments

- Smart India Hackathon for the challenge
- OpenStreetMap and OSGeo communities
- Ultralytics (YOLOv11)
- Meta AI (Segment Anything)
- Google Earth Engine

---

**Built with ❤️ for Smart India Hackathon**
