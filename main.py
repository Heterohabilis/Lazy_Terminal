import asyncio
import json
import sys
import os

from agent.prompt import CLEAN, get_system_prompt
from mcp_com.communication import call_tool
from utils.json_cleaner import extract_json_block
from utils.ring_memo import naive_memo
from utils.should_beautify import should_summarize

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
MAIN_MODEL = "gpt-4o"
CLEANER_MODEL = "gpt-4o-mini"

from coagent.agents import ChatMessage
from coagent.core import set_stderr_logger
from coagent.runtimes import LocalRuntime

from agent.model_router import build_agent


async def agent_start(agent):
    # init the memo
    memo = naive_memo(n=50)
    cleaner_agent = await build_agent(CLEANER_MODEL, CLEAN)
    print("Agent is ready; input 'exit' to quit")

    async with LocalRuntime() as runtime:
        await runtime.register(agent)
        await runtime.register(cleaner_agent)
        while True:
            user_input = input("You：").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("👋 Bye！")
                break

            context_prompt = str(memo) + "\nuser: " + user_input
            response = await agent.run(
                ChatMessage(role="user", content=context_prompt).encode(),
                stream=False
            )
            msg = ChatMessage.decode(response)

            try:
                tool_call = msg.content
                if "tool_name" in tool_call and "parameters" in tool_call:
                    tool_call = json.loads(extract_json_block(tool_call))
                    raw_result = await call_tool(tool_call["tool_name"], tool_call["parameters"])
                    raw_result = str(raw_result)

                    # clean the result
                    try:
                        summary_input = (
                                "user: " + user_input + "\n"
                                                        "guide: \n raw: " + CLEAN + raw_result
                        )
                        result = await cleaner_agent.run(
                            ChatMessage(role="system", content=summary_input).encode(),
                            stream=False
                        )
                        result = ChatMessage.decode(result).content

                        memo.add(user_input, json.dumps({
                            "tool_name": tool_call["tool_name"],
                            "result": result
                        }, ensure_ascii=False))
                    except Exception as e:
                        result = raw_result
                        memo.add(user_input, json.dumps({
                            "tool_name": tool_call["tool_name"],
                            "result": result
                        }, ensure_ascii=False))

                else:
                    print("🤖", msg.content)
                    memo.add(user_input, msg.content)

            except json.JSONDecodeError:
                memo.add(user_input, msg.content)



async def main():
    set_stderr_logger()
    main_agent_prompt = await get_system_prompt()
    main_agent = await build_agent(MAIN_MODEL, main_agent_prompt)
    await agent_start(main_agent)



if __name__ == "__main__":
    asyncio.run(main())
