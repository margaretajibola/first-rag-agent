import os

from langchain_core.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun

from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

import random

load_dotenv(override=True)

# web search tool
search_tool = DuckDuckGoSearchRun()
# results = search_tool.invoke("When is cherry blossom season in Japan?")
# print("-----------------------------------------------------------------------")
# print("🔍 Search Results:")
# print(results)
# print("-----------------------------------------------------------------------")


# weather info tool
def get_weather_info(location: str) -> str:
    """Fetches dummy weather information for a given location."""
    # Dummy weather data
    weather_conditions = [
        {"condition": "Rainy", "temp_c": 15},
        {"condition": "Clear", "temp_c": 25},
        {"condition": "Windy", "temp_c": 20}
    ]
    # Randomly select a weather condition
    data = random.choice(weather_conditions)
    return f"Weather in {location}: {data['condition']}, {data['temp_c']}°C"

# Initialize the tool
weather_info_tool = Tool(
    name="get_weather_info",
    func=get_weather_info,
    description="Fetches dummy weather information for a given location."
)

# chat = ChatOpenAI(
#     model="gpt-4o",
#     api_key=os.getenv("OPENAI_API_KEY"),
#     verbose=True,
# )

# tools = [search_tool, weather_info_tool]
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

# messages = [HumanMessage(content="What is the weather like in Tokyo?")]
# response = alfred_agent.invoke({"messages": messages})

# print("🎩 Alfred's Response:")
# print("-----------------------------------------------------------------------")
# print(response['messages'][-1].content)
# print("-----------------------------------------------------------------------")

