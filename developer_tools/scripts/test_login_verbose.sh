#!/bin/bash
echo "--- CREATE USER ---"
curl -v -X POST http://localhost:9999/usuarios \
  -H "Content-Type: application/json" \
  -d '{"login":"admin","senha":"123"}'

echo -e "\n\n--- LOGIN (HTTP) ---"
curl -v -X POST http://localhost:9999/login \
  -H "Content-Type: application/json" \
  -d '{"login":"admin","senha":"123"}'

echo -e "\n\n--- LOGIN (HTTPS via Traefik) ---"
curl -v -k -X POST https://137.131.179.58.nip.io/login \
  -H "Content-Type: application/json" \
  -d '{"login":"admin","senha":"123"}'
