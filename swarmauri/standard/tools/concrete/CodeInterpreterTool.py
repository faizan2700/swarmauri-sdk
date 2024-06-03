import sys
import io
from dataclasses import dataclass, field
from typing import List
from swarmauri.standard.tools.base.ToolBase import ToolBase 
from swarmauri.standard.tools.concrete.Parameter import Parameter 

@dataclass
class CodeInterpreterTool(ToolBase):
    version: str = "1.0.0"
    parameters: List[Parameter] = field(default_factory=lambda: [
            Parameter(
                name="user_code",
                type="string",
                description=("Executes the provided Python code snippet in a secure sandbox environment. "
                             "This tool is designed to interpret the execution of the python code snippet."
                             "Returns the output"),
                required=True
            )
        ])
    description: str = "Executes provided Python code and captures its output."
    


    def __call__(self, user_code: str) -> str:
        """
        Executes the provided user code and captures its stdout output.
        
        Parameters:
            user_code (str): Python code to be executed.
        
        Returns:
            str: Captured output or error message from the executed code.
        """
        return self.execute_code(user_code)
    
    def execute_code(self, user_code: str) -> str:
        """
        Executes the provided user code and captures its stdout output.

        Args:
            user_code (str): Python code to be executed.

        Returns:
            str: Captured output or error message from the executed code.
        """
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()

        try:
            # Note: Consider security implications of using 'exec'
            builtins = globals().copy()
            exec(user_code, builtins)
            sys.stdout = old_stdout
            captured_output = redirected_output.getvalue()
            return str(captured_output)
        except Exception as e:
            sys.stdout = old_stdout
            return f"An error occurred: {str(e)}"