from langchain.tools import tool
from typing import Optional
import subprocess

@tool
def git_status(repo_path : str = ".") -> str:
    """Checks the status of given repository.
    Args : 
    1.Repository Path (str): The Path of the repository."""
    
    try:
        ChildProcess = subprocess.run(
            args=['git', 'status'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return ChildProcess.stdout 
    
    except FileNotFoundError:
        return f"Error : Git is not installed, or not added in your PATH."
    
    except subprocess.CalledProcessError as e:
        return f"Error : Error checking repo status : {e.stderr}"
    

