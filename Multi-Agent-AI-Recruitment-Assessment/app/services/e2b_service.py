import os
from typing import Any

from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

load_dotenv()


class E2BSandboxService:
    """
    Executes candidate code inside an isolated E2B sandbox.
    """

    def __init__(self):
        self.api_key = os.getenv("E2B_API_KEY")

        if not self.api_key:
            raise RuntimeError("E2B_API_KEY is not configured.")

    def execute_python(
        self,
        code: str,
        test_cases: list[dict[str, Any]],
    ) -> dict[str, Any]:

        results = []
        passed = 0
        failed = 0

        try:
            with Sandbox() as sandbox:

                for index, test_case in enumerate(test_cases, start=1):

                    test_input = test_case.get("input", "")
                    expected_output = str(test_case.get("expected_output", ""))

                    execution_code = f"""
{code}

print("__TEST_RESULT__")
try:
    result = solve({test_input})
    print(result)
except Exception as e:
    print("__TEST_ERROR__")
    print(str(e))
"""

                    execution = sandbox.run_code(execution_code)

                    output = execution.text or ""

                    if "__TEST_ERROR__" in output:
                        failed += 1

                        results.append(
                            {
                                "test_case": index,
                                "status": "failed",
                                "input": test_input,
                                "expected": expected_output,
                                "actual": output,
                                "error": output,
                            }
                        )

                        continue

                    actual_output = output.split(
                        "__TEST_RESULT__",
                        1
                    )[-1].strip()

                    if actual_output == expected_output:
                        passed += 1
                        status = "passed"
                    else:
                        failed += 1
                        status = "failed"

                    results.append(
                        {
                            "test_case": index,
                            "status": status,
                            "input": test_input,
                            "expected": expected_output,
                            "actual": actual_output,
                        }
                    )

            total = len(test_cases)

            score = (
                round((passed / total) * 100, 2)
                if total
                else 0
            )

            return {
                "success": True,
                "passed": passed,
                "failed": failed,
                "total": total,
                "score": score,
                "results": results,
            }

        except Exception as exc:

            return {
                "success": False,
                "passed": passed,
                "failed": failed,
                "total": len(test_cases),
                "score": 0,
                "results": results,
                "error": str(exc),
            }