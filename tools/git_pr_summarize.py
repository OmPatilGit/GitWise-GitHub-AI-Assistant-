from langchain.tools import tool
from typing import Optional
import subprocess
from agent import model
from agent.prompts import pr_summarize_prompt
import json

llm = model.llm()
@tool
def summarize_pr(pr_url: str, repo_path: str = "."):
    """
    Analyzes the changes in a GitHub Pull Request and provides a concise summary.
    The input should be the full URL of the pull request.
    """
    if not pr_url:
        return "Error: Please provide the URL of the Pull Request to summarize."

    try:
        print(f"Fetching metadata for PR: {pr_url}...")
        pr_metadata_result = subprocess.run(
            [
                "gh", "pr", "view", pr_url,
                "--json", "title,body"
            ],
            cwd=repo_path, 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        pr_data = json.loads(pr_metadata_result.stdout)
        pr_title = pr_data.get("title", "")
        pr_body = pr_data.get("body", "No description provided.")

    
        print(f"Fetching diff for PR: {pr_url}...")
        diff_result = subprocess.run(
            ["gh", "pr", "diff", pr_url],
            cwd=repo_path, 
            capture_output=True, 
            text=True, 
            check=True
        )
        diff_content = diff_result.stdout

        if not diff_content:
            return "Could not retrieve changes for the PR. It might be empty or already merged."

        # --- UPGRADED PROMPT ---
        # This prompt provides much more context and structure for the LLM.
        prompt = pr_summarize_prompt.format(pr_title=pr_title, pr_body=pr_body, diff_content=diff_content)
        summary = llm.invoke(prompt).content.strip()

        return summary

    except FileNotFoundError:
        return "Error: GitHub CLI ('gh') not found. Please install it and authenticate with 'gh auth login'."
    except subprocess.CalledProcessError as e:
        return f"Error processing PR: {e.stderr}. Ensure the URL is correct, the PR exists, and you have access."
    except json.JSONDecodeError:
        return "Error: Could not parse PR metadata from GitHub CLI."
