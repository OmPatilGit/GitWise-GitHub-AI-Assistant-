from langchain.tools import tool
from typing import Optional
import subprocess

@tool
def create_branch(branch_name : str, repo_path : str):
    """This function creates a branch with user specified branch names.
    Args : 
    1.branch_name : name of the branch.
    2.repo_path : path of the local rep."""
    
    if not branch_name:
        return "Error : No branch name specified."
    
    try:
        ChildProcess = subprocess.run(
            args=['git', 'branch', branch_name],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        return f"Created branch : {branch_name}"
    
    except subprocess.CalledProcessError as e:
        return f"Error : Could not create branch {e.stderr}"
    
    
@tool
def git_checkout(branch_name: str, repo_path: str = "."):
    """Switches to an existing Git branch."""
    if not branch_name:
        return "Error: Please provide the name of the branch to switch to."
    try:
        subprocess.run(
            ["git", "checkout", branch_name],
            cwd=repo_path, capture_output=True, text=True, check=True
        )
        return f"Successfully switched to branch: '{branch_name}'."
    except subprocess.CalledProcessError as e:
        return f"Error switching branch: {e.stderr}"