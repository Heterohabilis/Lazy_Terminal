
from mcp_com.communication import manifest_loader

with open("agent/prompts/main.pmt", 'r') as f:
    PROMPT = f.read()

TOOLS = ""

with open("agent/prompts/cleaner.pmt", 'r') as f:
    CLEAN = f.read()

async def get_system_prompt():
    global TOOLS
    _ = await manifest_loader()
    TOOLS = str(_)
    return PROMPT+' '+TOOLS

if __name__ == "__main__":
    print(get_system_prompt())