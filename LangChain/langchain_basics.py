# pip install -qU langchain "langchain[openai]"
# from langchain.agents import create_agent

# def get_weather(city: str) -> str:
#     """Get weather for a given city."""
#     return f"It's always sunny in {city}!"

# agent = create_agent(
#     model="openai:gpt-5.5",
#     tools=[get_weather],
#     system_prompt="You are a helpful assistant",
# )

# result = agent.invoke(
#     {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
# )
# print(result["messages"][-1].content_blocks)

# xAI offers an API to interact with Grok models. 
# This example goes over how to use LangChain to interact with xAI models.

# Querying chat models with xAI
# pip install -U langchain-xai
# from langchain_xai import ChatXAI
# from dotenv import load_dotenv
# import os

# load_dotenv()

# chat = ChatXAI(
#     xai_api_key=os.environ["GROQ_API_KEY"],
#     model="grok-4",
# )

# # stream the response back from the model
# stream = chat.stream_events("Tell me fun things to do in Hyderabad", version="v3")
# for token in stream.text:
#     print(token, end="", flush=True)

# # if you don't want to do streaming, you can use the invoke method
# # chat.invoke("Tell me fun things to do in NYC")

# pip install -qU langchain langchain-openrouter
import pprint
from dotenv import load_dotenv
import urllib.error
import urllib.request
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

QUESTION = "What's the weather in San Francisco?"

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


def build_agent():
    """Shared agent setup — same brain, tools, and prompt for both demos."""
    return create_agent(
        model="openrouter:openrouter/free",
        tools=[get_weather],
        system_prompt="You are a helpful assistant",
    )


def invoke_agent() -> None:
    """Waits for the full agent run, then prints the final answer in one go."""
    agent = build_agent()

    result = agent.invoke({"messages": [{"role": "user", "content": QUESTION}]})
    pprint.pprint(result)
    print(result["messages"][-1].content_blocks)


def stream_agent() -> None:
    """Prints tokens as the model generates them — you see output while it runs."""
    agent = build_agent()

    stream = agent.stream_events(
        {"messages": [{"role": "user", "content": QUESTION}]},
        version="v3",
    )

    for message in stream.messages:
        for token in message.text:
            print(token, end="", flush=True)

    print()

def real_worlds_example():
    SYSTEM_PROMPT = """You are a literary data assistant.

                    ## Capabilities

                    - `fetch_text_from_url`: loads document text from a URL into the conversation.
                    Do not guess line counts or positions—ground them in tool results from the saved file.
                    
                    Read the first 50 lines only from any file."""

    @tool
    def fetch_text_from_url(url: str) -> str:
        """Fetch the document from a URL.
        """
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; quickstart-research/1.0)"},
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                raw = resp.read()
        except urllib.error.URLError as e:
            return f"Fetch failed: {e}"
        text = raw.decode("utf-8", errors="replace")
        return text

    model = init_chat_model(
        "openrouter:openrouter/free",
        temperature=0.5,
        timeout=100,
        max_tokens=2500,
    )

    checkpointer = InMemorySaver()

    agent = create_agent(
        model=model,
        tools=[fetch_text_from_url],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )

    content = f"""Project Gutenberg hosts a full plain-text copy of F. Scott Fitzgerald's The Great Gatsby.
                URL: https://www.gutenberg.org/files/64317/64317-0.txt

                Answer as much as you can:

                1) How many lines in the complete Gutenberg file contain the substring `Gatsby` (count lines, not occurrences within a line, each line ends with a line break).
                2) The 1-based line number of the first line in the file that contains `Daisy`.
                3) A two-sentence neutral synopsis.

                Do your best on (1) and (2). If at any point you realize you cannot **verify** an exact answer with
                your available tools and reasoning, do not fabricate numbers: use `null` for that field and spell out
                the limitation in `how_you_computed_counts`. If you encounter any errors please report what the error was and what the error message was."""

    agent_result = agent.invoke(
        {"messages": [{"role": "user", "content": content}]},
        config={"configurable": {"thread_id": "great-gatsby-lc"}},
    )

    print(agent_result["messages"][-1].content_blocks)

if __name__ == "__main__":
    # print("=== invoke (all at once) ===")
    # invoke_agent()

    # print("\n=== stream (token by token) ===")
    # stream_agent()

    real_worlds_example()


# Output for line number 76.
# {
#   "messages": [
#     {
#       "type": "HumanMessage",
#       "id": "af0823a7-1e4e-40f4-adae-12ce351d88b3",
#       "content": "What's the weather in San Francisco?",
#       "additional_kwargs": {},
#       "response_metadata": {}
#     },
#     {
#       "type": "AIMessage",
#       "id": "lc_run--019f8e1c-a7b0-7221-8f5e-ef3411f1060b-0",
#       "content": "",
#       "additional_kwargs": {
#         "reasoning_content": "Okay, the user is asking about the weather in San Francisco. Let me check the tools available. There's a function called get_weather that takes a city parameter. Since the user provided the city name, I should call that function. I need to make sure the argument is correctly formatted as a JSON object with the city key. No other parameters are needed here. Just pass \"San Francisco\" as the city value. Let me structure the tool call accordingly.\n",
#         "reasoning_details": [
#           {
#             "type": "reasoning.text",
#             "format": "unknown",
#             "index": 0,
#             "text": "Okay, the user is asking about the weather in San Francisco. Let me check the tools available. There's a function called get_weather that takes a city parameter. Since the user provided the city name, I should call that function. I need to make sure the argument is correctly formatted as a JSON object with the city key. No other parameters are needed here. Just pass \"San Francisco\" as the city value. Let me structure the tool call accordingly.\n"
#           }
#         ]
#       },
#       "response_metadata": {
#         "model_name": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
#         "id": "gen-1784795671-OQWOOzYcNnhVRnvQKzoE",
#         "created": 1784795671,
#         "object": "chat.completion",
#         "finish_reason": "tool_calls",
#         "logprobs": null,
#         "model_provider": "openrouter",
#         "cost": 0.0,
#         "cost_details": {
#           "upstream_inference_completions_cost": 0.0,
#           "upstream_inference_prompt_cost": 0.0,
#           "upstream_inference_cost": 0.0
#         }
#       },
#       "tool_calls": [
#         {
#           "id": "call-36aa1be7-90cd-4898-9ece-79a79ecade54",
#           "type": "tool_call",
#           "name": "get_weather",
#           "args": {
#             "city": "San Francisco"
#           }
#         }
#       ],
#       "invalid_tool_calls": [],
#       "usage_metadata": {
#         "input_tokens": 282,
#         "output_tokens": 119,
#         "total_tokens": 401,
#         "input_token_details": {
#           "cache_read": 0,
#           "cache_creation": 0
#         },
#         "output_token_details": {
#           "reasoning": 113
#         }
#       }
#     },
#     {
#       "type": "ToolMessage",
#       "id": "361abec7-25bd-4627-bf99-2263a58ea9e4",
#       "tool_call_id": "call-36aa1be7-90cd-4898-9ece-79a79ecade54",
#       "name": "get_weather",
#       "content": "It's always sunny in San Francisco!"
#     },
#     {
#       "type": "AIMessage",
#       "id": "lc_run--019f8e1c-af29-7f12-9bdb-bb46de418070-0",
#       "content": "It's always sunny in San Francisco!",
#       "additional_kwargs": {},
#       "response_metadata": {
#         "model_name": "google/gemma-4-26b-a4b-it:free",
#         "id": "gen-1784795672-MSr9nGQeMqZpBPnCd0FC",
#         "created": 1784795672,
#         "object": "chat.completion",
#         "finish_reason": "stop",
#         "logprobs": null,
#         "model_provider": "openrouter",
#         "cost": 0.0,
#         "cost_details": {
#           "upstream_inference_completions_cost": 0.00000231,
#           "upstream_inference_prompt_cost": 0.00000624,
#           "upstream_inference_cost": 0.00000855
#         }
#       },
#       "tool_calls": [],
#       "invalid_tool_calls": [],
#       "usage_metadata": {
#         "input_tokens": 208,
#         "output_tokens": 14,
#         "total_tokens": 222,
#         "input_token_details": {
#           "cache_read": 0,
#           "cache_creation": 0
#         },
#         "output_token_details": {
#           "reasoning": 0
#         }
#       }
#     }
#   ]
# }