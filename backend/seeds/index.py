'''
Business: Seeds management API - plant seeds, water them, track growth and sprouts
Args: event - dict with httpMethod, body (goal_id, user_id, seed_name, water action)
      context - object with attributes: request_id, function_name
Returns: HTTP response with seeds data or error
'''

import json
import os
from typing import Dict, Any
from datetime import datetime
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
        goal_id = body_data.get('goal_id')
        user_id = body_data.get('user_id')
        seed_name = body_data.get('seed_name')
        
        if not goal_id or not user_id or not seed_name:
            cursor.close()
            conn.close()
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({'error': 'goal_id, user_id and seed_name are required'})
            }
        
        cursor.execute(
            "INSERT INTO t_p72508054_karma_management_app.seeds (goal_id, user_id, seed_name) VALUES (%s, %s, %s) RETURNING *",
            (goal_id, user_id, seed_name)
        )
        conn.commit()
        seed = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return {
            'statusCode': 201,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'isBase64Encoded': False,
            'body': json.dumps({
                'seed_id': seed['seed_id'],
                'goal_id': seed['goal_id'],
                'user_id': seed['user_id'],
                'seed_name': seed['seed_name'],
                'planted_date': seed['planted_date'].isoformat() if seed['planted_date'] else None,
                'growth_level': seed['growth_level'],
                'sprouts_count': seed['sprouts_count']
            })
        }
    
    elif method == 'GET':
        query_params = event.get('queryStringParameters', {}) or {}
        user_id = query_params.get('user_id')
        goal_id = query_params.get('goal_id')
        seed_id = query_params.get('seed_id')
        
        if seed_id:
            cursor.execute(
                "SELECT * FROM t_p72508054_karma_management_app.seeds WHERE seed_id = %s",
                (seed_id,)
            )
            seed = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if not seed:
                return {
                    'statusCode': 404,
                    'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                    'isBase64Encoded': False,
                    'body': json.dumps({'error': 'Seed not found'})
                }
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({
                    'seed_id': seed['seed_id'],
                    'goal_id': seed['goal_id'],
                    'user_id': seed['user_id'],
                    'seed_name': seed['seed_name'],
                    'planted_date': seed['planted_date'].isoformat() if seed['planted_date'] else None,
                    'growth_level': seed['growth_level'],
                    'sprouts_count': seed['sprouts_count'],
                    'last_watered': seed['last_watered'].isoformat() if seed['last_watered'] else None,
                    'water_streak_days': seed['water_streak_days'],
                    'total_actions': seed['total_actions']
                })
            }
        elif goal_id:
            cursor.execute(
                "SELECT * FROM t_p72508054_karma_management_app.seeds WHERE goal_id = %s ORDER BY planted_date DESC",
                (goal_id,)
            )
            seeds = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({
                    'seeds': [
                        {
                            'seed_id': s['seed_id'],
                            'goal_id': s['goal_id'],
                            'seed_name': s['seed_name'],
                            'growth_level': s['growth_level'],
                            'sprouts_count': s['sprouts_count']
                        } for s in seeds
                    ]
                })
            }
        elif user_id:
            cursor.execute(
                "SELECT * FROM t_p72508054_karma_management_app.seeds WHERE user_id = %s ORDER BY planted_date DESC",
                (user_id,)
            )
            seeds = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({
                    'seeds': [
                        {
                            'seed_id': s['seed_id'],
                            'goal_id': s['goal_id'],
                            'seed_name': s['seed_name'],
                            'growth_level': s['growth_level'],
                            'sprouts_count': s['sprouts_count']
                        } for s in seeds
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
                'body': json.dumps({'error': 'user_id, goal_id, or seed_id parameter required'})
            }
    
    elif method == 'PUT':
        body_data = json.loads(event.get('body', '{}'))
        seed_id = body_data.get('seed_id')
        action = body_data.get('action')
        
        if not seed_id or not action:
            cursor.close()
            conn.close()
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({'error': 'seed_id and action are required'})
            }
        
        if action == 'water':
            cursor.execute(
                "UPDATE t_p72508054_karma_management_app.seeds SET last_watered = NOW(), water_streak_days = water_streak_days + 1, total_actions = total_actions + 1 WHERE seed_id = %s RETURNING *",
                (seed_id,)
            )
            conn.commit()
            seed = cursor.fetchone()
            
            if seed and seed['total_actions'] % 5 == 0:
                cursor.execute(
                    "UPDATE t_p72508054_karma_management_app.seeds SET growth_level = growth_level + 1 WHERE seed_id = %s RETURNING *",
                    (seed_id,)
                )
                conn.commit()
                seed = cursor.fetchone()
            
            if seed and seed['total_actions'] % 10 == 0:
                cursor.execute(
                    "UPDATE t_p72508054_karma_management_app.seeds SET sprouts_count = sprouts_count + 1 WHERE seed_id = %s RETURNING *",
                    (seed_id,)
                )
                conn.commit()
                seed = cursor.fetchone()
        else:
            cursor.close()
            conn.close()
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({'error': 'Invalid action. Use "water"'})
            }
        
        cursor.close()
        conn.close()
        
        if not seed:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'isBase64Encoded': False,
                'body': json.dumps({'error': 'Seed not found'})
            }
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'isBase64Encoded': False,
            'body': json.dumps({
                'seed_id': seed['seed_id'],
                'growth_level': seed['growth_level'],
                'sprouts_count': seed['sprouts_count'],
                'water_streak_days': seed['water_streak_days'],
                'total_actions': seed['total_actions']
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
