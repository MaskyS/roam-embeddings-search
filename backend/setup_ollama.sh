#!/bin/bash

echo "Setting up Ollama with opengemma:latest model..."

# Wait for Ollama to be ready
echo "Waiting for Ollama service to start..."
sleep 5

# Pull the embeddinggemma model
echo "Pulling embeddinggemma:latest model..."
docker exec roam-test-ollama-1 ollama pull embeddinggemma:latest

echo "Ollama setup complete!"
