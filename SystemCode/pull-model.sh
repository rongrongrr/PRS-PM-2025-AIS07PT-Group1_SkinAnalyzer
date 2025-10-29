#!/bin/bash
set -e

# Start ollama in the background
ollama serve &
OLLAMA_PID=$!

# Wait for ollama to be ready
echo "Waiting for Ollama to start..."
sleep 5

# Pull the model if not already present
echo "Pulling qwen3:0.6b model..."
ollama pull qwen3:0.6b

echo "Model ready. Starting Ollama service..."

# Keep the process running
wait $OLLAMA_PID

