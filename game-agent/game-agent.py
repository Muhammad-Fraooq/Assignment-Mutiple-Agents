import os
import asyncio
import chainlit as cl
from typing import cast
from openai import AsyncOpenAI
from agents.run import RunConfig
from dotenv import load_dotenv
import random
from agents import Agent, Runner, OpenAIChatCompletionsModel,ModelProvider,function_tool
from prompts.prompts import narrator_prompt,monstor_prompt,item_prompt,traige_prompt

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = os.getenv("BASE_URL")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set in .env")

# Start chainlit app
@cl.on_chat_start
async def on_chat_start():

     # Reference: https://ai.google.dev/gemini-api/docs/openai
    external_client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url=BASE_URL,
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash", openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client, # type: ignore
        tracing_disabled=True 
    )

    @function_tool
    def roll_dice(sides: int = 6) -> int:
        """Roll a dice with the specified number of sides (e.g., d6, d20)."""
        return random.randint(1, sides)

    @function_tool
    def generate_event(description: str) -> str:
        """Generate a random event based on the description prompt."""
        events = [
            "You find a hidden treasure!",
            "A wild beast appears!",
            "You encounter a mysterious stranger.",
            "A storm brews on the horizon.",
            "You hear whispering voices in the dark.",
            "You step on a pressure plate – something clicks...",
            "A merchant waves at you from the distance.",
            "You discover a crumbling map stuck under a rock."
        ]
        return random.choice(events)
        
    # Create the expert agents
    narrator_agent = Agent(
        name="Narrator Agent",
        instructions=narrator_prompt,
        handoff_description="Narrates story scenes and drives game progress",
        model=model,
        tools=[roll_dice, generate_event]
    )

    monster_agent = Agent(
    name="Monster Agent",
    instructions=monstor_prompt,
    handoff_description="Handles combat encounters and enemy logic",
    model=model,
)

    item_agent = Agent(
    name="Item Agent",
    instructions=item_prompt,
    handoff_description="Manages rewards and player inventory",
    model=model,
)

    # Create the main game agent
    triage_agent = Agent(
    name="Triage Game Assistant",
    instructions=traige_prompt,
    model=model,
    handoffs=[narrator_agent, monster_agent, item_agent]
)

    narrator_agent.handoffs.append(triage_agent)
    monster_agent.handoffs.append(triage_agent)
    item_agent.handoffs.append(triage_agent)

    cl.user_session.set("triage_agent", triage_agent)
    cl.user_session.set("config", config)
    cl.user_session.set("history",[])

    # Initialize the runner
    cl.user_session.set("runner", Runner())

    await cl.Message(
    content="🧙‍♂️ **The Enchanted Companion** — Your Guide Through Realms of Magic and Danger\n\nWelcome to the game! You can start by typing your first command."
).send()

    
@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming messages and route them to the appropriate agent with streaming."""

    triage_agent = cast(Agent,cl.user_session.get("triage_agent"))
    config = cast(RunConfig,cl.user_session.get("config"))
    runner = cast(Runner,cl.user_session.get("runner"))
    history = cl.user_session.get("history") or []

    # Add the user message to the history
    history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="Thinking...")
    await msg.send()

    # Run the agent with streaming
    try:
        result = runner.run_streamed(triage_agent,history,config)

        full_response: str = ""

        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data,"delta"):
                token = cast(str, event.data.delta) # type: ignore
                if token:
                    full_response += token
                    msg.content = full_response
                    await msg.update()
                    await asyncio.sleep(0.10) 

        # update the history with the full response
        history.append({"role": "assistant", "content": full_response})

        # Update the user session with the new history
        cl.user_session.set("history", history)

    except Exception as e:
        msg.content = f"Error: {str(e)} \nPlease try again."
        await msg.update()