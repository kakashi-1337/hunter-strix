#!/usr/bin/env python3
"""
HUNTER-OS Hunting Tools MCP Server
Executes red-team tools: subfinder, nuclei, httpx, naabu, dnsx, etc.

Tools exposed:
  - run_subfinder: Enumerate subdomains
  - run_nuclei: Vulnerability scan
  - run_httpx: HTTP fingerprinting
  - run_port_scan: Port scanning
"""

import httpx
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("hunter-tools")
HUNTER_OS = "http://127.0.0.1:3000"


async def _run_tool(tool: str, args: list) -> str:
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(f"{HUNTER_OS}/api/tools/run", json={"tool": tool, "args": args})
        data = r.json()
    exit_code = data.get("exitCode", "?")
    stdout = (data.get("stdout") or "")[:2000]
    stderr = (data.get("stderr") or "")[:500]
    output = stdout or stderr or "(no output)"
    return f"[{tool}] exit {exit_code}:\n{output}"


@mcp.tool()
async def run_subfinder(domain: str) -> str:
    """Enumerate subdomains using subfinder (passive DNS).
    
    Args:
        domain: Target domain (e.g., sharetreats.ph)
    
    Returns:
        List of discovered subdomains
    """
    return await _run_tool("subfinder", ["-d", domain, "-all", "-silent"])


@mcp.tool()
async def run_nuclei(target: str, templates: str = "") -> str:
    """Run nuclei vulnerability scanner against a target.
    
    Args:
        target: URL or host to scan (e.g., https://target.com)
        templates: Template tags to filter (e.g., cve,exposure) (optional)
    
    Returns:
        Vulnerability findings from nuclei
    """
    args = ["-u", target, "-silent"]
    if templates:
        args.extend(["-tags", templates])
    return await _run_tool("nuclei", args)


@mcp.tool()
async def run_httpx(urls: str) -> str:
    """Fingerprint HTTP services using httpx (tech detection, status, titles).
    
    Args:
        urls: Comma-separated URLs or file path to scan
    
    Returns:
        HTTP response details for each target
    """
    return await _run_tool("pd-httpx", ["-u", urls, "-title", "-status-code", "-tech-detect", "-silent"])


@mcp.tool()
async def run_port_scan(target: str, ports: str = "1-1000") -> str:
    """Scan ports on a target using naabu (fast port scanner).
    
    Args:
        target: IP or hostname to scan
        ports: Port range (e.g., 1-1000, 80,443,8080)
    
    Returns:
        Open ports discovered
    """
    return await _run_tool("naabu", ["-host", target, "-p", ports, "-silent"])


@mcp.tool()
async def http_probe(url: str) -> str:
    """Quick HTTP status check for a single URL.
    
    Args:
        url: URL to probe (e.g., https://target.com)
    
    Returns:
        HTTP status, response time, content size, and server IP
    """
    return await _run_tool("http-probe", [url])


if __name__ == "__main__":
    mcp.run()
