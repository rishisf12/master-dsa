
import os
import httpx
import json
from typing import Dict, Optional, Any
from pathlib import Path
from dotenv import load_dotenv
from app.utils.logger import logger

# ============================================================
# Load environment variables
# ============================================================
backend_dir = Path(__file__).parent.parent.parent
env_path = backend_dir / '.env'
load_dotenv(env_path)


# ============================================================
# AI Service Class
# ============================================================
class AIService:
    """AI service using Groq API for code analysis."""

    def __init__(self):
        """Initialize the AI service with Groq (FREE, fast inference)."""
        self.base_url = "https://api.groq.com/openai/v1"
        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.model = "llama-3.3-70b-versatile"
        self.max_tokens = 4000
        self.timeout = 120.0
        self._log_api_key_status()

    def _log_api_key_status(self) -> None:
        """Log whether the API key is loaded."""
        if self.api_key:
            logger.info(f"✅ GROQ_API_KEY loaded: {self.api_key[:10]}...")
        else:
            logger.warning("⚠️ GROQ_API_KEY not set. Please add to .env file.")
            logger.warning(f"Looking for .env at: {env_path}")

    def _build_prompt(
        self,
        problem_name: str,
        python_code: str,
        cpp_code: str,
        python_time_complexity: Optional[str] = None,
        python_space_complexity: Optional[str] = None,
        cpp_time_complexity: Optional[str] = None,
        cpp_space_complexity: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> str:
        """Build the prompt for the AI model."""
        python_code = python_code or "# No Python code provided"
        cpp_code = cpp_code or "// No C++ code provided"

        return f"""Problem: {problem_name}

User's Stated Complexity:
- Python Time: {python_time_complexity or 'Not provided'}
- Python Space: {python_space_complexity or 'Not provided'}
- C++ Time: {cpp_time_complexity or 'Not provided'}
- C++ Space: {cpp_space_complexity or 'Not provided'}
- Notes/Intuition: {notes or 'Not provided'}

Python Solution:
```python
{python_code}
```

C++ Solution:
```cpp
{cpp_code}
```

You are an expert DSA instructor. Analyze both solutions deeply and provide a comprehensive comparison.

┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. SUMMARY OF BOTH APPROACHES │
└─────────────────────────────────────────────────────────────────────────────┘

Explain the core algorithmic strategy used (e.g., Sliding Window, Two-Pointers, Backtracking, DP, Greedy, Divide & Conquer)

Explain how each solution implements this strategy in its respective language

Include a side-by-side comparison of the approach taken

┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. COMPLEXITY ANALYSIS - PYTHON (SEPARATE) │
└─────────────────────────────────────────────────────────────────────────────┘

PYTHON TIME COMPLEXITY:

Calculate the ACTUAL Time Complexity of the Python solution

Explain the calculation step by step

Identify the dominant operations

Include best, average, and worst-case scenarios if applicable

Note if amortized analysis is needed (e.g., for hash map operations)

PYTHON SPACE COMPLEXITY:

Calculate the ACTUAL Space Complexity of the Python solution

Distinguish between auxiliary space (algorithm) and input space (language overhead)

Note if any data structures are created that use extra space

┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. COMPLEXITY ANALYSIS - C++ (SEPARATE) │
└─────────────────────────────────────────────────────────────────────────────┘

C++ TIME COMPLEXITY:

Calculate the ACTUAL Time Complexity of the C++ solution

Explain the calculation step by step

Identify the dominant operations

Include best, average, and worst-case scenarios if applicable

Note if amortized analysis is needed (e.g., for hash map operations)

C++ SPACE COMPLEXITY:

Calculate the ACTUAL Space Complexity of the C++ solution

Distinguish between auxiliary space (algorithm) and input space (language overhead)

Note if any data structures are created that use extra space

┌─────────────────────────────────────────────────────────────────────────────┐
│ 4. COMPLEXITY VALIDATION (Compare with User's Claims) │
└─────────────────────────────────────────────────────────────────────────────┘

User stated Python Time: {python_time_complexity or 'Not provided'}
User stated Python Space: {python_space_complexity or 'Not provided'}
User stated C++ Time: {cpp_time_complexity or 'Not provided'}
User stated C++ Space: {cpp_space_complexity or 'Not provided'}

Check each solution separately:

Python TC: Is the user's claim CORRECT ✓ or INCORRECT ✗?

Python SC: Is the user's claim CORRECT ✓ or INCORRECT ✗?

C++ TC: Is the user's claim CORRECT ✓ or INCORRECT ✗?

C++ SC: Is the user's claim CORRECT ✓ or INCORRECT ✗?

If INCORRECT: Clearly explain what the correct complexity is and why the user's analysis was wrong
If INCOMPLETE: Explain what was missing and provide the complete picture

┌─────────────────────────────────────────────────────────────────────────────┐
│ 5. KEY DIFFERENCES IN REAL-LIFE SCENARIOS (DSA & SYSTEMS) │
└─────────────────────────────────────────────────────────────────────────────┘

Memory Layout & Cache Locality: How do std::vector vs Python list affect performance for large datasets?

Mutability & Side Effects: Does the C++ version modify input? Does Python use immutable copies?

Integer Overflow: Does the C++ solution handle large sums safely (using long long)? Does Python handle this natively?

Pass by Value vs Reference: How does this affect performance and memory spikes?

Language Idioms: How do Pythonic comprehensions vs C++ STL algorithms affect readability and maintainability?

┌─────────────────────────────────────────────────────────────────────────────┐
│ 6. CODE IMPROVEMENTS & OPTIMIZATIONS │
└─────────────────────────────────────────────────────────────────────────────┘

IMPORTANT: Suggest specific improvements for BOTH solutions.

PYTHON IMPROVEMENTS:

Suggest better Pythonic ways to write the code

Suggest micro-optimizations (e.g., using list comprehension, generators, built-in functions)

Suggest using slots if applicable

Suggest better data structures if applicable

Provide code examples for each improvement

C++ IMPROVEMENTS:

Suggest using better STL algorithms

Suggest using const references to avoid copying

Suggest using ios_base::sync_with_stdio(false) and cin.tie(NULL) for faster I/O

Suggest using move semantics or emplace_back

Suggest using long long for large numbers

Provide code examples for each improvement

┌─────────────────────────────────────────────────────────────────────────────┐
│ 7. EDGE CASES & ERROR HANDLING (Production Ready) │
└─────────────────────────────────────────────────────────────────────────────┘

Test these specific inputs and explain results:

Minimal input (e.g., nums = [] or n=1)

Maximum constraints (e.g., nums.length = 10^5)

Duplicate values / Negative numbers / Zero

Large numbers (overflow scenarios)

Error Handling: Should we use assert, exceptions, or optional returns?

Which solution handles edge cases better?

┌─────────────────────────────────────────────────────────────────────────────┐
│ 8. INTERVIEW NOTES (Communication & Hints) │
└─────────────────────────────────────────────────────────────────────────────┘

Brute Force Starting Point: What is the naive solution and its complexity?

Optimization Narrative: How to walk the interviewer from naive to optimal approach?

Trade-offs: When to choose Solution A over B in an interview (code speed vs development speed)?

Key talking points for each solution

┌─────────────────────────────────────────────────────────────────────────────┐
│ 9. VERDICT (The "Ship it" Decision) │
└─────────────────────────────────────────────────────────────────────────────┘

Which solution is superior for a "FAANG" interview (coding speed + clarity)?

Which solution is superior for a "High-Frequency Trading" / "Embedded" environment (raw performance)?

Which solution would you merge into a production codebase and why?

Final recommendation with clear reasoning

Format the response with clear numbered sections. Use plain text with capitalised headings. Provide specific code examples for improvements. Be detailed and educational."""

    def _make_api_request(self, prompt: str) -> httpx.Response:
        try:
            timeout = httpx.Timeout(self.timeout, connect=10.0)
            
            with httpx.Client(timeout=timeout, verify=False) as client:  # ✅ Add verify=False
                response = client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "Host": "api.groq.com"  # ✅ Add this header
                    },
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                        "max_tokens": self.max_tokens,
                    },
                )
                return response
        except Exception as e:
            logger.error(f"API request failed: {e}")
            raise  # Re-raise to be handled by the calling method

    def _handle_success_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle a successful API response."""
        try:
            data = response.json()
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON response")
            return {"summary": "Failed to parse API response", "error": True}
        
        summary = data.get("choices", [{}])[0].get("message", {}).get("content", "")

        if not summary:
            logger.error("Empty response from Groq API")
            return {"summary": "AI returned empty response", "error": True}

        logger.info("✅ AI summary generated successfully")
        return {"summary": summary, "error": False}

    def _handle_error_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle an error API response."""
        error_text = response.text[:300]
        logger.error(f"Groq API Error: {response.status_code} - {error_text}")
        return {
            "summary": f"API Error ({response.status_code}): {error_text}",
            "error": True,
        }

    def _handle_exception(self, error: Exception) -> Dict[str, Any]:
        """Handle exceptions during API request."""
        error_msg = str(error)
        logger.error(f"Groq API failed: {error_msg}")
        return {"summary": f"AI generation failed: {error_msg}", "error": True}

    def generate_summary(
        self,
        problem_name: str,
        python_code: str,
        cpp_code: str,
        python_time_complexity: Optional[str] = None,
        python_space_complexity: Optional[str] = None,
        cpp_time_complexity: Optional[str] = None,
        cpp_space_complexity: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate AI summary comparing Python and C++ solutions."""
        if not self.api_key:
            return {
                "summary": "GROQ_API_KEY not configured. Please add to .env file.",
                "error": True,
            }

        prompt = self._build_prompt(
            problem_name,
            python_code,
            cpp_code,
            python_time_complexity,
            python_space_complexity,
            cpp_time_complexity,
            cpp_space_complexity,
            notes,
        )

        try:
            logger.info("Sending request to Groq API...")
            response = self._make_api_request(prompt)

            if response.status_code == 200:
                return self._handle_success_response(response)
            else:
                return self._handle_error_response(response)

        except httpx.TimeoutException:
            logger.error("Groq API timeout")
            return {"summary": "Request timed out. Please try again.", "error": True}
        except Exception as e:
            return self._handle_exception(e)