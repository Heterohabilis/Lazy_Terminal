# 🐢 Lazy Terminal

**Lazy Terminal** is an intelligent command-line assistant that connects language models with external tools through MCP (Modular Component Protocol). It dynamically determines whether a query should be directly answered or passed to a registered tool, enabling seamless terminal automation and smart interaction (you are lazy; it isn't).

---

## 🔧 Features

- **Dynamic Tool Routing:** Automatically chooses between direct response or tool invocation.
- **Contextual Memory:** Maintains conversation context (default 50 interactions).
- **Multi-model Support:** Easily integrate various language models via Coagent.
- **Robust JSON Handling:** Extracts and processes structured model responses.
- **Secure Bash Execution:** Runs safe, controlled bash scripts through MCP tools.

---

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

- Edit `config/models.yaml` to include your model credentials.
- Edit `config/mcp_servers.yaml` to list your MCP servers.

### Running

Launch the assistant with:

```bash
python main.py
```

For GUI, use:

```bash
make backend
cd frontend && npm run dev
```

Start interacting with Lazy Terminal directly from your console!

---

## 🛠 Example Usage

**Start the bash runner server:**

```bash
python test_servers/bash_runner.py
```

**Sample interaction:**

User input:
```
You: List all .txt files in ~/Documents and save output to files.txt
```

Assistant tool invocation:
```json
{
  "tool_name": "run_bash_script",
  "parameters": {
    "commands": "ls ~/Documents/*.txt > files.txt"
  }
}
```

Lazy Terminal will then execute this safely and return the results.

---

## 🔑 Environment Variables

Set model API keys as environment variables, e.g.:

```bash
export DEEPSEEK_API_KEY="your-api-key"
```

Ensure they match your settings in `models.yaml`.

---

## 📌 Roadmap

- [ ] Implement advanced memory compression.
- [ ] Add interactive UI (terminal/web).
- [ ] Enhance error handling and logging.
- [ ] Extend toolset (e.g., file handling, browser automation).
- [ ] Multi-tool calling

--- 

## 📚 Examples

- **GUI examples:**

<img src="https://github.com/user-attachments/assets/b8e4ae9c-fbbc-487f-9996-593ffd269a4f" alt="image" width="75%">
<img src="https://github.com/user-attachments/assets/3c51f2f4-10ac-44d0-b6f6-dce8f5d6db08" alt="image" width="75%">

- **Terminal-like examples:**
  
<img src="https://github.com/user-attachments/assets/6c8f83dc-5f3f-4ced-a860-1e8516a5ee0c" alt="image" width="75%">

---

## 🤝 Credits

- [Coagent](https://github.com/OpenCSGs/coagent)
- [MCP](https://modelcontextprotocol.io/introduction)

Enjoy building your intelligent terminal assistant!
