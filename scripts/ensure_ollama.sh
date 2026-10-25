#!/usr/bin/env bash
# Starts a local Ollama only if nothing is already listening on its port.
# Compose can't detect a container another project started; this is the
# practical stand-in for that -- reuse what's running, don't duplicate it.
set -euo pipefail

if command -v podman &> /dev/null; then
  COMPOSE="podman compose"
elif command -v docker &> /dev/null; then
  COMPOSE="docker compose"
else
  echo "Neither podman nor docker found on PATH." >&2
  exit 1
fi

if curl -sf http://localhost:11434/api/tags > /dev/null 2>&1; then
  echo "Ollama is already running at localhost:11434 -- reusing it, starting nothing new."
else
  echo "No Ollama detected at localhost:11434 -- starting one via '$COMPOSE'."
  $COMPOSE up -d ollama ollama-init
fi
