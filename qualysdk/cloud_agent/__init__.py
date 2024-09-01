"""
Cloud Agent APIs let you pull data on and modify Cloud Agents in your account.

https://cdn2.qualys.com/docs/qualys-ca-api-user-guide.pdf
"""

from .purge import purge_agent, bulk_purge_agent
from .calls import list_agents, launch_ods, bulk_launch_ods
