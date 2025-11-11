#!/usr/bin/env python3
"""
Simple webhook server for testing the Instagram Reels Scraper app.
This server receives reel URLs and saves them to a file.

Usage:
    python webhook_server.py

Then expose it with ngrok:
    ngrok http 5000

Use the ngrok URL in the Rearn app.
"""

from flask import Flask, request, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)

# Create output directory if it doesn't exist
OUTPUT_DIR = 'received_reels'
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Receive reel URLs from the Rearn app."""
    try:
        # Get JSON data from request
        data = request.json
        
        # Extract information
        reel_url = data.get('reel_url', '')
        timestamp = data.get('timestamp', 0)
        
        # Convert timestamp to readable date
        date_str = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
        
        # Log to console
        print(f"\n{'='*60}")
        print(f"Received Reel URL at {date_str}")
        print(f"URL: {reel_url}")
        print(f"{'='*60}\n")
        
        # Save to file
        output_file = os.path.join(OUTPUT_DIR, 'reels.txt')
        with open(output_file, 'a') as f:
            f.write(f"{reel_url}\n")
        
        # Also save as JSON with metadata
        json_file = os.path.join(OUTPUT_DIR, 'reels.json')
        
        # Read existing data
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                try:
                    all_reels = json.load(f)
                except:
                    all_reels = []
        else:
            all_reels = []
        
        # Add new reel
        all_reels.append({
            'url': reel_url,
            'timestamp': timestamp,
            'received_at': date_str
        })
        
        # Save back to JSON
        with open(json_file, 'w') as f:
            json.dump(all_reels, f, indent=2)
        
        return jsonify({
            'status': 'success',
            'message': 'Reel URL received',
            'count': len(all_reels)
        }), 200
        
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/stats', methods=['GET'])
def stats():
    """Get statistics about received reels."""
    json_file = os.path.join(OUTPUT_DIR, 'reels.json')
    
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            try:
                all_reels = json.load(f)
                return jsonify({
                    'total_reels': len(all_reels),
                    'reels': all_reels
                }), 200
            except:
                return jsonify({'total_reels': 0, 'reels': []}), 200
    else:
        return jsonify({'total_reels': 0, 'reels': []}), 200

@app.route('/', methods=['GET'])
def index():
    """Simple info page."""
    return """
    <html>
        <head><title>Rearn Webhook Server</title></head>
        <body>
            <h1>Rearn Instagram Reels Scraper - Webhook Server</h1>
            <p>Server is running!</p>
            <p><strong>Webhook endpoint:</strong> POST /webhook</p>
            <p><strong>Stats endpoint:</strong> GET /stats</p>
            <hr>
            <h2>How to use:</h2>
            <ol>
                <li>If running locally, expose with ngrok: <code>ngrok http 5000</code></li>
                <li>Use the ngrok URL + /webhook in the Rearn app</li>
                <li>Example: <code>https://abc123.ngrok.io/webhook</code></li>
            </ol>
            <p><a href="/stats">View Stats</a></p>
        </body>
    </html>
    """

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Rearn Webhook Server Starting...")
    print("="*60)
    print(f"Output directory: {os.path.abspath(OUTPUT_DIR)}")
    print("Endpoints:")
    print("  POST /webhook - Receive reel URLs")
    print("  GET  /stats   - View statistics")
    print("  GET  /        - Info page")
    print("="*60 + "\n")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
