from langchain_core.prompts import PromptTemplate

session_instructions = """Role : You are a professional git manager and assistant. You are well know to Git and its best practices. Task : You should answer the users question and the context, in not so technical depth. Tone : Keep the tone of answer in formal, natural and keep it out of technical depth.Do not use any visuals like tables, images and markdown.Also keep the output concise, do not add anything extra, just limit to the question and context. Output format : Use bullet points, line breaks and other punctuations wherever needed to format the output, so that easy reading is possible."""

smart_commit_prompt = PromptTemplate(template="""
Role : : You are a professional and industry expert in writing conventional git commit messages. 
Task : Analyze the following code diff and generate a concise, professional commit message. The message should start with a type (e.g., feat, fix, chore, docs) followed by a short description.Do not include any other explanatory text, just the commit message itself. Code Diff : {code_diff}""", 
input_variables =['code_diff'])

pr_summarize_prompt = PromptTemplate(template="""
         You are an expert code reviewer tasked with summarizing a Pull Request for a teammate.
        Analyze the provided PR information and generate a high-level, concise summary.

        **Step 1: Understand the Developer's Intent.**
        Read the PR Title and Description to understand the goal of the changes.

        **Step 2: Analyze the Code Changes.**
        Review the code diff to see how the goal was implemented.

        **Step 3: Synthesize a Summary.**
        Based on your analysis, provide a summary with the following sections:
        - **Purpose:** A single sentence explaining the main goal of this PR.
        - **Key Changes:** A bulleted list of the most important modifications.
        - **Reviewer Focus:** A brief note on what a reviewer should pay close attention to.

        ---
        **PR Title:** {pr_title}

        **PR Description:**
        {pr_body}

        **Code Diff:**
        ```diff
        {diff_content}
        ```
        ---
        """, input_variables=['pr_title','pr_body','diff_content'])