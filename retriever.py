import os
import datasets
from langchain_core.documents import Document

from langchain_community.retrievers import BM25Retriever
from langchain_core.tools import Tool

from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv(override=True)

# Load the dataset
guest_dataset = datasets.load_dataset("agents-course/unit3-invitees", split="train")

# Convert dataset entries into Document objects
docs = [
    Document(
        page_content="\n".join([
            f"Name: {guest_dataset['name'][i]}",
            f"Relation: {guest_dataset['relation'][i]}",
            f"Description: {guest_dataset['description'][i]}",
            f"Email: {guest_dataset['email'][i]}"
        ]),
        metadata={"name": guest_dataset['name'][i]}
    )
    for i in range(len(guest_dataset))
]

bm25_retriever = BM25Retriever.from_documents(docs)

def extract_text(query: str) -> str:
    """Retrieves detailed information about gala guests based on their name or relation."""
    results = bm25_retriever.invoke(query)
    if results:
        return "\n\n".join([doc.page_content for doc in results[:3]])
    else:
        return "No matching guest information found."

guest_info_tool = Tool(
    name="guest_info_retriever",
    func=extract_text,
    description="Retrieves detailed information about gala guests based on their name or relation."
)

# chat = ChatOpenAI(
#     model="gpt-4o",
#     api_key=os.getenv("OPENAI_API_KEY"),
#     verbose=True,
# )

# tools = [guest_info_tool]
# chat_with_tools = chat.bind_tools(tools)


# # Generate the AgentState and Agent graph
# class AgentState(TypedDict):
#     messages: Annotated[list[AnyMessage], add_messages]

# def assistant(state: AgentState):
#     return {
#         "messages": [chat_with_tools.invoke(state["messages"])],
#     }

# ## The graph
# builder = StateGraph(AgentState)

# # Define nodes: these do the work
# builder.add_node("assistant", assistant)
# builder.add_node("tools", ToolNode(tools))

# # Define edges: these determine how the control flow moves
# builder.add_edge(START, "assistant")
# builder.add_conditional_edges("assistant", tools_condition)
# builder.add_edge(
#     "tools",
#     "assistant"
# )

# alfred_agent = builder.compile()

# messages = [HumanMessage(content="Tell me about our guest named 'Lady Ada Lovelace'.")]
# response = alfred_agent.invoke({"messages": messages})

# print("🎩 Alfred's Response:")
# print(response['messages'][-1].content)


