import json

log_path = "/Users/rohan/.gemini/antigravity-ide/brain/daa8389e-76e5-4f45-9540-33e2b7eec427/.system_generated/logs/transcript.jsonl"

def search():
    with open(log_path, "r") as f:
        for line in f:
            if "sc1" in line or "NCO I/C" in line:
                idx = line.find("sc1")
                if idx == -1:
                    idx = line.find("NCO I/C")
                start = max(0, idx - 50)
                end = min(len(line), idx + 2500)
                print(line[start:end])
                print("="*80)

if __name__ == '__main__':
    search()
