import json

log_path = "/Users/rohan/.gemini/antigravity-ide/brain/daa8389e-76e5-4f45-9540-33e2b7eec427/.system_generated/logs/transcript.jsonl"

def search():
    with open(log_path, "r") as f:
        for line in f:
            step = json.loads(line)
            step_idx = step.get("step_index")
            tool_calls = step.get("tool_calls", [])
            for tc in tool_calls:
                args = tc.get("args", {})
                for k, v in args.items():
                    val_str = str(v)
                    if "_modal_add_sale" in val_str or "_modal_edit_sale" in val_str:
                        print(f"Step {step_idx}, key {k}, len {len(val_str)}")
                        if "Meal Name" in val_str and "Rate" in val_str and len(val_str) < 4000:
                            print(val_str[:1500])
                            print("...")

if __name__ == '__main__':
    search()
