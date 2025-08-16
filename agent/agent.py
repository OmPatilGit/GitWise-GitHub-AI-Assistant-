from tools.git_status import git_status
from tools.git_stag_changes import git_add
from tools.git_commit import smart_commit
from tools.git_branches import create_branch, git_checkout
from tools.git_pr_summarize import summarize_pr
from tools.git_summarize_commit import summarize_commits
from tools.git_summarize_blame import explain_code_change
from tools.git_fetch_pull import git_fetch, git_pull
from agent import model
from langgraph.graph import StateGraph,END
from langchain_core.messages import HumanMessage,ToolMessage, BaseMessage, SystemMessage
from typing import TypedDict, Annotated, List
from langchain_core.tools import tool
from agent.prompts import session_instructions

# Loading the LLM model
model = model.llm()

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
    instructions = state.get('instructions', "")
    message_with_prompt = []
    
    if instructions:
        message_with_prompt.append(SystemMessage(content=instructions))
        
    message_with_prompt.extend(state['messages'])
    response = model_with_tools.invoke(message_with_prompt)
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


# Wiring the graph
graph = StateGraph(state_schema=AgentState)

graph.add_node("model_call", model_call)
graph.add_node("tool_call", tool_call)

graph.set_entry_point('model_call')

graph.add_conditional_edges(
    source="model_call",
    path=should_continue,
    path_map={
        "CONTINUE" : "tool_call",
        "END" : END
    }
)
graph.add_edge('tool_call', 'model_call')

app = graph.compile()
