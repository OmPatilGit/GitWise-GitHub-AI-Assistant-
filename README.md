**GitWise AI** 🧠✨ Your intelligent command-line partner for seamless Git & GitHub workflows.

GitWise is a **terminal-based AI agent** that understands **natural language**, allowing you to manage complex Git operations, enforce best practices, and resolve common frustrations like **merge conflicts** with ease. **Stop memorizing commands** and start having a conversation with your repository.

## Features :

- Natural Language Commands
- Smart Commits & PRs
- AI-Powered Merge Conflict Resolver
- Instant Summaries
- Extensible Toolset    

## Installation

### 1.Prerequisite 

- Get up and running with GitWise in a few simple steps.
- Python **3.9+**
- **Git** installed on your system.
- **GitHub CLI** installed and authenticated `(gh auth login)`.
- **UV** Package Manager installed.
    
### 2. Clone the repository 

Repo : `https://github.com/OmPatilGit/GitHub.git`

Dir : `cd GitHub`

### 3. Virtual Environments

Virtual Environment : `uv venv`

Windows (PS)  : `.venv\Scripts\Activate.ps1`

Windows (CMD) : `.venv\Scripts\activate.bat`

### 4. Install Dependencies 

Dependencies : `uv pip install -r pyproject.toml`




### 5. Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`OPENAI_API_KEY="your-open-router-api-key"`

`URL="open-router-base-url"`


### 6.Usage 

Run the file using `uv run main.py`


# Working and Undertakes:

## GitWise is built on a powerful, modern AI stack:

LangChain & LangGraph: The core of the agent is a state machine built with LangGraph. This allows for complex, multi-step reasoning. The agent can call tools, analyze the output, and decide on the next best action in a continuous loop.

Tool-Based Architecture: Every Git or GitHub command is a "tool" that the agent can choose to use. This makes the system highly modular and easy to extend with new capabilities.

LLM-Powered Reasoning: A Large Language Model (like **GPT-OSS-20B**) acts as the "brain," interpreting user requests, selecting the right tools, and generating human-readable summaries and code resolutions.

The flow is a simple but powerful "Think → Act → Observe" loop, managed entirely by the graph.


## Future Takes
- Project Roadmap
This is just the beginning. Here's what's planned for the future:

- Phase 2: Full GitHub Integration. Create and manage PRs directly from the agent.List, view, and comment on issues.

- Phase 3: Enhanced User Experience. Integrate the rich library for beautiful terminal outputs (colors, spinners, tables).Implement a full Text User Interface (TUI) with textual.

- Phase 4: Advanced Git Operations. AI-assisted interactive rebase (git rebase -i).`"Git archaeology"` tool to find when a specific line of code was introduced (git blame on steroids).

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

- Fork the Project

- Create your Feature Branch (git checkout -b feature/AmazingFeature)

- Commit your Changes (git commit -m 'feat: Add some AmazingFeature')

- Push to the Branch (git push origin feature/AmazingFeature)

- Open a Pull Request


## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
