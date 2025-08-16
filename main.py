# main.py

from langchain_core.messages import HumanMessage
from rich.console import Console
from rich.markdown import Markdown

# Import your agent's graph
from agent.agent import app # Assuming your compiled app is here

def main():
    # 1. Create a Rich Console object
    console = Console()

    console.print(Markdown("# Welcome to GitWise AI! 🧠✨"))
    console.print("I'm here to help you with your Git and GitHub workflows.")
    console.print("Type '[bold red]exit[/bold red]' to quit.", markup=True)

    # The conversation loop
    while True:
        try:
            user_input = console.input("[bold cyan]You:[/bold cyan] ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                console.print("[bold yellow]Goodbye![/bold yellow]")
                break

            # 2. Use a spinner while the agent is working
            with console.status("[bold green]🧠 Agent is thinking...[/bold green]", spinner="dots"):
                # Create the initial state for the graph
                inputs = {"messages": [HumanMessage(content=user_input)]}
                
                # Invoke the graph to get the final result
                final_state = app.invoke(inputs)
                
                # The agent's final response is the last message
                final_message = final_state["messages"][-1]

            # 3. Print the final output using Markdown rendering
            console.print("[bold magenta]Agent:[/bold magenta]", end=" ")
            console.print(Markdown(final_message.content, style="default"))

        except KeyboardInterrupt:
            console.print("\n[bold yellow]Goodbye![/bold yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]An error occurred: {e}[/bold red]")

if __name__ == "__main__":
    main()
