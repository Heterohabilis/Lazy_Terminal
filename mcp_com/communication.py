import asyncio

import requests
import yaml
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

ARGS = 'args'
URL = 'url'
COMMAND = 'command'
ROUTER = {}


def load_manifest_http(server_url: str) -> dict:
    resp = requests.get(f"{server_url}/manifest")
    resp.raise_for_status()
    return resp.json()


async def load_manifest_stdio(server_params):
    async with stdio_client(server_params) as (stdio, write):
        async with ClientSession(stdio, write) as session:
            await session.initialize()
            manifest = await session.list_tools()
    return manifest


async def manifest_loader(yaml_path: str = "./config/mcp_servers.yaml"):
    tools = []
    with open (yaml_path, 'r') as f:
        servers = yaml.safe_load(f)
    for server in servers:
        if ARGS in server:
            server_params = StdioServerParameters(
                command=server[COMMAND],
                args=server[ARGS],
            )
            manifest= await load_manifest_stdio(server_params)
            for tool in manifest.tools:
                tools.append({'tool': tool.name,
                              'description': tool.description, 'params': tool.inputSchema})
                ROUTER[tool.name] = (server_params, 'stdio')
        elif URL in server:
            manifest=load_manifest_http(server[URL])
            for tool in manifest['tools']:
                tools.append({'tool': tool['tool'],
                              'description': tool['description'], 'params': tool['inputSchema']})
                ROUTER[tool['tool']] = (server[URL], 'http')
    # print(ROUTER)
    return tools


async def call_tool(tool_name, params):
    handler, type = ROUTER[tool_name]
    if type == 'stdio':
        async with stdio_client(handler) as (stdio, write):
            async with ClientSession(stdio, write) as session:
                await session.initialize()
                # print(tool_name, params)
                response = await session.call_tool(tool_name, params)
        return response
    if type == 'http':
        url = handler + "/call"
        resp = requests.post(url, json=params)
        resp.raise_for_status()
        return resp.json()

if __name__ == '__main__':
    asyncio.run(manifest_loader())
