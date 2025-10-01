#!/bin/bash
# Quick fix script for Render deployment
# Run this in the Render shell to fix corrupted date issues

echo "🔧 Running quick fix for corrupted dates..."

# Run the fix script
python fix_corrupted_dates.py

echo "✅ Fix complete. Restarting application..."

# If running as a one-off command, the service will restart automatically
# If running in shell, you may need to trigger a restart manually