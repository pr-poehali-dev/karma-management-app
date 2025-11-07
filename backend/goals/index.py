'''
Business: Goals management API - create, read, update goals for users
Args: event - dict with httpMethod, body (user_id, title, description, target_date)
      context - object with attributes: request_id, function_name
Returns: HTTP response with goals data or error
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
                'Access-Control-Allow-Methods': 'GET, POST, PUT, OPTIONS',
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
        user_id = body_data.get('user_id')
        title = body_data.get('title')
        description = body_data.get('description', '')
        target_date = body_data.get('target_date')
        
        if not user_id or not title:
            cursor.close()
            conn.close()
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({'error': 'user_id and title are required'})
            }
        
        cursor.execute(
            "INSERT INTO t_p72508054_karma_management_app.goals (user_id, title, description, target_date) VALUES (%s, %s, %s, %s) RETURNING goal_id, user_id, title, description, created_at, status, target_date",
            (user_id, title, description, target_date)
        )
        conn.commit()
        goal = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return {
            'statusCode': 201,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'isBase64Encoded': False,
            'body': json.dumps({
                'goal_id': goal['goal_id'],
                'user_id': goal['user_id'],
                'title': goal['title'],
                'description': goal['description'],
                'created_at': goal['created_at'].isoformat() if goal['created_at'] else None,
                'status': goal['status'],
                'target_date': goal['target_date'].isoformat() if goal['target_date'] else None
            })
        }
    
    elif method == 'GET':
        query_params = event.get('queryStringParameters', {}) or {}
        user_id = query_params.get('user_id')
        goal_id = query_params.get('goal_id')
        
        if goal_id:
            cursor.execute(
                "SELECT * FROM t_p72508054_karma_management_app.goals WHERE goal_id = %s",
                (goal_id,)
            )
            goal = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if not goal:
                return {
                    'statusCode': 404,
                    'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                    'isBase64Encoded': False,
                    'body': json.dumps({'error': 'Goal not found'})
                }
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({
                    'goal_id': goal['goal_id'],
                    'user_id': goal['user_id'],
                    'title': goal['title'],
                    'description': goal['description'],
                    'created_at': goal['created_at'].isoformat() if goal['created_at'] else None,
                    'status': goal['status'],
                    'target_date': goal['target_date'].isoformat() if goal['target_date'] else None
                })
            }
        elif user_id:
            cursor.execute(
                "SELECT * FROM t_p72508054_karma_management_app.goals WHERE user_id = %s ORDER BY created_at DESC",
                (user_id,)
            )
            goals = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({
                    'goals': [
                        {
                            'goal_id': g['goal_id'],
                            'user_id': g['user_id'],
                            'title': g['title'],
                            'description': g['description'],
                            'status': g['status'],
                            'target_date': g['target_date'].isoformat() if g['target_date'] else None
                        } for g in goals
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
                'body': json.dumps({'error': 'user_id or goal_id parameter required'})
            }
    
    elif method == 'PUT':
        body_data = json.loads(event.get('body', '{}'))
        goal_id = body_data.get('goal_id')
        status = body_data.get('status')
        
        if not goal_id or not status:
            cursor.close()
            conn.close()
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({'error': 'goal_id and status are required'})
            }
        
        cursor.execute(
            "UPDATE t_p72508054_karma_management_app.goals SET status = %s WHERE goal_id = %s RETURNING *",
            (status, goal_id)
        )
        conn.commit()
        goal = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not goal:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({'error': 'Goal not found'})
            }
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'isBase64Encoded': False,
            'body': json.dumps({
                'goal_id': goal['goal_id'],
                'status': goal['status']
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
