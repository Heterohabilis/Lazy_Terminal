import subprocess
import json
import os

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

with open("base_mcp/prompts/app_runner.pmt", 'r') as f:
    DESCRIPTION = f.read()

class AppRunner:
    def launch_app(self, command: str) -> dict:
        """
        Launch a GUI application or long-running program using Popen.
        Ensures compatibility with both X11 (DISPLAY) and Wayland (WAYLAND_DISPLAY).
        """
        env = os.environ.copy()

        # Fallback logic: if no display info is present, set DISPLAY=:0
        if "WAYLAND_DISPLAY" not in env and "DISPLAY" not in env:
            env["DISPLAY"] = ":0"

        # print(command.split())
        process = subprocess.Popen(command, shell = True,
                                   env=env,
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL,
                                   stdin=subprocess.DEVNULL,
                                   start_new_session=True)
        return {
            "pid": process.pid,
            "message": f"Application launched with PID {process.pid}"
        }

async def serve() -> None:
    server = Server("mcp-app-runner")
    app_runner = AppRunner()

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="launch_app",
                description=DESCRIPTION,
                inputSchema={
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The shell command to launch the application (e.g., 'gnome-calculator', 'google-chrome')."
                        }
                    },
                    "required": ["command"],
                },
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        try:
            if name == "launch_app":
                command = arguments.get("command")
                if not command:
                    raise ValueError("Missing required argument: command")
                result = app_runner.launch_app(command)
            else:
                raise ValueError(f"Unknown tool: {name}")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        except Exception as e:
            raise ValueError(f"Error processing mcp-app-runner query: {str(e)}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)

import asyncio

if __name__ == "__main__":
    asyncio.run(serve())
