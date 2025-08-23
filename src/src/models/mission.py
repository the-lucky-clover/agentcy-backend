from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Mission(Base):
    __tablename__ = "missions"
    id = Column(String, primary_key=True)
    description = Column(Text, nullable=False)
    status = Column(String, default="PLANNING")
    classification = Column(String, default="CONFIDENTIAL")
    risk_level = Column(String, default="MODERATE")
    priority = Column(String, default="NORMAL")
    objective = Column(Text)
    ai_analysis = Column(Text)
    tactical_plan = Column(Text)
    assigned_agents = Column(Text)  # Stored as comma-separated string or JSON
    required_resources = Column(Text) # Stored as comma-separated string or JSON
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    progress_percentage = Column(Integer, default=0)
    current_phase = Column(String)

class IntelReport(Base):
    __tablename__ = "intel_reports"
    id = Column(String, primary_key=True)
    target = Column(String, nullable=False)
    intel_type = Column(String, nullable=False)
    classification = Column(String, default="CONFIDENTIAL")
    report_content = Column(Text)
    key_findings = Column(Text)
    threat_assessment = Column(Text)
    recommendations = Column(Text)
    source_agent = Column(String)
    confidence_level = Column(String)
    status = Column(String, default="DRAFT")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    mission_id = Column(String) # Foreign key to missions table

class ThreatAssessment(Base):
    __tablename__ = "threat_assessments"
    id = Column(String, primary_key=True)
    threat_name = Column(String, nullable=False)
    threat_type = Column(String)
    threat_level = Column(String, default="MODERATE")
    description = Column(Text)
    location = Column(String)
    probability = Column(String)
    impact_assessment = Column(Text)
    countermeasures = Column(Text)
    response_plan = Column(Text)
    assigned_personnel = Column(Text)
    status = Column(String, default="ACTIVE")
    last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    created_at = Column(DateTime, default=datetime.now)
    mission_id = Column(String) # Foreign key to missions table

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    clearance_level = Column(String, default="CONFIDENTIAL")
    role = Column(String, default="OPERATOR")
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime)
    is_active = Column(Integer, default=1) # SQLite does not have boolean type, use INTEGER 0 or 1

class AgentStatus(Base):
    __tablename__ = "agent_status"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, default="OFFLINE")
    current_mission = Column(String)
    capabilities = Column(Text)
    last_activity = Column(DateTime, default=datetime.now)
    performance_metrics = Column(Text)

class SystemLog(Base):
    __tablename__ = "system_logs"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    level = Column(String, nullable=False)
    component = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    user_id = Column(Integer)
    mission_id = Column(String)

# Database setup (for local development/testing)
def init_db(database_url="sqlite:///src/database/app.db"):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

if __name__ == "__main__":
    Session = init_db()
    session = Session()

    # Example initial data for agent_status
    initial_agents = [
        AgentStatus(id=\'INTEL-01\', name=\'Intelligence Agent Alpha\', status=\'OPERATIONAL\', current_mission=\'SIGINT Analysis\', capabilities=\'OSINT,SIGINT,Data Analysis\'),
        AgentStatus(id=\'TACTICAL-02\', name=\'Tactical Planning Agent\', status=\'OPERATIONAL\', current_mission=\'Route Optimization\', capabilities=\'Mission Planning,Terrain Analysis,Resource Allocation\'),
        AgentStatus(id=\'LOGISTICS-03\', name=\'Logistics Coordination Agent\', status=\'WARNING\', current_mission=\'Supply Chain Analysis\', capabilities=\'Supply Management,Transportation,Inventory\'),
        AgentStatus(id=\'COMMS-04\', name=\'Communications Agent\', status=\'OPERATIONAL\', current_mission=\'Secure Channel Maintenance\', capabilities=\'Secure Communications,Encryption,Signal Processing\'),
        AgentStatus(id=\'ANALYSIS-05\', name=\'Data Analysis Agent\', status=\'OPERATIONAL\', current_mission=\'Pattern Recognition\', capabilities=\'Data Mining,Pattern Analysis,Predictive Modeling\'),
        AgentStatus(id=\'SECURITY-06\', name=\'Security Monitoring Agent\', status=\'CRITICAL\', current_mission=\'Threat Detection\', capabilities=\'Threat Detection,Vulnerability Assessment,Incident Response\'),
    ]

    for agent in initial_agents:
        existing_agent = session.query(AgentStatus).filter_by(id=agent.id).first()
        if not existing_agent:
            session.add(agent)

    session.commit()
    session.close()
    print("Database initialized with initial agent data.")


