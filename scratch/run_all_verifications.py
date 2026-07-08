import os
import glob
import subprocess

def main():
    verify_files = sorted(glob.glob('/Users/rohan/Desktop/canteen/verify_db_ingestion_*.py'))
    print(f"Found {len(verify_files)} verification files.")
    
    passed = 0
    failed = []
    
    for vf in verify_files:
        basename = os.path.basename(vf)
        res = subprocess.run(['python3', vf], capture_output=True, text=True)
        if res.returncode == 0 and "ALL VERIFICATIONS PASSED" in res.stdout:
            passed += 1
        else:
            failed.append((basename, res.stdout, res.stderr))
            
    print(f"Passed: {passed}/{len(verify_files)}")
    print(f"Failed: {len(failed)}")
    for name, stdout, stderr in failed:
        print(f"\n--- {name} FAILED ---")
        lines = stdout.strip().split("\n")
        err_lines = [l for l in lines if "mismatch" in l or "errors:" in l or "FAILED" in l or "-" in l]
        for l in err_lines[-10:]:
            print(f"  {l}")
        if stderr:
            print(f"  STDERR: {stderr}")

if __name__ == '__main__':
    main()
