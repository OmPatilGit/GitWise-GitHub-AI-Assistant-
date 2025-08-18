from langchain_core.messages import HumanMessage
from rich.console import Console
from rich.markdown import Markdown
from rich.spinner import Spinner
from agent.agent import app 

config = {"configurable" : {"thread_id" : 1}}
spinner = Spinner("dots",text="🧠 Agent is thinking...")
def main(): 
    
    console = Console()

    console.print(Markdown("# GitWise AI! 🧠✨"))
    console.print("I'm here to help you with your Git and GitHub workflows.")
    console.print("Type '[bold red]exit[/bold red]' to quit.", markup=True)

    while True:
        try:
            user_input = console.input("[bold cyan]You:[/bold cyan] ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                console.print("[bold yellow]Goodbye![/bold yellow]")
                break
            console.print(spinner, end="")
            inputs = {"messages": [HumanMessage(content=user_input)]}
            final_state = app.invoke(inputs, config=config)
            final_message = final_state["messages"][-1]
            console.print("\r", end="")   
            snapshot = app.get_state(config=config)
            last_message = snapshot.values['messages'][-1]
                
            if last_message.tool_calls:
                tool_call = last_message.tool_calls[0]
                tool_name = tool_call['name']
                tool_args = tool_call['args']
                    
                console.print(f"\n[bold yellow]Confirmation Required:[/bold yellow]")
                console.print(f"Agent wants to run: [bold green]{tool_name}[/bold green] \nwith arguments: [bold green]{tool_args}[/bold green]")
                    
                confirm = console.input("Confirm ['y'/'n'] : ")
                if confirm.strip().lower() == 'y':
                    with console.status("[bold green]⚙️ Executing...[/bold green]", spinner="dots"):
                        final_result = app.invoke(None, config)
                        final_message = final_result["messages"][-1]
                else:
                    console.print("[red]Command aborted by user.[/red]")
                    continue 
            else:
                final_message = last_message
                
            console.print("[bold magenta]Agent:[/bold magenta]", end=" ")
            console.print(Markdown(final_message.content, style="default"))

        except KeyboardInterrupt:
            console.print("[bold yellow]Goodbye![/bold yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]An error occurred: {e}[/bold red]")

if __name__ == "__main__":
    main()
