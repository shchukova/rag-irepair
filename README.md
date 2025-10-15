# iFixit RAG Chatbot

A production-ready RAG (Retrieval-Augmented Generation) chatbot system that provides intelligent repair guidance using iFixit's comprehensive repair database.

## Overview

This intelligent chatbot combines the power of modern AI with iFixit's extensive repair knowledge base to provide accurate, context-aware repair assistance. Built with:

- **Llama 2** - Advanced language model for natural conversation
- **LlamaIndex** - RAG orchestration and vector store management
- **iFixit API** - Access to thousands of repair guides
- **FastAPI** - High-performance REST API
- **Ollama** - Local LLM deployment
- **Docker** - Containerized deployment

## Features

- Real-time repair guidance with access to iFixit's repair database
- Conversational AI with context memory
- Multi-device support
- Session management and conversation history
- REST API for easy integration
- Source attribution for transparency
- Docker-ready containerized deployment
- Scalable production-grade architecture

## Architecture

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│   FastAPI Server    │
│   (Port 8000)       │
└──────┬──────────────┘
       │
       ├─────────────────┐
       ▼                 ▼
┌─────────────┐   ┌──────────────┐
│  Ollama     │   │  iFixit API  │
│  (Llama 2)  │   │              │
└─────────────┘   └──────────────┘
       │
       ▼
┌─────────────────┐
│  LlamaIndex RAG │
│  Vector Store   │
└─────────────────┘
```

## Installation

### Prerequisites

- Python 3.9+
- Docker and Docker Compose (optional, for containerized deployment)
- 8GB+ RAM recommended
- GPU recommended (NVIDIA with CUDA support for optimal performance)

### Option 1: Local Installation

```bash
# 1. Clone the repository
git clone https://github.com/shchukova/rag-irepair.git
cd rag-irepair

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 5. Pull Llama 2 model
ollama pull llama2

# 6. (Optional) Set your iFixit API key
export IFIXIT_API_KEY="your_key_here"
```

### Option 2: Docker Installation (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/shchukova/rag-irepair.git
cd rag-irepair

# 2. Create .env file with your API key
echo "IFIXIT_API_KEY=your_key_here" > .env

# 3. Build and run with Docker Compose
docker-compose up -d

# 4. Check logs
docker-compose logs -f chatbot_api
```

## Quick Start

### Using Python Script

```python
from ifixit_chatbot import IFixitRAGChatbot

# Initialize chatbot
chatbot = IFixitRAGChatbot(model_name="llama2")

# Build knowledge base for a specific device
chatbot.build_knowledge_base("iPhone 13", max_guides=10)

# Ask a question
response = chatbot.query("How do I replace the screen?")
print(response)

# Start interactive chat session
chatbot.chat()
```

### Using REST API

**1. Start the API server:**
```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

**2. Initialize chatbot for a device:**
```bash
curl -X POST "http://localhost:8000/initialize" \
  -H "Content-Type: application/json" \
  -d '{
    "device_name": "iPhone 13",
    "max_guides": 10
  }'
```

**3. Query the chatbot:**
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I replace the battery?"
  }'
```

**4. Start a conversational session:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What tools do I need?",
    "session_id": "user_123"
  }'
```

## API Documentation

### Health Check

Check API status:
```http
GET /health
GET /healthz  # Kubernetes/Docker health check
```

### Initialization

Initialize chatbot with device-specific knowledge:
```http
POST /initialize

Request Body:
{
  "device_name": "iPhone 13",
  "max_guides": 10,
  "model_name": "llama2"  // optional
}
```

### Query (Stateless)

Ask a single question without maintaining context:
```http
POST /query

Request Body:
{
  "question": "How do I replace the screen?",
  "session_id": "optional"
}
```

### Chat (Stateful)

Engage in conversation with context memory:
```http
POST /chat

Request Body:
{
  "message": "What tools do I need?",
  "session_id": "user_123"
}
```

### Session Management

Get conversation history:
```http
GET /sessions/{session_id}
```

Delete session:
```http
DELETE /sessions/{session_id}
```

### Reset

Reset chatbot state:
```http
POST /reset
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# iFixit API Configuration
IFIXIT_API_KEY=your_api_key_here

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_HOST=0.0.0.0:11434

# Application Settings
PYTHONUNBUFFERED=1
```

### Model Configuration

Choose the right model based on your needs:

```python
# Faster inference, lower accuracy (7B parameters)
chatbot = IFixitRAGChatbot(model_name="llama2:7b")

# Balanced performance (13B parameters) - Default
chatbot = IFixitRAGChatbot(model_name="llama2:13b")

# Best accuracy, slower inference (70B parameters)
chatbot = IFixitRAGChatbot(model_name="llama2:70b")
```

### RAG Parameters

Customize retrieval and chunking behavior:

```python
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter

# Configure document chunking
Settings.node_parser = SentenceSplitter(
    chunk_size=512,      # Size of each text chunk
    chunk_overlap=50     # Overlap between consecutive chunks
)

# Configure query engine
query_engine = index.as_query_engine(
    similarity_top_k=5,              # Number of relevant chunks to retrieve
    response_mode="tree_summarize"   # How to synthesize response
)
```

## Docker Deployment

### Single Container

```bash
# Build the Docker image
docker build -t ifixit-chatbot .

# Run the container
docker run -d \
  --name ifixit-chatbot \
  -p 8000:8000 \
  -e IFIXIT_API_KEY=your_key \
  ifixit-chatbot
```

### Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart specific service
docker-compose restart chatbot_api
```

## Cloud Deployment

### AWS EC2

```bash
# 1. Launch EC2 instance (t3.large or better recommended)

# 2. SSH into your instance
ssh -i your-key.pem ubuntu@your-instance-ip

# 3. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 4. Clone repository and deploy
git clone https://github.com/shchukova/rag-irepair.git
cd rag-irepair
docker-compose up -d
```

### Google Cloud Run

```bash
# 1. Build and push image to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/ifixit-chatbot

# 2. Deploy to Cloud Run
gcloud run deploy ifixit-chatbot \
  --image gcr.io/PROJECT_ID/ifixit-chatbot \
  --platform managed \
  --region us-central1 \
  --memory 8Gi \
  --cpu 4 \
  --set-env-vars IFIXIT_API_KEY=your_key
```

### Azure Container Instances

```bash
# 1. Create resource group
az group create --name ifixit-rg --location eastus

# 2. Deploy container
az container create \
  --resource-group ifixit-rg \
  --name ifixit-chatbot \
  --image your-registry/ifixit-chatbot \
  --cpu 4 --memory 8 \
  --ports 8000 \
  --environment-variables IFIXIT_API_KEY=your_key
```

## Testing

```bash
# Run unit tests
python -m pytest tests/

# Run integration tests
python test_chatbot.py

# Run performance tests
python -m pytest tests/test_performance.py

# Test all API endpoints
python testing_suite.py
```

## Performance Optimization

### 1. Model Selection

Balance speed vs accuracy based on your use case:

| Model | Parameters | Speed | Accuracy | Use Case |
|-------|-----------|-------|----------|----------|
| llama2:7b | 7B | Fast | Good | High-traffic applications |
| llama2:13b | 13B | Medium | Better | Balanced production use |
| llama2:70b | 70B | Slow | Best | Maximum accuracy needed |

### 2. Chunk Size Optimization

```python
# Smaller chunks = faster retrieval, less context
Settings.node_parser = SentenceSplitter(chunk_size=256)

# Larger chunks = more context, slower retrieval
Settings.node_parser = SentenceSplitter(chunk_size=1024)

# Recommended balanced setting
Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
```

### 3. Response Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(question: str):
    return chatbot.query(question)
```

### 4. GPU Acceleration

```bash
# Enable GPU support in Docker Compose
docker-compose --profile gpu up -d

# Verify GPU is being used
docker exec chatbot_api nvidia-smi
```

## Security Best Practices

### 1. API Key Management
- Store API keys in environment variables or secret managers
- Never commit keys to version control
- Use `.env` files (listed in `.gitignore`)

### 2. Rate Limiting
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/query")
@limiter.limit("10/minute")
async def query_endpoint():
    pass
```

### 3. Input Validation
- Sanitize all user inputs
- Implement request size limits
- Validate data types and formats

### 4. HTTPS
- Always use SSL/TLS in production
- Configure reverse proxy (nginx, Caddy)
- Use Let's Encrypt for free certificates

### 5. CORS Configuration
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

## Monitoring and Logging

### Logging Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Metrics Collection

```python
from prometheus_client import Counter, Histogram

# Track query counts
query_counter = Counter('chatbot_queries_total', 'Total number of queries')

# Track response times
response_time = Histogram('chatbot_response_seconds', 'Response time in seconds')

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    query_counter.inc()
    with response_time.time():
        response = chatbot.query(request.question)
    return response
```

## Troubleshooting

### Ollama Not Responding

```bash
# Check Ollama status
ollama list

# Check if service is running
ps aux | grep ollama

# Restart Ollama
pkill ollama
ollama serve

# Pull model again if needed
ollama pull llama2
```

### Out of Memory Errors

```bash
# Switch to smaller model
ollama pull llama2:7b

# Reduce chunk size
# In your code:
Settings.node_parser = SentenceSplitter(chunk_size=256)

# Reduce number of retrieved chunks
query_engine = index.as_query_engine(similarity_top_k=3)
```

### Slow Response Times

```bash
# Enable GPU acceleration
export OLLAMA_GPU=1

# Use smaller model
chatbot = IFixitRAGChatbot(model_name="llama2:7b")

# Reduce retrieval size
query_engine = index.as_query_engine(similarity_top_k=3)

# Enable response caching (see Performance Optimization section)
```

### Connection Errors

```bash
# Check if API server is running
curl http://localhost:8000/health

# Check Docker containers
docker-compose ps

# View container logs
docker-compose logs chatbot_api

# Restart services
docker-compose restart
```

## Project Structure

```
rag-irepair/
├── api_server.py              # FastAPI server implementation
├── ifixit_chatbot.py          # Core chatbot logic
├── test_chatbot.py            # Integration tests
├── testing_suite.py           # API endpoint tests
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker image configuration
├── docker-compose.yml         # Multi-container setup
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── README.md                 # This file
├── tests/
│   ├── test_unit.py          # Unit tests
│   └── test_performance.py   # Performance tests
└── docs/
    └── API.md                # Detailed API documentation
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

