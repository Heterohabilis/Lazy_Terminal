import asyncio
import json
import sys
import os

from my_mcp.mcp_invoker import call_tool
from utils.json_cleaner import extract_json_block

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
MODEL = "deepseek-chat"

from coagent.agents import ChatMessage
from coagent.core import set_stderr_logger
from coagent.runtimes import LocalRuntime

from agent.model_router import build_agent


async def agent_start(translator):
    history = []
    print("Agent is ready; input 'exit' to quit")

    async with LocalRuntime() as runtime:
        await runtime.register(translator)
        while True:
            user_input = input("You：").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("👋 Bye！")
                break
            history.append(ChatMessage(role="user", content=user_input))
            response = await translator.run(history[-1].encode(), stream=False)
            msg = ChatMessage.decode(response)
            try:
                tool_call = msg.content
                if "tool_name" in tool_call and "parameters" in tool_call:
                    tool_call = json.loads(extract_json_block(tool_call))
                    result = call_tool(tool_call["tool_name"], tool_call["parameters"])
                    print(f"return code: {result['returncode']}")
                    if(len(result['stderr'])): print(f"stderr: {result['stderr']}")
                    if(len(result['stdout'])): print(f"stdout: {result['stdout']}")
                    print("🤖", "done")

                    history.append(msg)
                    history.append(ChatMessage(
                        role="tool",
                        content=json.dumps({
                            "tool_name": tool_call["tool_name"],
                            "result": result
                        }, ensure_ascii=False)
                    ))

                else:
                    print("🤖", msg.content)
                    history.append(msg)

            except json.JSONDecodeError:
                history.append(msg)
            except Exception as e:
                print("🤖", e)


async def main():
    set_stderr_logger()
    translator = build_agent(MODEL)
    await agent_start(translator)



if __name__ == "__main__":
    asyncio.run(main())
