import json

log_path = "/Users/rohan/.gemini/antigravity-ide/brain/daa8389e-76e5-4f45-9540-33e2b7eec427/.system_generated/logs/transcript.jsonl"

def extract():
    results = []
    with open(log_path, "r") as f:
        for line in f:
            step = json.loads(line)
            step_idx = step.get("step_index")
            tool_calls = step.get("tool_calls", [])
            for tc in tool_calls:
                args = tc.get("args", {})
                for k, v in args.items():
                    val_str = str(v)
                    if "def _modal_edit_ingredients" in val_str and "🍽  Recipe Batch Size:" in val_str:
                        results.append(f"# === STEP {step_idx} (arg: {k}) ===")
                        results.append(val_str)
                        results.append("\n" + "="*80 + "\n")
    
    with open("/Users/rohan/Desktop/canteen/scratch/modal_code.py", "w") as out:
        out.write("\n".join(results))
    print("Extracted successfully!")

if __name__ == '__main__':
    extract()
