import json

log_path = "/Users/rohan/.gemini/antigravity-ide/brain/daa8389e-76e5-4f45-9540-33e2b7eec427/.system_generated/logs/transcript.jsonl"

def search():
    with open(log_path, "r") as f:
        for line in f:
            step = json.loads(line)
            step_idx = step.get("step_index")
            if step_idx == 1108:
                tool_calls = step.get("tool_calls", [])
                for tc in tool_calls:
                    print("Tool:", tc.get("name"))
                    args = tc.get("args", {})
                    for k, v in args.items():
                        print(f"--- Key: {k} ---")
                        print(str(v)[:3000])
                        print("="*80)

if __name__ == '__main__':
    search()
