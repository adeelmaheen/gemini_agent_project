# import os
# from dotenv import load_dotenv
# from typing import cast
# import chainlit as cl
# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
# from agents.run import RunConfig

# # Load the environment variables from the .env file
# load_dotenv()

# gemini_api_key = os.getenv("GEMINI_API_KEY")

# # Check if the API key is present; if not, raise an error
# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")


# @cl.on_chat_start
# async def start():
#     #Reference: https://ai.google.dev/gemini-api/docs/openai
#     external_client = AsyncOpenAI(
#         api_key=gemini_api_key,
#         base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
#     )

#     model = OpenAIChatCompletionsModel(
#         model="gemini-2.0-flash",
#         openai_client=external_client
#     )

#     config = RunConfig(
#         model=model,
#         model_provider=external_client,
#         tracing_disabled=True
#     )
#     """Set up the chat session when a user connects."""
#     # Initialize an empty chat history in the session.
#     cl.user_session.set("chat_history", [])

#     cl.user_session.set("config", config)
#     agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)
#     cl.user_session.set("agent", agent)

#     await cl.Message(content="Welcome to the Panaversity AI Assistant! How can I help you today?").send()

# @cl.on_message
# async def main(message: cl.Message):
#     """Process incoming messages and generate responses."""
#     # Send a thinking message
#     msg = cl.Message(content="Thinking...")
#     await msg.send()

#     agent: Agent = cast(Agent, cl.user_session.get("agent"))
#     config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

#     # Retrieve the chat history from the session.
#     history = cl.user_session.get("chat_history") or []
    
#     # Append the user's message to the history.
#     history.append({"role": "user", "content": message.content})
    

#     try:
#         print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
#         result = Runner.run_sync(starting_agent = agent,
#                     input=history,
#                     run_config=config)
        
#         response_content = result.final_output
        
#         # Update the thinking message with the actual response
#         msg.content = response_content
#         await msg.update()
    
#         # Update the session with the new history.
#         cl.user_session.set("chat_history", result.to_input_list())
        
#         # Optional: Log the interaction
#         print(f"User: {message.content}")
#         print(f"Assistant: {response_content}")
        
#     except Exception as e:
#         msg.content = f"Error: {str(e)}"
#         await msg.update()
#         print(f"Error: {str(e)}")

import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please add it to your .env file.")

@cl.on_chat_start
async def start():
    client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
    config = RunConfig(model=model, model_provider=client, tracing_disabled=True)

    agent = Agent(
        name="GeminiAgent",
        instructions="You are a helpful assistant. For current info, search the web and cite sources.",
        model=model,
        tools=[]  # We'll inject search results manually, no hosted tools
    )

    cl.user_session.set("agent", agent)
    cl.user_session.set("config", config)
    cl.user_session.set("history", [])
    await cl.Message(content="👋 Hello! Ask me anything. I can search the web if needed.").send()

async def perform_web_search(query: str):
    resp = await cl.tools.web.run({
        "search_query": [{"q": query, "recency": 7, "domains": None}]
    })
    # Return only first 3 results
    return resp.get("search_query", [])[:3]

@cl.on_message
async def on_message(msg: cl.Message):
    thinking = cl.Message(content="Thinking..."); await thinking.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))
    history = cl.user_session.get("history") or []
    history.append({"role": "user", "content": msg.content})

    # Basic check whether to search
    lc = msg.content.lower()
    needs_search = lc.startswith(("who", "what", "latest", "current", "search", "find", "news"))

    web_results = await perform_web_search(msg.content) if needs_search else []

    if web_results:
        snippets = "\n".join(f"- **{item.get('title','No title')}**: {item.get('snippet','')}" for item in web_results)
        history.append({"role": "system", "content": f"Web search results:\n{snippets}"})

    try:
        result = Runner.run_sync(starting_agent=agent, input=history, run_config=config)
        output = result.final_output

        if web_results:
            sources = "\n".join(f"- {item.get('title','No title')} — {item.get('link','')}" for item in web_results)
            thinking.content = f"{output}\n\n**📰 Sources:**\n{sources}"
        else:
            thinking.content = output

        await thinking.update()
        cl.user_session.set("history", result.to_input_list())
    except Exception as e:
        thinking.content = f"⚠️ Error: {e}"
        await thinking.update()
        print("Error:", e)


