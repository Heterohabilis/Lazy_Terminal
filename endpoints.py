import asyncio
import json
import os
import sys

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from agent.prompt import CLEAN, get_system_prompt
from mcp_com.communication import call_tool
from utils.json_cleaner import extract_json_block
from utils.ring_memo import naive_memo
from utils.should_beautify import should_summarize

from coagent.agents import ChatMessage
from coagent.core import set_stderr_logger
from coagent.runtimes import LocalRuntime

from agent.model_router import build_agent

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

MAIN_MODEL = "deepseek-chat"
CLEANER_MODEL = "gpt-4o-mini"
MAIN = 'main'
CLEANER = 'cleaner'

app = FastAPI()
memo = naive_memo(n=50)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


main_agent = None
cleaner_agent = None
runtime = None

@app.on_event("startup")
async def startup_event():
    global main_agent, cleaner_agent, runtime
    set_stderr_logger()
    main_prompt = await get_system_prompt()
    main_agent = await build_agent(MAIN_MODEL, main_prompt, MAIN)
    cleaner_agent = await build_agent(CLEANER_MODEL, CLEAN, CLEANER)
    runtime = LocalRuntime()
    await runtime.__aenter__()
    await runtime.register(main_agent)
    await runtime.register(cleaner_agent)
    print("✅ Agents registered and ready")

@app.on_event("shutdown")
async def shutdown_event():
    global runtime
    if runtime:
        await runtime.__aexit__(None, None, None)

@app.post("/api/run")
async def run_llmos(request: Request):
    data = await request.json()
    user_input = data.get("prompt", "").strip()

    if not user_input:
        return {"output": "[Empty prompt]"}

    context_prompt = str(memo) + "\nuser: " + user_input
    response = await main_agent.run(
        ChatMessage(role="user", content=context_prompt).encode(),
        stream=False
    )
    msg = ChatMessage.decode(response)

    try:
        tool_call = msg.content
        # print(tool_call)
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
            result = msg.content
            memo.add(user_input, msg.content)

    except json.JSONDecodeError:
        result = msg.content
        memo.add(user_input, msg.content)

    return {"output": result}
