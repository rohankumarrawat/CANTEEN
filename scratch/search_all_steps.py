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
                    if "def _modal_edit_ingredients" in val_str:
                        is_truncated = "truncated" in val_str or "<truncated" in val_str
                        print(f"Step {step_idx}, key {k}, len {len(val_str)}, truncated: {is_truncated}")
                        if not is_truncated and len(val_str) > 1000:
                            print("FOUND FULL CODE in Step", step_idx)
                            with open(f"/Users/rohan/Desktop/canteen/scratch/step_{step_idx}_{k}.py", "w") as out:
                                out.write(val_str)

if __name__ == '__main__':
    search()
