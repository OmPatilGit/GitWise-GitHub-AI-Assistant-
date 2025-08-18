from tools.git_status import git_status
from tools.git_stag_changes import git_add
from tools.git_commit import smart_commit
from tools.git_branches import create_branch, git_checkout
from tools.git_pr_summarize import summarize_pr
from tools.git_summarize_commit import summarize_commits
from tools.git_summarize_blame import explain_code_change
from tools.git_fetch_pull import git_fetch, git_pull
from agent import model
from langgraph.graph import StateGraph,END, START
from langchain_core.messages import HumanMessage,ToolMessage, BaseMessage, SystemMessage
from typing import TypedDict, Annotated, List, Optional
from langchain_core.tools import tool
from agent.prompts import session_instructions
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from rich.console import Console
console = Console()

# Loading the LLM model
model = model.llm()

# # Checkpointer for the chat
# memory = MemorySaver()
# Thread for the chat
config = {"configurable" : {"thread_id" : 1}}
sqlite_conn = sqlite3.connect("checkpoint.sqlite", check_same_thread=False)
memory = SqliteSaver(sqlite_conn)


# StageGraph of the agent
class AgentState(TypedDict):
    messages : Annotated[List[BaseMessage], lambda x,y : x+y]
    
tools = [git_add, git_status, 
         smart_commit, 
         create_branch, 
         git_checkout, 
         summarize_pr,
         summarize_commits,
         explain_code_change,
         git_fetch,
         git_pull]

model_with_tools = model.bind_tools(tools=tools)


# Deciding the graph and nodes
# Checking the conditional Edge
def should_continue(state: AgentState):
    """This function provides the conditional edge, whether to continue or end converstaion.
    Args :
    1.state : The current state of the agent."""
    last_message = state['messages'][-1]
    if not last_message.tool_calls:
        return "END"
    else:
        return "CONTINUE"
    
    
# Calling the model
def model_call(state: AgentState):
    """Invokes the model with the current state.
    Args :
    1.state : The current state of the agent"""
    message_with_prompt = []
    
    if session_instructions:
        message_with_prompt.append(SystemMessage(content=session_instructions))
        
    message_with_prompt.extend(state['messages'])
    response = model_with_tools.invoke(message_with_prompt, config=config)
    return {"messages": [response]}

# Calling the tool
def tool_call(state: AgentState):
    """Executes the tool chosen by the model.
    Args :
    1.state : Current State of the agent"""
    last_message = state['messages'][-1]
    
    if not last_message.tool_calls:
        return {"messages": []}
        
    action = last_message.tool_calls[0]
    
    tool_to_call = next((t for t in tools if t.name == action["name"]), None)
    if tool_to_call is None:
        raise ValueError(f"Tool '{action['name']}' not found.")
    
    result = tool_to_call.invoke(action.get("args", {}))
    
    tool_message = ToolMessage(content=str(result), tool_call_id=action["id"])
    
    return {"messages": [tool_message]}

# # Check if the model is calling a tool and guide
# def after_model_router(state : AgentState):
#     last_message = state["messages"][-1]
#     if not last_message.tool_calls:
#         return "END"
#     return "CONTINUE"

# # Asking the user for the consent and route accordingly 
# def human_consent_router(state : AgentState):
#     last_message = state["messages"][-1]
#     if not last_message.tool_calls:
#         return {"human_consent": False}
#     tool_called = last_message.tool_calls[0]
#     tool_name = tool_called['name']
#     tool_args = tool_called['args']
    
#     console.print(f"\n[bold yellow]Confirmation Required:[/bold yellow]")
#     console.print(f"Agent wants to run: [bold green]{tool_name}[/bold green] with arguments: [bold green]{tool_args}[/bold green]")
    
#     # This is the blocking input() call inside the graph
#     confirm = console.input("Proceed? (y/n): ")

#     if confirm.lower() == 'y':
#         return {"human_feedback": True}
#     else:
#         # If user says no, we add a message to the history and set consent to False
#         aborted_message = HumanMessage(content="User aborted the command.")
#         return {"messages": [aborted_message], "human_feedback": False}

# # Checking for consent of user and guide accordingly 
# def after_consent_router(state : AgentState):
#     consent = state["human_feedback"]
#     if consent:
#         return "CONTINUE"
#     return "END"

# Wiring the graph
graph = StateGraph(state_schema=AgentState)
graph.add_node("model", model_call)
graph.add_edge(START, "model")
graph.add_node("tool", tool_call)
graph.add_conditional_edges(
    source="model",
    path=should_continue,
    path_map={
        "CONTINUE" : "tool",
        "END" : END
    }
)
graph.add_edge("tool", "model")
# app = graph.compile(checkpointer=memory, interrupt_before=['human_feedback'])
app = graph.compile(checkpointer=memory, interrupt_before=['tool'])
