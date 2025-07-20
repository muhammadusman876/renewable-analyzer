# 🌞 Renewable Energy Investment Analyzer

An **AI-powered web application** that helps German households and small businesses assess solar panel investment feasibility using historical renewable energy data, weather APIs, and **LLM-generated reports with RAG system**.

## 🎯 Project Overview

This application combines:

- **Historical Data**: Real German renewable energy dataset (2006-2017)
- **AI Consultation**: LLM-powered personalized solar reports
- **RAG System**: FAISS vector database with German energy policies
- **Weather Integration**: Real-time DWD weather service
- **Financial Modeling**: ROI calculations with current German market rates
- **Student Training**: Multiple AI training options from laptop to HPC clusters
- **Modern Tech Stack**: FastAPI backend + ReactJS frontend + Ollama LLM

## 🧠 AI Features

### ✅ LLM Integration

- **Local AI**: Ollama with Llama3 model
- **Smart Reports**: AI-generated vs template-based consultation
- **German Market Focus**: Trained on local regulations and pricing

### ✅ RAG System

- **Vector Database**: FAISS with German energy policy documents
- **Semantic Search**: Find relevant regulations for each query
- **Context-Aware**: Enhanced recommendations with policy backing

### ✅ Training Options

- **Student-Friendly**: 5-30 minute training on any laptop
- **Cloud Options**: Google Colab integration
- **University HPC**: SLURM cluster deployment (TU Chemnitz specific)

## 🏗️ Architecture

```
Frontend (ReactJS) ↔ Backend (FastAPI) ↔ Ollama LLM + FAISS RAG
                            ↓
                EDA Dataset + Weather APIs + Policy Documents
                            ↓
                Training Pipeline (Local/Cloud/HPC)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- Git
- Ollama (for AI features)

### Backend Setup

1. **Clone and navigate to project**:

```bash
cd renewable-analyzer/server
```

2. **Create virtual environment**:

```bash
conda create -n renewable python=3.11
conda activate renewable
# OR: python -m venv venv && source venv/bin/activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:

```bash
cp .env.example .env
# Edit .env file with your configuration
```

5. **Run the backend**:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### AI Features Setup

```bash
# Install Ollama for local LLM
# Visit: https://ollama.ai/download

# Start Ollama
ollama serve

# Pull the model
ollama pull llama3

# Install AI dependencies
pip install faiss-cpu sentence-transformers
```

### AI Training (Optional)

#### For Students (Laptop/Colab)

```bash
cd server/training/

# One-click setup
quick_start.bat  # Windows

# Manual setup
pip install -r requirements.txt
python simple_train.py --num_samples 50 --epochs 3 --test_after_training

# See server/training/SIMPLE_STUDENT_GUIDE.md for Google Colab and other options
```

#### For University Students (HPC)

```bash
# TU Chemnitz specific setup
cd server/training/
# Follow CLUSTER_SETUP_GUIDE.md for complete university cluster deployment
```

### Frontend Setup (Coming Soon)

```bash
cd frontend
npm install
npm start
```

## 📊 Features

### ✅ Current Implementation

- **Solar Calculations**: Real German EDA dataset integration (2006-2017)
- **AI-Powered Reports**: Ollama LLM with personalized consultation
- **RAG System**: FAISS vector database with German energy policies
- **Weather Integration**: DWD weather service with historical data
- **Financial Analysis**: ROI calculations with current German market rates
- **RESTful API**: FastAPI with comprehensive endpoints
- **Training Pipeline**: Student-friendly to university HPC cluster options

### ✅ AI Training Options

- **TensorFlow Training**: Simple 5-30 minute sessions on any laptop
- **Cloud Training**: Google Colab integration with free GPU
- **University HPC**: SLURM cluster deployment (advanced)
- **One-Click Setup**: Automated environment setup and training

### 🔄 Frontend Development

- ReactJS user interface (in progress)
- Interactive solar calculation forms
- Chart visualizations for ROI analysis
- PDF report generation

## 🔧 API Endpoints

### Main Analysis Endpoint

```http
POST /api/analyze
Content-Type: application/json

{
  "location": "Hamburg, Germany",
  "roof_area": 50,
  "orientation": "south",
  "budget": 15000
}
```

### Weather Data

```http
GET /api/weather/{location}
```

### Supported Locations

```http
GET /api/locations
```

## 📈 Example Analysis

**Input:**

- Location: Hamburg, Germany
- Roof Area: 50 m²
- Orientation: South
- Budget: €15,000

**Output:**

- Annual Production: ~4,250 kWh
- Total Investment: ~€12,500
- Annual Savings: ~€1,190
- Payback Period: ~10.5 years
- CO2 Reduction: ~1.7 tons/year

## 🧪 Testing

```bash
# Run basic API test
curl http://localhost:8000/health

# Test analysis endpoint
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Berlin",
    "roof_area": 40,
    "orientation": "south",
    "budget": 12000
  }'
```

## 📁 Project Structure

```
renewable-analyzer/
├── app/
│   ├── api/
│   │   ├── models.py           # Pydantic models
│   │   └── routes.py           # API endpoints
│   ├── core/
│   │   ├── solar_calculator.py # Solar potential calculations
│   │   ├── roi_calculator.py   # Financial analysis
│   │   └── weather_service.py  # Weather data integration
│   ├── rag/
│   │   └── llm_service.py      # LLM and RAG functionality
│   ├── data/
│   │   ├── processed_eda_data/ # Your EDA dataset
│   │   ├── policy_documents/   # German energy policies
│   │   └── vector_db/          # Vector database files
│   └── main.py                 # FastAPI application
├── frontend/                   # ReactJS frontend (coming soon)
├── docs/                       # Documentation
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## 💡 Key Calculations

### Solar Potential

- Uses historical sunshine duration from EDA dataset
- Applies efficiency factors for roof orientation
- Accounts for system losses and panel degradation
- Provides monthly production breakdown

### Financial Analysis

- German electricity prices (€0.32/kWh)
- Feed-in tariffs (€0.082/kWh)
- Installation costs (€1,400/kW)
- KfW financing options
- 25-year lifecycle analysis

### Environmental Impact

- CO2 reduction calculations
- Grid electricity carbon factor (0.401 kg CO2/kWh)
- Equivalent tree planting calculations

## 🔌 Integration with EDA Dataset

This project directly leverages your Germany Renewable Energy EDA analysis:

1. **Historical Weather Data**: Uses sunshine duration and temperature data
2. **Seasonal Patterns**: Applies learned seasonal variations
3. **Regional Factors**: Incorporates location-specific adjustments
4. **Validation**: Cross-references with historical renewable production

## 🎨 Frontend Preview (Coming Soon)

The ReactJS frontend will feature:

- Clean, responsive design with Tailwind CSS
- Interactive input forms
- Real-time calculations
- Downloadable PDF reports
- Mobile-friendly interface

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build individual container
docker build -t renewable-analyzer .
docker run -p 8000:8000 renewable-analyzer
```

## 🔮 Future Enhancements

### Phase 2: AI Integration

- [ ] OpenAI/Llama LLM integration
- [ ] FAISS vector database for policy documents
- [ ] RAG-powered report generation
- [ ] Multi-language support (German/English)

### Phase 3: Advanced Features

- [ ] Battery storage optimization
- [ ] Smart home integration recommendations
- [ ] Financing calculator with loan options
- [ ] Installer network integration

### Phase 4: Scale & Deploy

- [ ] Multi-country support
- [ ] Commercial building analysis
- [ ] Real-time monitoring integration
- [ ] Mobile app development

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

For questions or support:

- Create an issue on GitHub
- Check the [documentation](docs/)
- Review the [API documentation](http://localhost:8000/docs) when running

## 🎯 Portfolio Impact

This project demonstrates:

- **Full-Stack Development**: Backend + Frontend + AI
- **Data Science Application**: Real-world use of EDA insights
- **Modern Tech Stack**: FastAPI, ReactJS, LangChain, Docker
- **Business Value**: Practical tool for renewable energy decisions
- **Technical Depth**: Complex calculations, API integration, AI features

Perfect for showcasing to employers in:

- Renewable energy companies
- Tech startups
- Data science roles
- Full-stack development positions
- AI/ML engineering roles

---

**Built with ❤️ using Python, FastAPI, and renewable energy data**
