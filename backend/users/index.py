'''
Business: User registration and authentication API for KarmaFlow
Args: event - dict with httpMethod, body (email, username for POST)
      context - object with attributes: request_id, function_name
Returns: HTTP response with user data or error
'''

import json
import os
from typing import Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    method: str = event.get('httpMethod', 'GET')
    
    # Handle CORS OPTIONS request
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, X-User-Id',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'isBase64Encoded': False,
            'body': json.dumps({'error': 'Database connection not configured'})
        }
    
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    if method == 'POST':
        body_data = json.loads(event.get('body', '{}'))
        email = body_data.get('email')
        username = body_data.get('username')
        
        if not email or not username:
            cursor.close()
            conn.close()
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({'error': 'Email and username are required'})
            }
        
        cursor.execute(
            "INSERT INTO t_p72508054_karma_management_app.users (email, username) VALUES (%s, %s) RETURNING user_id, email, username, created_at, subscription_plan",
            (email, username)
        )
        conn.commit()
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return {
            'statusCode': 201,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'isBase64Encoded': False,
            'body': json.dumps({
                'user_id': user['user_id'],
                'email': user['email'],
                'username': user['username'],
                'created_at': user['created_at'].isoformat() if user['created_at'] else None,
                'subscription_plan': user['subscription_plan']
            })
        }
    
    elif method == 'GET':
        query_params = event.get('queryStringParameters', {}) or {}
        user_id = query_params.get('user_id')
        
        if user_id:
            cursor.execute(
                "SELECT user_id, email, username, created_at, last_login, subscription_plan FROM t_p72508054_karma_management_app.users WHERE user_id = %s",
                (user_id,)
            )
            user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if not user:
                return {
                    'statusCode': 404,
                    'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                    'isBase64Encoded': False,
                    'body': json.dumps({'error': 'User not found'})
                }
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({
                    'user_id': user['user_id'],
                    'email': user['email'],
                    'username': user['username'],
                    'created_at': user['created_at'].isoformat() if user['created_at'] else None,
                    'last_login': user['last_login'].isoformat() if user['last_login'] else None,
                    'subscription_plan': user['subscription_plan']
                })
            }
        else:
            cursor.execute("SELECT user_id, email, username, subscription_plan FROM t_p72508054_karma_management_app.users ORDER BY created_at DESC")
            users = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({
                    'users': [
                        {
                            'user_id': u['user_id'],
                            'email': u['email'],
                            'username': u['username'],
                            'subscription_plan': u['subscription_plan']
                        } for u in users
                    ]
                })
            }
    
    cursor.close()
    conn.close()
    
    return {
        'statusCode': 405,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'isBase64Encoded': False,
        'body': json.dumps({'error': 'Method not allowed'})
    }
