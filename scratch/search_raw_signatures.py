import json

log_path = "/Users/rohan/.gemini/antigravity-ide/brain/daa8389e-76e5-4f45-9540-33e2b7eec427/.system_generated/logs/transcript.jsonl"

def search():
    with open(log_path, "r") as f:
        for line in f:
            if "NCO I/C" in line or "NCO In-Charge" in line or "Commissioned" in line:
                # print snippet of line around matching text
                idx = line.find("NCO I/C")
                if idx == -1:
                    idx = line.find("NCO In-Charge")
                if idx == -1:
                    idx = line.find("Commissioned")
                start = max(0, idx - 400)
                end = min(len(line), idx + 1500)
                print(f"Match found in line of length {len(line)}:")
                print(line[start:end])
                print("="*80)

if __name__ == '__main__':
    search()
