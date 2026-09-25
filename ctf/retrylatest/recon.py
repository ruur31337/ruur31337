#!/usr/bin/env python3
"""
retrylatest CTF recon script
Run locally: python3 recon.py
"""
import requests, json, sys
from urllib.parse import urljoin

BASE = 'https://retrylatest.pwndemanila.ph'
s = requests.Session()
s.verify = False

def r(method, path, **kw):
    resp = s.request(method, urljoin(BASE, path), timeout=15, **kw)
    print(f'\n{method} {path} → {resp.status_code}')
    print('  Headers:', dict(resp.headers))
    try:
        j = resp.json()
        print('  JSON:', json.dumps(j, indent=2)[:800])
    except Exception:
        print('  Body:', resp.text[:800])
    return resp

# ── Initial discovery ──────────────────────────────────────────────────────
print('=== Root ===')
r('GET', '/')

print('\n=== Common paths ===')
for path in [
    '/api', '/api/v1', '/api/v1/', '/swagger', '/openapi.json',
    '/docs', '/redoc', '/graphql', '/health', '/status',
    '/login', '/register', '/auth',
    '/export', '/exports', '/api/exports',
    '/receipt', '/receipts', '/api/receipts',
    '/recovery', '/api/recovery',
    '/retry', '/api/retry',
    '/compliance', '/api/compliance',
    '/control', '/dashboard',
    '/robots.txt', '/sitemap.xml',
    '/.well-known/openapi',
    '/js/app.js', '/js/main.js', '/static/js/main.js',
]:
    try:
        resp = s.get(urljoin(BASE, path), timeout=10)
        if resp.status_code not in (404,):
            print(f'  {resp.status_code}  {path}  {resp.text[:120]}')
    except Exception as e:
        print(f'  ERR  {path}  {e}')

print('\n=== Done ===')
