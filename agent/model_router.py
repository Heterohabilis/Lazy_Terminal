# agent/model_router.py

from coagent.agents import ChatAgent
from coagent.core import AgentSpec, new

from agent.client_builder import build_model_client


async def build_agent(model_name: str, prompt:str, role: str) -> AgentSpec:
    # create ModelClient
    client = build_model_client(model_name)

    # load prompt
    # system_prompt = await get_system_prompt()

    # create agent
    agent = AgentSpec(
        f"{role}_agent",
        new(
            ChatAgent,
            system=prompt,
            client=client,
        ),
    )

    return agent


