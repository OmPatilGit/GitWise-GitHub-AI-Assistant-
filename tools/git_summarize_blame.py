import subprocess
from agent import model 
from langchain_core.tools import tool
from agent.prompts import blame_summarize_prompt


@tool
def explain_code_change(file_path: str, line_number: int, repo_path: str = "."):
    """
    Finds who last modified a specific line of code and summarizes the purpose of their change.
    Args :
    1. file_path : Path of the file which is to be searched for the code
    2. line_number : The number of line in file_path to check for explaination
    """
    try:
        ChildProcess = [
            "git", "blame", f"-L{line_number},{line_number}", "--porcelain", file_path
        ]
        blame_result = subprocess.run(
            args=ChildProcess, 
            cwd=repo_path, 
            capture_output=True, 
            text=True, 
            check=True
            )
        
        commit_hash = blame_result.stdout.split(' ')[0]

        show_command = ["git", "show", commit_hash]
        commit_details = subprocess.run(
            args=show_command, 
            cwd=repo_path, 
            capture_output=True, 
            text=True, 
            check=True
            ).stdout

        prompt = blame_summarize_prompt.format(commit_details=commit_details)
        llm = model.llm()
        explanation = llm.invoke(prompt).content.strip()
        return explanation

    except Exception as e:
        return f"Could not analyze the code change: {str(e)}"