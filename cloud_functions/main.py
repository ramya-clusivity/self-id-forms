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
import asyncio
import functions_framework
from logger import logger
import time

# Custom imports
from logger import logger
from handler import Self_ID_FORMS

# Asynchronous helper for Flask
async def health(request):
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200

@functions_framework.http
def self_id_forms(request):
    """Handles the HTTP GET request and returns a JSON response."""
    path = request.path

    if request.method == 'GET':
        # Validate the GET method
        logger.info(f"path: {path}")

        if path.endswith('/overview/health'):
            logger.info(f"Health: {path}")
            return  asyncio.run(health(request))
        
        if path.endswith('/campaign/download_forms'):
            logger.info(f"GET: {path}")
            try:
                extractor = Self_ID_FORMS(request)
                csv_content = asyncio.run(extractor.fetch_data())

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
        
    if request.method == 'POST':
        return jsonify(error="Route not found"), 404
    
    logger.info(f"GET No route: {path}")
    return jsonify(error="Route not found"), 404



# Local testing setup
if __name__ == "__main__":
    app = Flask(__name__)

    @app.route('/campaign/download_forms', methods=['GET'])
    def test_route():
        with app.test_request_context(
            path=request.path, method=request.method, query_string=request.query_string
        ):
            return self_id_forms(request)

    app.run(debug=True, port=8080)