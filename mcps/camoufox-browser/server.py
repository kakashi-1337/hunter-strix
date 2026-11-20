#!/usr/bin/env python3
"""
HUNTER-OS Camoufox Browser MCP Server
Anti-fingerprinting browser for stealth web browsing and WAF bypass.

Tools exposed:
  - browse_url: Visit a URL with Camoufox (real Firefox, anti-fingerprint)
"""

import httpx
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("hunter-camoufox")
HUNTER_OS = "http://127.0.0.1:3000"


@mcp.tool()
async def browse_url(url: str) -> str:
    """Browse a URL with the Camoufox anti-fingerprinting browser.
    
    Uses a real Firefox engine with Canvas spoofing, WebGL noise, and
    randomized fingerprints. Bypasses most WAF bot detection.
    
    Args:
        url: URL to visit (e.g., https://target.com)
    
    Returns:
        Page title, DOM content, forms, links, and fingerprint info
    """
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{HUNTER_OS}/api/camoufox/browse", json={"url": url})
        data = r.json()
    
    if not data.get("ok"):
        return f"Browse failed: {data.get('error', 'unknown')}"
    
    title = data.get("title", "no title")
    dom_length = data.get("domLength", 0)
    forms = data.get("forms", [])
    links = data.get("links", [])
    fp = data.get("fingerprint", {})
    proxied = data.get("proxied", False)
    
    parts = [
        f"Title: {title}",
        f"DOM: {dom_length} chars",
        f"Forms: {len(forms)} | Links: {len(links)}",
        f"User-Agent: {fp.get('ua', '?')[:60]}",
        f"Platform: {fp.get('platform', '?')}",
        f"Webdriver detectable: {fp.get('webdriver', 'unknown')}",
        f"Proxied: {'Yes (Caido)' if proxied else 'No'}",
    ]
    
    if forms:
        form_details = []
        for f in forms[:5]:
            form_details.append(f"  action={f.get('action', '?')} method={f.get('method', '?')} inputs={len(f.get('inputs', []))}")
        parts.append("Forms detail:\n" + "\n".join(form_details))
    
    if links:
        parts.append("Top links:\n" + "\n".join(f"  {l}" for l in links[:10]))
    
    return "\n".join(parts)


if __name__ == "__main__":
    mcp.run()
