#!/bin/bash
echo "start support_client.sh"
playwright install
~/.cargo/bin/uv pip install websocket-client

echo "waiting for 20 seconds..."
sleep 20
python3 /app/scripts/devika/support_client.py
