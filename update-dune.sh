#!/bin/bash

echo "📦 Pulling latest code from GitHub..."
git pull origin main

echo "🔄 Ensuring latest playlist is active..."
cp playlists.json ~/dune-weaver/playlists.json

echo "🚀 Restarting Dune Weaver..."
docker compose up -d

echo "✅ Dune Weaver updated and running!"
