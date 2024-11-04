import os

from fastapi import FastAPI

from demo.dto.chat import ChatPayload
from demo.dto.mem import AddPayload
from mem0 import Memory

app = FastAPI()

config = {
    "version": "v1.1",
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "neo4j://localhost:7687",
            "username": "neo4j",
            "password": "xxx"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "test",
            "host": "localhost",
            "port": 6333,
            "embedding_model_dims": 1024,  # Change this according to your local model's dimensions
        },
    },
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": os.environ.get("OPENAI_API_KEY"),
            "openai_base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "model": "qwen-max",
            "temperature": 0.001,
            "top_p": 0.001,
            "max_tokens": 1500,
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": os.environ.get("OPENAI_API_KEY"),
            "openai_base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "model": "text-embedding-v3",
        },
    },
    # "llm": {
    #     "provider": "ollama",
    #     "config": {
    #         # "model": "llama3.2:latest",
    #         "model": "qwen2.5:14b",
    #         "temperature": 0.001,
    #         "top_p": 0.001,
    #         "max_tokens": 8000,
    #         "ollama_base_url": "http://localhost:11434",  # Ensure this URL is correct
    #     },
    # },
    # "embedder": {
    #     "provider": "ollama",
    #     "config": {
    #         "model": "mxbai-embed-large:latest",
    #         # Alternatively, you can use "snowflake-arctic-embed:latest"
    #         "ollama_base_url": "http://localhost:11434",
    #     },
    # },
}

# Initialize Memory with the configuration
m = Memory.from_config(config)


@app.put("/memory/add/list")
async def memory_add_list(payload: AddPayload):
    returned_memory = m.add(payload.messages, payload.user_id, payload.agent_id, payload.run_id, payload.metadata, payload.filters)
    return returned_memory


@app.get("/memory/{memory_id}")
async def memory_get(memory_id: int):
    return m.get(memory_id)


@app.post("/chat")
async def chat(payload: ChatPayload):
    return m.chat(payload.system_prompt, payload.query, payload.user_id, payload.run_id)

