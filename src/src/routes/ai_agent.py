from flask import Blueprint, request, jsonify
import requests
import os

ai_agent_bp = Blueprint("ai_agent_bp", __name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAEkn-OTMM4b7h8r3GNV4CDhqKYoaVCilo")

@ai_agent_bp.route("/mission/execute", methods=["POST"])
def execute_mission():
    data = request.get_json()
    mission_description = data.get("mission")

    if not mission_description:
        return jsonify({"error": "Mission description is required"}), 400

    system_instruction = """You are AGENTCY.ONE, an advanced tactical military AI system. 
    Analyze the mission request and provide:
    1. Mission classification (INTEL/TACTICAL/LOGISTICS/SECURITY)
    2. Risk assessment (LOW/MODERATE/HIGH/CRITICAL)
    3. Required resources and personnel
    4. Step-by-step tactical plan
    5. Contingency measures
    6. Estimated timeline
    
    Format your response as a structured military briefing."""

    try:
        ai_response = call_gemini_api(mission_description, system_instruction)
        return jsonify({"message": "Mission analysis completed", "mission": {"ai_analysis": ai_response}}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def call_gemini_api(prompt, system_instruction):
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
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

    response = requests.post(api_url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    if "candidates" in result and len(result["candidates"]) > 0:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return "No response generated"

@ai_agent_bp.route("/intel/gather", methods=["POST"])
def gather_intel():
    data = request.get_json()
    intel_request = data.get("intel_request")

    if not intel_request:
        return jsonify({"error": "Intel request is required"}), 400

    system_instruction = """You are AGENTCY.ONE, an advanced intelligence gathering AI. 
    Analyze the intel request and provide:
    1. Target identification
    2. Data sources (OSINT, SIGINT, HUMINT, GEOINT)
    3. Key findings
    4. Threat assessment
    5. Recommendations for further action
    
    Format your response as a structured intelligence report."""

    try:
        ai_response = call_gemini_api(intel_request, system_instruction)
        return jsonify({"message": "Intelligence gathered", "report": {"ai_analysis": ai_response}}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_agent_bp.route("/tactical/plan", methods=["POST"])
def tactical_plan():
    data = request.get_json()
    plan_request = data.get("plan_request")

    if not plan_request:
        return jsonify({"error": "Plan request is required"}), 400

    system_instruction = """You are AGENTCY.ONE, an advanced tactical planning AI. 
    Analyze the planning request and provide:
    1. Mission objective
    2. Resource allocation
    3. Movement strategies
    4. Contingency measures
    5. Estimated timeline
    
    Format your response as a structured tactical plan."""

    try:
        ai_response = call_gemini_api(plan_request, system_instruction)
        return jsonify({"message": "Tactical plan generated", "plan": {"ai_analysis": ai_response}}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_agent_bp.route("/threat/assess", methods=["POST"])
def threat_assess():
    data = request.get_json()
    threat_request = data.get("threat_request")

    if not threat_request:
        return jsonify({"error": "Threat request is required"}), 400

    system_instruction = """You are AGENTCY.ONE, an advanced threat assessment AI. 
    Analyze the threat request and provide:
    1. Threat identification
    2. Threat level (LOW/MODERATE/HIGH/CRITICAL)
    3. Potential impact
    4. Recommended countermeasures
    5. Response plan
    
    Format your response as a structured threat assessment report."""

    try:
        ai_response = call_gemini_api(threat_request, system_instruction)
        return jsonify({"message": "Threat assessment completed", "assessment": {"ai_analysis": ai_response}}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_agent_bp.route("/agents/status", methods=["GET"])
def get_agent_status():
    # This would typically fetch from a database
    agent_data = [
        {"id": "INTEL-01", "name": "Intelligence Agent Alpha", "status": "OPERATIONAL", "currentMission": "SIGINT Analysis"},
        {"id": "TACTICAL-02", "name": "Tactical Planning Agent", "status": "OPERATIONAL", "currentMission": "Route Optimization"},
        {"id": "LOGISTICS-03", "name": "Logistics Coordination Agent", "status": "WARNING", "currentMission": "Supply Chain Analysis"},
        {"id": "COMMS-04", "name": "Communications Agent", "status": "OPERATIONAL", "currentMission": "Secure Channel Maintenance"},
        {"id": "ANALYSIS-05", "name": "Data Analysis Agent", "status": "OPERATIONAL", "currentMission": "Pattern Recognition"},
        {"id": "SECURITY-06", "name": "Security Monitoring Agent", "status": "CRITICAL", "currentMission": "Threat Detection"}
    ]
    return jsonify(agent_data), 200

@ai_agent_bp.route("/system/status", methods=["GET"])
def get_system_status():
    status_data = {
        "aiProcessing": "ONLINE",
        "secureComms": "ENCRYPTED",
        "database": "OPERATIONAL",
        "activeAgents": 6
    }
    return jsonify(status_data), 200


