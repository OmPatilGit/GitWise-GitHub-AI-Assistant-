import subprocess
from agent import model 
from langchain_core.tools import tool


@tool
def git_fetch(repo_path: str = "."):
    """
    Fetches all new changes from the remote repository but does not merge them.
    Args :
    1.repo_path : The path of the repository
    """
    try:
        print("Fetching from remote...")
        subprocess.run(
            ["git", "fetch", "--prune"],
            cwd=repo_path, 
            capture_output=True, 
            text=True, 
            heck=True, 
            encoding='utf-8'
        )
        
        status_result = subprocess.run(
            ["git", "status", "-sb"],
            cwd=repo_path, 
            capture_output=True, 
            text=True, 
            check=True, 
            encoding='utf-8'
        )
        status_output = status_result.stdout.strip()
        
        if "[behind" in status_output:
            return f"Successfully fetched changes. Your branch is behind the remote."
        else:
            return "Successfully fetched. Your local branch is already up-to-date with the remote."

    except subprocess.CalledProcessError as e:
        return f"Error during fetch: {e.stderr}. Make sure you have a remote repository configured."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


@tool
def git_pull(repo_path: str = "."):
    """
    Fetches new changes from the remote repository and merges them into the current local branch.
    This will directly update your code. It may result in a merge conflict.
    """
    try:
        print("Pulling and merging changes from remote...")
        pull_result = subprocess.run(
            ["git", "pull", "--rebase", "--autostash"],
            cwd=repo_path, capture_output=True, text=True, check=True, encoding='utf-8'
        )
        
        if "up-to-date" in pull_result.stdout:
            return "Your branch is already up-to-date. No new changes were pulled."
        
        return f"Successfully pulled and merged changes from the remote repository.\nOutput:\n{pull_result.stdout}"

    except subprocess.CalledProcessError as e:
        if "conflict" in e.stderr.lower():
            return f"A merge conflict occurred during the pull. Please run the 'robust_conflict_resolver' tool to fix it."
        return f"Error during pull: {e.stderr}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

