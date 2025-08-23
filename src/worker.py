from js import Response, fetch
import json
import asyncio
from datetime import datetime

# Import your Flask routes and logic
from src.routes.ai_agent import call_gemini_api

async def handle_request(request):
    """Main request handler for Cloudflare Workers"""
    url = request.url
    method = request.method
    
    # Parse the request
    if method == "OPTIONS":
        return handle_cors()
    
    # Route handling
    if "/api/mission/execute" in url and method == "POST":
        return await handle_mission_execute(request)
    elif "/api/intel/gather" in url and method == "POST":
        return await handle_intel_gather(request)
    elif "/api/tactical/plan" in url and method == "POST":
        return await handle_tactical_plan(request)
    elif "/api/threat/assess" in url and method == "POST":
        return await handle_threat_assess(request)
    elif "/api/agents/status" in url and method == "GET":
        return handle_agent_status()
    elif "/api/system/status" in url and method == "GET":
        return handle_system_status()
    else:
        return Response.new("Not Found", {"status": 404})

def handle_cors():
    """Handle CORS preflight requests"""
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Max-Age": "86400"
    }
    return Response.new("", {"status": 200, "headers": headers})

async def handle_mission_execute(request):
    """Handle mission execution requests"""
    try:
        body = await request.json()
        mission_description = body.get('mission', '')
        
        # Call Gemini API
        system_instruction = """You are AGENTCY.ONE, an advanced tactical military AI system. 
        Analyze the mission request and provide:
        1. Mission classification (INTEL/TACTICAL/LOGISTICS/SECURITY)
        2. Risk assessment (LOW/MODERATE/HIGH/CRITICAL)
        3. Required resources and personnel
        4. Step-by-step tactical plan
        5. Contingency measures
        6. Estimated timeline
        
        Format your response as a structured military briefing."""
        
        ai_response = await call_gemini_api_async(mission_description, system_instruction)
        
        mission_data = {
            'id': f"MISSION-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'description': mission_description,
            'status': 'PLANNING',
            'created_at': datetime.now().isoformat(),
            'ai_analysis': ai_response,
            'risk_level': 'MODERATE',
            'assigned_agents': ['INTEL-01', 'TACTICAL-02']
        }
        
        response_data = {
            'success': True,
            'mission': mission_data,
            'message': 'Mission analysis completed'
        }
        
        headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
        
        return Response.new(json.dumps(response_data), {"status": 200, "headers": headers})
        
    except Exception as e:
        error_response = {'error': str(e)}
        headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
        return Response.new(json.dumps(error_response), {"status": 500, "headers": headers})

async def call_gemini_api_async(prompt, system_instruction):
    """Async version of Gemini API call for Workers"""
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyAEkn-OTMM4b7h8r3GNV4CDhqKYoaVCilo"
    
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"{system_instruction}\n\n{prompt}"
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 2048,
        }
    }
    
    try:
        response = await fetch(api_url, {
            "method": "POST",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(data)
        })
        
        result = await response.json()
        
        if response.status == 200:
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "No response generated"
        else:
            return f"API Error: {response.status}"
            
    except Exception as e:
        return f"Error calling Gemini API: {str(e)}"

# Export the handler
export = handle_request
