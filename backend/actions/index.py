'''
Business: Daily actions tracking API - log actions, earn karma points, track progress
Args: event - dict with httpMethod, body (seed_id, user_id, action_type, description)
      context - object with attributes: request_id, function_name
Returns: HTTP response with actions data or error
'''

import json
import os
from typing import Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    method: str = event.get('httpMethod', 'GET')
    
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
        seed_id = body_data.get('seed_id')
        user_id = body_data.get('user_id')
        action_type = body_data.get('action_type')
        action_description = body_data.get('action_description', '')
        karma_points = body_data.get('karma_points', 1)
        
        if not seed_id or not user_id or not action_type:
            cursor.close()
            conn.close()
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({'error': 'seed_id, user_id and action_type are required'})
            }
        
        cursor.execute(
            "INSERT INTO t_p72508054_karma_management_app.daily_actions (seed_id, user_id, action_type, action_description, karma_points) VALUES (%s, %s, %s, %s, %s) RETURNING *",
            (seed_id, user_id, action_type, action_description, karma_points)
        )
        conn.commit()
        action = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return {
            'statusCode': 201,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'isBase64Encoded': False,
            'body': json.dumps({
                'action_id': action['action_id'],
                'seed_id': action['seed_id'],
                'user_id': action['user_id'],
                'action_type': action['action_type'],
                'action_description': action['action_description'],
                'karma_points': action['karma_points'],
                'created_at': action['created_at'].isoformat() if action['created_at'] else None
            })
        }
    
    elif method == 'GET':
        query_params = event.get('queryStringParameters', {}) or {}
        user_id = query_params.get('user_id')
        seed_id = query_params.get('seed_id')
        
        if seed_id:
            cursor.execute(
                "SELECT * FROM t_p72508054_karma_management_app.daily_actions WHERE seed_id = %s ORDER BY created_at DESC",
                (seed_id,)
            )
            actions = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({
                    'actions': [
                        {
                            'action_id': a['action_id'],
                            'seed_id': a['seed_id'],
                            'action_type': a['action_type'],
                            'action_description': a['action_description'],
                            'karma_points': a['karma_points'],
                            'created_at': a['created_at'].isoformat() if a['created_at'] else None
                        } for a in actions
                    ]
                })
            }
        elif user_id:
            cursor.execute(
                "SELECT * FROM t_p72508054_karma_management_app.daily_actions WHERE user_id = %s ORDER BY created_at DESC LIMIT 50",
                (user_id,)
            )
            actions = cursor.fetchall()
            
            cursor.execute(
                "SELECT SUM(karma_points) as total_karma FROM t_p72508054_karma_management_app.daily_actions WHERE user_id = %s",
                (user_id,)
            )
            karma_result = cursor.fetchone()
            total_karma = karma_result['total_karma'] if karma_result and karma_result['total_karma'] else 0
            
            cursor.close()
            conn.close()
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({
                    'total_karma': total_karma,
                    'actions': [
                        {
                            'action_id': a['action_id'],
                            'seed_id': a['seed_id'],
                            'action_type': a['action_type'],
                            'action_description': a['action_description'],
                            'karma_points': a['karma_points'],
                            'created_at': a['created_at'].isoformat() if a['created_at'] else None
                        } for a in actions
                    ]
                })
            }
        else:
            cursor.close()
            conn.close()
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({'error': 'user_id or seed_id parameter required'})
            }
    
    cursor.close()
    conn.close()
    
    return {
        'statusCode': 405,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'isBase64Encoded': False,
        'body': json.dumps({'error': 'Method not allowed'})
    }
