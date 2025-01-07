"""
This custom framework exposes many RESTful endpoints
to query the database and return data
"""

__author__  = "Ramyashree Rajgopal <ramya_shree@clusivity.io>"
__status__  = "dev"
__version__ = "0.0.1"
__date__    = "20 November 2024"
__all__     = "get"

from flask import Flask, request, jsonify
import functions_framework
from logger import logger
import asyncio
import time

# Custom imports
from handler import *


@functions_framework.http
def self_id_forms(request):
    """Handles the HTTP GET request and returns a JSON response."""
    path = request.path

    if request.method == 'GET':
        # Validate the GET method

        if path.endswith('/overview/health'):
            logger.info(f"Health: {path}")
            return health(request)
        
        if path.endswith('/campaign/download_forms'):
            logger.info(f"GET: {path}")

            # fetch company_id form_id from request and extract data from BigQuery
            company_id = request.args.get('company_id')
            form_id = request.args.get('form_id')
                     
            logger.info(f"company_id: {company_id}")
            logger.info(f"form_id: {form_id}")

            return 
        
    if request.method == 'POST':
        ...
    
    logger.info(f"GET No route: {path}")
    return jsonify(error="Route not found"), 404