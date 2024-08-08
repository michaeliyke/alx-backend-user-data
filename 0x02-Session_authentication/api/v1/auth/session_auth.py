#!/usr/bin/env python3
"""
Session auth module for the api
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.basic_auth import Auth


class SessionAuth(Auth):
    """Session auth wrapper around the Auth class"""
