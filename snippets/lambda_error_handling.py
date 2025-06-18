"""
AWS Lambda Error Handling
Implements retry logic with fallback mechanism
"""
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class TransientError(Exception):
    """Indicates temporary failure that might resolve on retry"""
    pass

def lambda_handler(event, context):
    """Handles requests with resilient error processing"""
    try:
        # Simplified processing logic
        result = {"processed": True, "items": len(event.get('items', []))}
        return {'statusCode': 200, 'body': json.dumps(result)}
    
    except TransientError as e:
        logger.warning("Transient error, retrying: %s", str(e))
        raise  # Triggers Lambda automatic retry
        
    except Exception as e:
        logger.error("Processing failure: %s", str(e), exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Service unavailable'}),
            'headers': {'Retry-After': '300'}
        }