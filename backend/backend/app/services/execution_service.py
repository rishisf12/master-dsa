import subprocess
import tempfile
import os
from typing import Dict


class ExecutionService:
    @staticmethod
    def execute_python(code: str, stdin: str = "") -> Dict:
        """Execute Python code."""
        try:
            # Use python3 directly (we're in WSL)
            result = subprocess.run(
                ["python3", "-c", code],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"stdout": "", "stderr": "Execution timeout (5 seconds)", "returncode": 1}
        except Exception as e:
            return {"stdout": "", "stderr": str(e), "returncode": 1}

    @staticmethod
    def execute_cpp(code: str, stdin: str = "") -> Dict:
        """Execute C++ code."""
        temp_dir = "/tmp/"
        cpp_file = f"{temp_dir}temp_{os.getpid()}.cpp"
        output_file = f"{temp_dir}temp_{os.getpid()}.out"
        
        try:
            # Write code to temp file
            with open(cpp_file, 'w') as f:
                f.write(code)
            
            # Compile
            compile_result = subprocess.run(
                ["g++", cpp_file, "-o", output_file],
                capture_output=True,
                text=True
            )
            
            if compile_result.returncode != 0:
                return {"stdout": "", "stderr": compile_result.stderr, "returncode": compile_result.returncode}
            
            # Run
            result = subprocess.run(
                [output_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {"stdout": "", "stderr": "Execution timeout (5 seconds)", "returncode": 1}
        except Exception as e:
            return {"stdout": "", "stderr": str(e), "returncode": 1}
        finally:
            # Clean up temp files
            try:
                os.unlink(cpp_file)
                os.unlink(output_file)
            except:
                pass

    @staticmethod
    def execute(language: str, code: str, stdin: str = "") -> Dict:
        """Execute code in the specified language."""
        if language == "python":
            return ExecutionService.execute_python(code, stdin)
        elif language == "cpp":
            return ExecutionService.execute_cpp(code, stdin)
        else:
            return {"stdout": "", "stderr": f"Unsupported language: {language}", "returncode": 1}