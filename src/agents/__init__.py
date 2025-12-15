"""
Agent module

Contains:
- orchestrator.py: Original single-layer Agent (deprecated)
- orchestrator_v2.py: Dual-layer architecture Agent (recommended)
- analyst_agent.py: Upper-layer Analyst/Planner Agent
"""

# Export original single-layer architecture (for backward compatibility)
from src.agents.orchestrator import (
    SensorsAnalyticsAgent,
    create_agent
)

# Export new dual-layer architecture (recommended)
from src.agents.orchestrator_v2 import (
    SensorsAnalyticsAgentV2,
    create_agent_v2
)

# Export sub-agents
from src.agents.analyst_agent import AnalystAgent

__all__ = [
    # Original single-layer architecture
    "SensorsAnalyticsAgent",
    "create_agent",

    # Dual-layer architecture
    "SensorsAnalyticsAgentV2",
    "create_agent_v2",
    "AnalystAgent",
]
