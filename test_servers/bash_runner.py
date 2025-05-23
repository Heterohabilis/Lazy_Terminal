from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)
PORT = 1510
DESCRIPTION = '''[Generate a valid bash script] that solves the user’s task.  
- Do not use 'sudo' or any root-only commands; 
- Use heredoc (cat <<EOF > file) to write source code if needed.  
- Return your response as plain bash commands, separated by newlines.  
- The output should be directly executable in a non-root Unix environment.  
example: open an application, write code, find files...
'''


@app.route("/manifest", methods=["GET"])
def manifest():
    return jsonify({
        "tools": [{
            "tool": "run_bash_script",
            "description": DESCRIPTION,
            "inputSchema": {
                "type": "object",
                "properties": {
                    "commands": {
                        "type": "string",
                        "description": "The bash commands to run"
                    }
                },
                "required": ["commands"]
            }
        }]
    })

@app.route("/call", methods=["POST"])
def call():
    data = request.get_json(silent=False)
    print(data)
    if not data:
        print("No data")
        return jsonify({"error": "No data provided"}), 400

    commands = data.get("commands")
    if not commands:
        print("No command")
        return jsonify({"error": "Missing 'commands' in arguments"})

    try:
        result = subprocess.run(
            ["bash", "-c", commands],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=1000,
            text=True,
        )

        return jsonify({
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        })

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Command execution timed out"}), 504

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=PORT)
