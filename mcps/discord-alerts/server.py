#!/usr/bin/env python3
"""
HUNTER-OS Discord Alerts MCP Server
Send vulnerability alerts to the operator's Discord channel.

Tools exposed:
  - send_alert: Send a critical/high vulnerability alert to Discord
"""

import httpx
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("hunter-discord")
HUNTER_OS = "http://127.0.0.1:3000"


@mcp.tool()
async def send_alert(cve_id: str, title: str, severity: str, detail: str = "") -> str:
    """Send a vulnerability alert to the operator's Discord channel.
    
    Use this when a CRITICAL or HIGH severity vulnerability is confirmed.
    
    Args:
        cve_id: CVE identifier (e.g., CVE-2024-6387)
        title: Brief alert title
        severity: CRITICAL, HIGH, MEDIUM, or LOW
        detail: Technical details for the alert (optional)
    
    Returns:
        Confirmation of Discord dispatch
    """
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{HUNTER_OS}/api/notifications/discord", json={
            "cveId": cve_id,
            "title": title,
            "severity": severity.upper(),
            "description": detail,
        })
        data = r.json()
    
    if data.get("success"):
        return f"Discord alert sent: [{severity}] {cve_id} — {title}"
    return f"Discord alert failed: {data.get('message', 'unknown error')}"


if __name__ == "__main__":
    mcp.run()
