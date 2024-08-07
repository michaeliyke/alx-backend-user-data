#!/usr/bin/env python3
""" Main 1
"""
from api.v1.auth.auth import Auth

a = Auth()

# print(a.require_auth(None, None))
# print(a.require_auth(None, []))
# print(a.require_auth("/api/v1/status/", []))
# print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
# print(a.require_auth("/api/v1/status", ["/api/v1/status/"]))
# print(a.require_auth("/api/v1/users", ["/api/v1/status/"]))
# print(a.require_auth("/api/v1/users", ["/api/v1/status/", "/api/v1/stats"]))

excluded_paths = ['/api/v1/stat*']
yes = [
    '/api/v1/status',
    '/api/v1/stats/',
    '/api/v1/statistics',
    '/api/v1/stat123',
    '/api/v1/stat_data/',
]
print('--REQUIRES AUTH == False--')
for path in yes:
    print(a.require_auth(path, excluded_paths))

no = [
    '/api/v1/stale',
    '/api/v1/user_stats',
    '/api/v1/users',
    '/api/v1/statistics/reports',
    '/api/v1/statistical/analysis',
]

print('--REQUIRES AUTH == True--')
for path in no:
    print(a.require_auth(path, excluded_paths))

excluded_paths = ['/api/v1/user*']
yes = [
    '/api/v1/user',
    '/api/v1/users',
    '/api/v1/user_profile',
    '/api/v1/user123',
    '/api/v1/user.login',
    '/api/v1/user?register=true',
]

print('--REQUIRES AUTH == False--')
for path in yes:
    print(a.require_auth(path, excluded_paths))

no = [
    '/api/v1/admin',
    '/api/v1/settings',
    '/api/v1/userdata/123',
    '/api/v1/user?p=/roles',
]

print('--REQUIRES AUTH == True--')
for path in no:
    print(a.require_auth(path, excluded_paths))
