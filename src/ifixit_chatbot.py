"""
iFixit RAG Chatbot - Optimized for low memory systems
"""

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

import os
import requests
from typing import List, Dict
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter


class IFixitAPIClient:
    def __init__(self, api_key: str = None):
        self.base_url = "https://www.ifixit.com/api/2.0"
        self.headers = {}
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
    
    def search_devices(self, query: str) -> List[Dict]:
        try:
            response = requests.get(
                f"{self.base_url}/search/{query}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json().get('results', [])
        except Exception as e:
            print(f"Error searching: {e}")
            return []
    
    def get_guide_details(self, guide_id: int) -> Dict:
        try:
            response = requests.get(
                f"{self.base_url}/guides/{guide_id}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching guide: {e}")
            return {}


class IFixitRAGChatbot:
    def __init__(self, api_key: str = None, model_name: str = "tinyllama"):
        self.ifixit_client = IFixitAPIClient(api_key)
        
        # Optimized settings for low memory
        Settings.llm = Ollama(
            model=model_name,
            request_timeout=180.0,
            base_url="http://localhost:11434",
            temperature=0.7,
            context_window=2048  # Reduced context window
        )
        
        Settings.embed_model = HuggingFaceEmbedding(
            model_name="sentence-transformers/all-MiniLM-L6-v2"  # Smaller embedding model
        )
        
        Settings.node_parser = SentenceSplitter(
            chunk_size=256,  # Smaller chunks for less memory
            chunk_overlap=25
        )
        
        self.index = None
        self.query_engine = None
        print(f"✅ Chatbot initialized with {model_name}")
    
    def format_guide_to_document(self, guide: Dict) -> str:
        doc_text = f"Title: {guide.get('title', 'N/A')}\n"
        doc_text += f"Device: {guide.get('device', 'N/A')}\n"
        doc_text += f"Difficulty: {guide.get('difficulty', 'N/A')}\n\n"
        
        if 'introduction' in guide:
            doc_text += f"Introduction:\n{guide['introduction']}\n\n"
        
        if 'tools' in guide and guide['tools']:
            doc_text += "Tools Required:\n"
            for tool in guide['tools']:
                tool_name = tool.get('text') or tool.get('name', 'Unknown')
                doc_text += f"- {tool_name}\n"
            doc_text += "\n"
        
        if 'steps' in guide:
            doc_text += "Repair Steps:\n"
            for idx, step in enumerate(guide['steps'], 1):
                doc_text += f"\nStep {idx}: {step.get('title', 'Untitled')}\n"
                for line in step.get('lines', []):
                    doc_text += f"  {line.get('text', '')}\n"
        
        return doc_text
    
    def build_knowledge_base(self, device_query: str, max_guides: int = 3):
        print(f"\n🔍 Searching for: {device_query}")
        
        search_results = self.ifixit_client.search_devices(device_query)
        
        if not search_results:
            print("❌ No results found.")
            return
        
        documents = []
        
        for result in search_results[:max_guides]:  # Reduced to 3 for memory
            guide_id = result.get('guideid')
            
            if guide_id:
                print(f"  📥 Fetching guide {guide_id}...")
                guide = self.ifixit_client.get_guide_details(guide_id)
                
                if guide:
                    doc_text = self.format_guide_to_document(guide)
                    documents.append(Document(text=doc_text))
                    print(f"  ✅ {guide.get('title', 'Unknown')}")
        
        if not documents:
            documents = [Document(text="No guides found.")]
        
        print(f"\n🏗️  Building index from {len(documents)} documents...")
        self.index = VectorStoreIndex.from_documents(documents)
        self.query_engine = self.index.as_query_engine(
            similarity_top_k=2,  # Reduced for memory
            response_mode="compact"
        )
        print("✅ Ready!\n")
    
    def query(self, question: str) -> str:
        if not self.query_engine:
            return "⚠️  Build knowledge base first"
        
        response = self.query_engine.query(question)
        return str(response)
    
    def chat(self):
        if not self.query_engine:
            print("❌ Build knowledge base first!")
            return
        
        print("="*60)
        print("🔧 iFixit Repair Assistant - Type 'quit' to exit")
        print("="*60 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                print("💭 Thinking...")
                response = self.query(user_input)
                print(f"\n🤖 {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")


def main():
    print("\n🔧 iFixit RAG Chatbot (Low Memory Optimized)")
    print("="*60)
    
    chatbot = IFixitRAGChatbot(model_name="tinyllama")  # Using phi3 for low memory
    device = input("\n📱 Enter device (e.g., 'iPhone 13'): ").strip()
    
    if device:
        chatbot.build_knowledge_base(device, max_guides=3)  # Reduced guides
        if chatbot.query_engine:
            chatbot.chat()


if __name__ == "__main__":
    main()
