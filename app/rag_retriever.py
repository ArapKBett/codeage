from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import json
import os
import aiohttp
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load local library data
with open("data/libraries.json", "r") as f:
    libraries = json.load(f)

# Initialize embeddings and vectorstore
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
texts = [lib["description"] for lib in libraries]
vectorstore = Chroma.from_texts(texts, embeddings, metadatas=libraries)

# Libraries.io API settings
LIBRARIES_IO_API_KEY = os.getenv("LIBRARIES_IO_API_KEY")
LIBRARIES_IO_API_URL = "https://libraries.io/api/search"

async def fetch_libraries_io(query: str) -> list:
    """
    Fetch library data from libraries.io API.
    """
    if not LIBRARIES_IO_API_KEY:
        logger.warning("Libraries.io API key not set. Using local data only.")
        return []

    async with aiohttp.ClientSession() as session:
        params = {"q": query, "api_key": LIBRARIES_IO_API_KEY}
        try:
            async with session.get(LIBRARIES_IO_API_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return [
                        {
                            "name": lib["name"],
                            "description": lib.get("description", ""),
                            "platform": lib.get("platform", "")
                        }
                        for lib in data[:5]  # Limit to top 5 results
                    ]
                else:
                    logger.error(f"Libraries.io API error: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching from libraries.io: {e}")
            return []

def retrieve_libraries(query: str) -> str:
    """
    Retrieve libraries from libraries.io API and local vectorstore.
    """
    # Run async API call
    loop = asyncio.get_event_loop()
    api_libraries = loop.run_until_complete(fetch_libraries_io(query))

    # Retrieve from local vectorstore
    local_results = vectorstore.similarity_search(query, k=2)

    # Combine results
    combined_libraries = api_libraries + [
        {"name": r.metadata["name"], "description": r.page_content, "platform": r.metadata["platform"]}
        for r in local_results
    ]

    # Deduplicate by name
    seen = set()
    unique_libraries = [
        lib for lib in combined_libraries
        if not (lib["name"] in seen or seen.add(lib["name"]))
    ]

    # Format output
    context = "\n".join([f"{lib['name']} ({lib['platform']}): {lib['description']}" for lib in unique_libraries[:3]])
    return context if context else "No relevant libraries found."
