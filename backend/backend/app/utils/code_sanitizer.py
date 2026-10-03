import re
import tempfile
import os
import subprocess
from typing import Tuple


class CodeSanitizer:
    """Sanitize and safely execute code."""
    
    # Dangerous imports/commands to block
    DANGEROUS_PATTERNS = [
        r'import\s+os',
        r'import\s+subprocess',
        r'import\s+socket',
        r'import\s+requests',
        r'__import__\s*\(',
        r'eval\s*\(',
        r'exec\s*\(',
        r'compile\s*\(',
        r'open\s*\(',
        r'file\s*\(',
        r'system\s*\(',
        r'popen\s*\(',
        r'call\s*\(',
        r'check_output\s*\(',
    ]
    
    @classmethod
    def sanitize_python(cls, code: str) -> Tuple[bool, str]:
        """Sanitize Python code."""
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                return False, f"Blocked: {pattern} is not allowed"
        return True, code
    
    @classmethod
    def sanitize_cpp(cls, code: str) -> Tuple[bool, str]:
        """Sanitize C++ code."""
        # Check for dangerous headers
        dangerous_headers = [
            '<windows.h>',
            '<sys/socket.h>',
            '<unistd.h>',
            '<dlfcn.h>',
        ]
        for header in dangerous_headers:
            if header in code:
                return False, f"Blocked: {header} is not allowed"
        return True, code
    
    @classmethod
    def execute_python(cls, code: str, stdin: str = "") -> dict:
        """Execute Python code safely."""
        # Sanitize first
        is_safe, message = cls.sanitize_python(code)
        if not is_safe:
            return {"stdout": "", "stderr": message, "returncode": 1}
        
        try:
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
    
    @classmethod
    def execute_cpp(cls, code: str, stdin: str = "") -> dict:
        """Execute C++ code safely."""
        # Sanitize first
        is_safe, message = cls.sanitize_cpp(code)
        if not is_safe:
            return {"stdout": "", "stderr": message, "returncode": 1}
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False) as f:
            f.write(code.encode())
            cpp_file = f.name
        
        output_file = tempfile.NamedTemporaryFile(suffix=".out", delete=False)
        output_file.close()
        
        try:
            # Compile
            compile_result = subprocess.run(
                ["g++", cpp_file, "-o", output_file.name],
                capture_output=True,
                text=True
            )
            
            if compile_result.returncode != 0:
                return {"stdout": "", "stderr": compile_result.stderr, "returncode": compile_result.returncode}
            
            # Run
            result = subprocess.run(
                [output_file.name],
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
            # Clean up temporary files
            try:
                os.unlink(cpp_file)
                os.unlink(output_file.name)
            except:
                pass