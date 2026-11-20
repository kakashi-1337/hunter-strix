#!/usr/bin/env python3
"""
HUNTER-OS RAG Knowledge Base MCP Server
Semantic vector search using bge-m3 (1024d, 8192 token context).

Tools exposed:
  - rag_search: Semantic search across ingested security knowledge
"""

import httpx
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("hunter-rag")
HUNTER_OS = "http://127.0.0.1:3000"


@mcp.tool()
async def rag_search(query: str, limit: int = 5) -> str:
    """Search the HUNTER-OS RAG knowledge base using semantic vector search (bge-m3).
    
    Contains security notes, code snippets, CVE writeups, and ingested documents.
    Results include relevance scores and source citations (file:line).
    
    Args:
        query: Natural language query (e.g., "prototype pollution express RCE")
        limit: Max results (default 5)
    
    Returns:
        Matching knowledge chunks with cosine similarity scores
    """
    params = {"q": query, "k": min(limit, 20)}
    
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(f"{HUNTER_OS}/api/rag/search", params=params)
        data = r.json()
    
    hits = data.get("hits", [])
    if not hits:
        return f"No RAG matches for '{query}'"
    
    results = []
    for h in hits[:limit]:
        score = h.get("score", 0)
        source = h.get("sourceName", "?")
        lines = f"{h.get('lineStart', '?')}-{h.get('lineEnd', '?')}"
        text = h.get("text", "")[:200]
        signals = h.get("vulnerabilitySignals") or []
        signal_str = f" [signals: {', '.join(signals)}]" if signals else ""
        results.append(f"[{score:.2f}] {source}:{lines}{signal_str}\n  {text}")
    
    return f"RAG search results ({len(hits)} found):\n" + "\n\n".join(results)


if __name__ == "__main__":
    mcp.run()
