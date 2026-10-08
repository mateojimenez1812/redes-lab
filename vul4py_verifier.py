import subprocess
import os

def verify_patch(vulnerable_file_path: str, patch_content: str) -> bool:
    patch_path = "temp_patch.diff"
    with open(patch_path, "w") as f:
        f.write(patch_content)
    
    try:
        subprocess.run(["patch", vulnerable_file_path, patch_path], check=True)
        result = subprocess.run(["vul4py", "verify", vulnerable_file_path], capture_output=True, text=True)
        verified_success = (result.returncode == 0)
        return verified_success
    except Exception as e:
        print(f"Error durante la verificación con Vul4Py: {e}")
        return False
    finally:
        if os.path.exists(patch_path):
            os.remove(patch_path)
