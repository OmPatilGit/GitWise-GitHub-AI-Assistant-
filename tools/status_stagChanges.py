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
    
# @tool
def git_add(repo_path : str = ".", file_to_stag : str = ".") -> str:
    """Stags the changes to the staging area for the specifies repository.
    Args :
    1.Repository Path (str) : The path of the repository.
    2.file_to_stag (str) : The files to stag -> "." for staging all files """ 
    
    try:
        ChildProcess = subprocess.run(
            args=['git', 'add', str(repo_path)],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return ChildProcess.stdout
    
    except FileNotFoundError:
        return f"Error : Git is not installed, or not added in your PATH."
    
    except subprocess.CalledProcessError as e:
        return f"Error : Error staging files : {e.stderr}"   

result = git_add()

print(result)