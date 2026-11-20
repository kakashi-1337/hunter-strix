# HUNTER-STRIX Integration

Strix AI (autonomous pentesting engine) + HUNTER-OS (security tooling) via MCP.

## Architecture
```
Strix AI Agent (OpenAI Agents SDK)
  ├── Built-in: Docker sandbox, multi-agent, budget management
  ├── Built-in: Caido proxy (HTTP capture/replay)
  └── MCP Tools from HUNTER-OS:
      ├── cve-database    → 411,987 offline CVEs
      ├── exploitdb       → 47,182 exploit entries
      ├── rag-knowledge   → bge-m3 semantic search
      ├── hunting-tools   → subfinder, nuclei, httpx, naabu
      ├── camoufox-browser → Anti-fingerprint Firefox
      ├── caido-proxy     → Captured traffic queries
      └── discord-alerts  → Vulnerability notifications
```

## Usage
```bash
# Quick start (auto-starts HUNTER-OS if needed)
./run-strix.sh --target ./your-app

# With options
./run-strix.sh --target ./your-app --max-budget 5.00
```

## Requirements
- Strix AI installed: ~/.strix/bin/strix
- HUNTER-OS running on :3000
- Python 3.10+ with mcp, httpx packages
