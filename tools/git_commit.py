from langchain.tools import tool
from typing import Optional
import subprocess
from agent import model
from agent.prompts import smart_commit_prompt

model = model.llm()

@tool
def commit(commit_message : str, repo_path : str = "."):
    """This function commits all the staged changes with custom commit message.
    Args : 
    1.commit_message (str): The message to be written in commit.
    2.repo_path (str): Path to the repository in local storage."""
    
    if not commit_message:
        return "Error : Commit message is required."
    
    try:
        ChildProcess = subprocess.run(
            args=['git', 'status', '--porcelain'],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )
        
        if not ChildProcess.stdout.strip():
            return "No changed to commit. First stag the changes."
        
        ChildProcess = subprocess.run(
            args=['git', 'commit', '-m', commit_message],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        return f"Successfully committed with message: '{commit_message}'"
    
    except subprocess.CalledProcessError as e:
        return f"Error : Error committing : {e.stderr}"
        
        
@tool
def smart_commit(repo_path : str = "."):
    """This function create a smart commit based on the stagged files.
    Args : 
    1.repo_path : Path of the local repository."""
    
    try:
        ChildProcess = subprocess.run(
            args=['git', 'diff', '--staged'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        code_diff = ChildProcess.stdout
        if not ChildProcess.stdout.strip():
            return "Error : No changes are staged. Stage the changes first."
        
        prompt = smart_commit_prompt.format(code_diff=code_diff)
        
        commit_message = model.invoke(prompt)
        
        ChildProcess = subprocess.run(
            args=['git', 'commit', '-m', commit_message.content],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        
        return f"Successfully Commited : Message -> {commit_message}"
    
    except subprocess.CalledProcessError as e:
        return f"Error : Failed Smart Commit : {e.stderr}"
    
    