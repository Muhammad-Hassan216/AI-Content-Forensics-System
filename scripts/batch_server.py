"""Lightweight HTTP server for batch predictions using built-in libraries.
POST JSON {"texts": ["...", ...], "threshold": 0.5, "ml_weight": 0.7}
-> returns JSON with per-text results and the effective settings.
Run: python scripts/batch_server.py
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import os

# ensure project root on path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.feature_extractor import extract_features
from src.detector import detect

HOST = '0.0.0.0'
PORT = 8000

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, data):
        body = json.dumps(data).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != '/predict':
            self._send(404, {'error': 'not found'})
            return
        length = int(self.headers.get('Content-Length', '0'))
        body = self.rfile.read(length).decode('utf-8')
        try:
            data = json.loads(body)
            texts = data.get('texts') or []
            threshold = float(data.get('threshold', 0.5))
            ml_weight = float(data.get('ml_weight', 0.5))
        except Exception:
            self._send(400, {'error': 'invalid json'})
            return

        results = []
        for t in texts:
            f = extract_features(t)
            d = detect(f, text=t, threshold=threshold, ml_weight=ml_weight)
            results.append({'label': d.get('label'), 'ensemble': d.get('score'), 'ml_prob': d.get('ml_prob'), 'heuristic_prob': d.get('heuristic_prob')})

        self._send(200, {'results': results, 'threshold': threshold, 'ml_weight': ml_weight, 'count': len(results)})

def run():
    print(f'Starting server on http://{HOST}:{PORT} ...')
    server = HTTPServer((HOST, PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Stopping...')
        server.server_close()

if __name__ == '__main__':
    run()
