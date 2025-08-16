from langchain_core.messages import HumanMessage
from rich.console import Console
from rich.markdown import Markdown
from agent.agent import app 

def main():
    
    console = Console()

    console.print(Markdown("# Welcome to GitWise AI! 🧠✨"))
    console.print("I'm here to help you with your Git and GitHub workflows.")
    console.print("Type '[bold red]exit[/bold red]' to quit.", markup=True)

    while True:
        try:
            user_input = console.input("[bold cyan]You:[/bold cyan] ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                console.print("[bold yellow]Goodbye![/bold yellow]")
                break

        
            with console.status("[bold green]🧠 Agent is thinking...[/bold green]", spinner="dots"):
                
                inputs = {"messages": [HumanMessage(content=user_input)]}
                final_state = app.invoke(inputs)
                final_message = final_state["messages"][-1]

            console.print("[bold magenta]Agent:[/bold magenta]", end=" ")
            console.print(Markdown(final_message.content, style="default"))

        except KeyboardInterrupt:
            console.print("[bold yellow]Goodbye![/bold yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]An error occurred: {e}[/bold red]")

if __name__ == "__main__":
    main()
