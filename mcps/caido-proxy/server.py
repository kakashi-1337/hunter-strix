#!/usr/bin/env python3
"""
HUNTER-OS Caido Proxy MCP Server
Query captured HTTP traffic from the Caido surgical proxy.

Tools exposed:
  - list_captured_requests: List requests captured by Caido proxy
"""

import httpx
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("hunter-caido")
HUNTER_OS = "http://127.0.0.1:3000"


@mcp.tool()
async def list_captured_requests(limit: int = 20) -> str:
    """List HTTP requests captured by the Caido surgical proxy.
    
    All agent browsing traffic is captured and can be analyzed or replayed.
    
    Args:
        limit: Max results (default 20)
    
    Returns:
        List of captured requests with status codes, methods, hosts, and paths
    """
    params = {"limit": limit}
    
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(f"{HUNTER_OS}/api/caido/requests", params=params)
        data = r.json()
    
    requests = data.get("requests", [])
    if not requests:
        return "No captured requests (Caido proxy may be offline)"
    
    results = []
    for req in requests[:limit]:
        status = req.get("statusCode", "?")
        method = req.get("method", "?")
        host = req.get("host", "?")
        path = req.get("path", "?")
        rt = req.get("roundtripMs", "?")
        results.append(f"[{status}] {method} {host}{path} ({rt}ms)")
    
    return f"Caido proxy captures ({len(requests)} total):\n" + "\n".join(results)


if __name__ == "__main__":
    mcp.run()
