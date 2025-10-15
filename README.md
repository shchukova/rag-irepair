# RAG iRepair

A Retrieval-Augmented Generation (RAG) application designed to provide intelligent assistance for repair-related queries using advanced AI technology.

## Overview

RAG iRepair combines the power of retrieval systems with large language models to deliver accurate, context-aware responses for repair documentation, troubleshooting guides, and technical support. The system retrieves relevant information from a knowledge base and uses it to generate helpful, precise answers to user queries.

## Features

- **Intelligent Query Processing**: Understands natural language questions about repairs and maintenance
- **Context-Aware Responses**: Leverages RAG architecture to provide accurate answers based on stored documentation
- **Semantic Search**: Finds relevant repair guides and documentation using vector embeddings
- **Real-time Information Retrieval**: Quickly accesses and synthesizes information from large knowledge bases
- **Scalable Architecture**: Built to handle growing documentation and user queries efficiently

## Architecture

The application follows a standard RAG pipeline:

1. **Document Ingestion**: Repair manuals, guides, and documentation are processed and stored
2. **Embedding Generation**: Text is converted to vector embeddings for semantic search
3. **Vector Storage**: Embeddings are stored in a vector database for efficient retrieval
4. **Query Processing**: User questions are embedded and matched against stored knowledge
5. **Response Generation**: Retrieved context is used to generate accurate, helpful responses

## Prerequisites

- Python 3.8+
- pip or conda for package management
- API keys for LLM provider (OpenAI, Anthropic, etc.)
- Vector database (Chroma, FAISS, Pinecone, or similar)

## Installation

```bash
# Clone the repository
git clone https://github.com/shchukova/rag-irepair.git
cd rag-irepair

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# LLM Provider Configuration
OPENAI_API_KEY=your_api_key_here
# or
ANTHROPIC_API_KEY=your_api_key_here

# Vector Database Configuration
VECTOR_DB_PATH=./data/vector_store
COLLECTION_NAME=repair_docs

# Application Settings
EMBEDDING_MODEL=text-embedding-ada-002
LLM_MODEL=gpt-4
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## Usage

### Basic Usage

```python
from rag_irepair import RepairAssistant

# Initialize the assistant
assistant = RepairAssistant()

# Ask a question
response = assistant.query("How do I replace the screen on an iPhone 12?")
print(response)
```

### Command Line Interface

```bash
# Start the interactive assistant
python main.py

# Query from command line
python main.py --query "What tools do I need for laptop repair?"
```

### Web Interface

```bash
# Start the web server
python app.py

# Access at http://localhost:5000
```

## Project Structure

```
rag-irepair/
├── data/
│   ├── documents/          # Raw repair documentation
│   └── vector_store/       # Vector database storage
├── src/
│   ├── __init__.py
│   ├── document_processor.py  # Document loading and chunking
│   ├── embeddings.py          # Embedding generation
│   ├── retriever.py           # Vector search and retrieval
│   ├── generator.py           # Response generation
│   └── assistant.py           # Main RAG pipeline
├── tests/
│   └── test_assistant.py
├── app.py                  # Web application
├── main.py                 # CLI interface
├── requirements.txt
├── .env.example
└── README.md
```

## Adding New Documentation

To add new repair guides to the knowledge base:

```python
from src.document_processor import DocumentProcessor

processor = DocumentProcessor()
processor.add_documents("path/to/repair/guides")
processor.build_index()
```

Supported document formats:
- PDF
- Markdown
- Plain text
- HTML
- DOCX

## API Reference

### RepairAssistant

```python
class RepairAssistant:
    def __init__(self, config: dict = None)
    def query(self, question: str, top_k: int = 5) -> str
    def add_documents(self, documents: list)
    def rebuild_index(self)
```

### DocumentProcessor

```python
class DocumentProcessor:
    def load_documents(self, path: str) -> list
    def chunk_documents(self, documents: list) -> list
    def build_index(self)
```

## Performance Optimization

- **Caching**: Frequently accessed documents are cached for faster retrieval
- **Batch Processing**: Documents can be processed in batches for efficiency
- **Async Operations**: Support for asynchronous query processing
- **Index Optimization**: Regular index maintenance for optimal search performance

## Testing

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/test_assistant.py

# Run with coverage
pytest --cov=src tests/
```

## Troubleshooting

### Common Issues

**Issue**: Slow query responses
- **Solution**: Check vector database size, consider increasing batch size or using GPU acceleration

**Issue**: Irrelevant responses
- **Solution**: Adjust chunk size, increase top_k retrieval, or refine document quality

**Issue**: Out of memory errors
- **Solution**: Reduce chunk size, use smaller embedding models, or implement streaming

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

- [ ] Multi-language support
- [ ] Image-based repair guide search
- [ ] Real-time chat interface
- [ ] Mobile application
- [ ] Integration with repair service platforms
- [ ] Advanced analytics and usage tracking

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain)
- Vector storage powered by [ChromaDB](https://github.com/chroma-core/chroma) or similar
- LLM capabilities from OpenAI/Anthropic
- Inspired by the RAG community and repair documentation standards

## Contact

For questions or support, please:
- Open an issue on GitHub
- Contact the maintainer: [shchukova](https://github.com/shchukova)

## Citation

If you use this project in your research or work, please cite:

```bibtex
@software{rag_irepair,
  author = {Shchukova},
  title = {RAG iRepair: AI-Powered Repair Assistant},
  year = {2025},
  url = {https://github.com/shchukova/rag-irepair}
}
```

---

**Note**: This is an active project. Features and documentation are subject to change. Please check the repository for the latest updates.
