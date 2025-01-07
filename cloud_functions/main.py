"""
This custom framework exposes many RESTful endpoints
to query the database and return data
"""

__author__  = "Ramyashree Rajgopal <ramya_shree@clusivity.io>"
__status__  = "dev"
__version__ = "0.0.1"
__date__    = "20 November 2024"
__all__     = "get"

from flask import Flask, request, jsonify,Response
import functions_framework
from logger import logger
import asyncio
import time

# Custom imports
from handler import *


@functions_framework.http
async def self_id_forms(request):
    """Handles the HTTP GET request and returns a JSON response."""
    path = request.path

    if request.method == 'GET':
        # Validate the GET method

        if path.endswith('/overview/health'):
            logger.info(f"Health: {path}")
            return health(request)
        
        if path.endswith('/campaign/download_forms'):
            logger.info(f"GET: {path}")
            try:
                extractor = Self_ID_FORMS(request)
                csv_content = await extractor.fetch_data()

                if not csv_content:
                    return {"message": "No data found or error occurred"}, 500

                # Return the CSV as a downloadable file
                return Response(
                    csv_content,
                    mimetype='text/csv',
                    headers={
                        "Content-Disposition": f"attachment;filename=data_{extractor.company_id}_{extractor.form_id}.csv"
                    }
                )
            
            except Exception as e:
                logger.error(f"Error in export_csv endpoint: {e}")
                return {"message": "Internal server error"}, 500


            return 
        
    if request.method == 'POST':
        return jsonify(error="Route not found"), 404
    
    logger.info(f"GET No route: {path}")
    return jsonify(error="Route not found"), 404