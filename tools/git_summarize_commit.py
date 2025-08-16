import subprocess
from agent import model 
from langchain_core.tools import tool
from agent.prompts import commit_summarize_prompt

@tool
def summarize_commits(commit_count: int = 3, repo_path: str = "."):
    """
    Fetches and summarizes the most recent Git commit messages to provide a high-level
    overview of project activity.
    Args:
    1. commit_count (int): The number of recent commits to analyze. Defaults to 10.
    """
    try:
        log_format = "--pretty=format:%h | %an | %ar%n%B%n---COMMIT-SEPARATOR---"
        
        log_command = [
            "git", "log", f"-n{commit_count}", log_format
        ]
        
        print(f"Fetching the last {commit_count} commits...")
        commit_log_result = subprocess.run(
            args=log_command,
            cwd=repo_path, 
            capture_output=True, 
            text=True, 
            check=True, 
            encoding='utf-8'
        )
        
        raw_commit_logs = commit_log_result.stdout.strip()

        if not raw_commit_logs:
            return "There are no commits in this repository to summarize."

        # --- Step 2: The AI Analyst ---
        # We create a detailed prompt to guide the LLM's analysis.
        prompt = commit_summarize_prompt.format(raw_commit_logs=raw_commit_logs)
        
        llm = model.llm()
        summary = llm.invoke(prompt).content.strip()

        return f"Here is a summary of the last {commit_count} commits:\n\n{summary}"

    except subprocess.CalledProcessError as e:
        return f"Error fetching git log: {e.stderr}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

