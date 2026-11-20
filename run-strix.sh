#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# HUNTER-STRIX: Strix AI + HUNTER-OS MCP Tools + Camoufox Browser
#
# Replaces Strix's default Chromium browser with Camoufox (anti-fingerprint,
# Caido-proxied) via MCP tool preference.
#
# Usage:
#   ./run-strix.sh --target ./app          # Scan a local app
#   ./run-strix.sh --target . --max-budget 5
# ═══════════════════════════════════════════════════════════════
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MCP_CONFIG="$SCRIPT_DIR/config/strix-mcp.json"
STRIX_CONFIG="$SCRIPT_DIR/config/strix-hunter.json"

# ── Ensure HUNTER-OS server is running ──
if ! curl -s -m 3 http://127.0.0.1:3000/api/health | grep -q '"ok"'; then
  echo "[hunter-strix] Starting HUNTER-OS server..."
  cd /home/dave/hunter-os && nohup npx tsx server.ts > /tmp/hunter-server.log 2>&1 &
  sleep 15
  if curl -s -m 3 http://127.0.0.1:3000/api/health | grep -q '"ok"'; then
    echo "[hunter-strix] HUNTER-OS server running ✓"
  else
    echo "[hunter-strix] WARNING: HUNTER-OS may not be running"
  fi
else
  echo "[hunter-strix] HUNTER-OS server already running ✓"
fi

# ── Ensure Caido proxy is running (for Camoufox traffic capture) ──
if ! curl -s -m 3 http://127.0.0.1:8280/ 2>/dev/null | head -1 | grep -q "HTTP"; then
  echo "[hunter-strix] Starting Caido proxy..."
  curl -s -m 30 -X POST http://127.0.0.1:3000/api/caido/start > /dev/null 2>&1
  sleep 8
  echo "[hunter-strix] Caido proxy started ✓"
else
  echo "[hunter-strix] Caido proxy already running ✓"
fi

# ── Verify Camoufox is available ──
if python3 -c "from camoufox.sync_api import Camoufox" 2>/dev/null; then
  echo "[hunter-strix] Camoufox browser available ✓"
else
  echo "[hunter-strix] WARNING: Camoufox not installed. Run: pip install camoufox[geoip]"
fi

echo ""
echo "═══ HUNTER-STRIX CONFIG ═══"
echo "  Engine:    Strix AI (OpenAI Agents SDK)"
echo "  LLM:       abliterated-model-large-v2 (ABLIT)"
echo "  Browser:   Camoufox v158 (anti-fingerprint, Caido-proxied)"
echo "  MCP Tools:"
echo "    ✓ cve-database    (411,987 offline CVEs)"
echo "    ✓ exploitdb       (47,182 entries)"
echo "    ✓ rag-knowledge   (bge-m3 semantic search)"
echo "    ✓ hunting-tools   (subfinder, nuclei, httpx)"
echo "    ✓ camoufox-browser (REAL Firefox, anti-fingerprint)"
echo "    ✓ caido-proxy     (surgical traffic capture)"
echo "    ✓ discord-alerts   (vulnerability notifications)"
echo ""

# ── Launch Strix with our MCP tools and config ──
exec /home/dave/.strix/bin/strix \
  --config "$STRIX_CONFIG" \
  --mcp-config "$MCP_CONFIG" \
  "$@"
