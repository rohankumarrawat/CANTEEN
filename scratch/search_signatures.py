import json

log_path = "/Users/rohan/.gemini/antigravity-ide/brain/daa8389e-76e5-4f45-9540-33e2b7eec427/.system_generated/logs/transcript.jsonl"

def search():
    with open(log_path, "r") as f:
        for line in f:
            step = json.loads(line)
            step_idx = step.get("step_index")
            if 1070 <= step_idx <= 1120:
                tool_calls = step.get("tool_calls", [])
                for tc in tool_calls:
                    args = tc.get("args", {})
                    for k, v in args.items():
                        val_str = str(v)
                        if "Prepared By" in val_str or "Officer-in-Charge" in val_str or "signature" in val_str.lower():
                            print(f"Step {step_idx}, key {k}:")
                            print(val_str)
                            print("="*80)

if __name__ == '__main__':
    search()
