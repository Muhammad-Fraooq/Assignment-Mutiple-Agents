import os
import asyncio
import chainlit as cl
from typing import cast
from openai import AsyncOpenAI
from agents.run import RunConfig
from dotenv import load_dotenv
from pydantic import BaseModel
from tools.roadmaps_data import career_roadmaps
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool,ModelProvider
from prompts.prompt import career_prompt, job_prompt,skill_prompt,triage_prompt

# Structured input models for handoffs
class CareerField(BaseModel):
    field: str

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = os.getenv("BASE_URL")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set in .env")

 # Gemini model provider
class GeminiModelProvider(ModelProvider):
    def __init__(self, api_key, model_name):
        super().__init__()
        self.api_key = api_key
        self.model_name = model_name
        self.client = AsyncOpenAI(
                api_key=api_key,
                base_url=BASE_URL
        )
    def get_model(self, model_name="gemini-2.0-flash"):
        return OpenAIChatCompletionsModel(
                model=self.model_name,
                openai_client=self.client
        )

model_provider = GeminiModelProvider(api_key=GEMINI_API_KEY,model_name="gemini-2.0-flash")

# Model config
config = RunConfig(model=model_provider.get_model(),model_provider=model_provider,tracing_disabled=True)

@cl.on_chat_start
async def start():
    # Define function tool for career roadmap
    @function_tool
    def get_career_roadmap(fields: CareerField):
        """Returns the key skills required for a given career field.
        Input:
        - field (str): The name of a career field (e.g., 'Frontend Developer', 'AI Engineer').
        Output:
        - A skill list relevant to that field or suggestions if the field is unknown.
        """
        field_name = fields.field.strip().lower()
        if field_name in career_roadmaps:
            return f"🧠 Skills for {field_name.title()}:\n{career_roadmaps[field_name]}"
        else:
            return (
                f"❌ I don’t have a roadmap for '{field_name}'. Try one of:\n- " +
                "\n- ".join([f.title() for f in career_roadmaps])
            )

    # Define specialist agents with improved prompts and handoff descriptions
    career_agent = Agent(
        name="Career Agent",
        instructions=career_prompt,
        model=model_provider.get_model(),
        tools=[get_career_roadmap],
        handoff_description="Expert in personalized career guidance and planning"
    )

    skill_agent = Agent(
        name="Skill Agent",
        instructions=skill_prompt,
        model=model_provider.get_model(),
        handoff_description="Skill-building expert offering learning roadmaps and tools"
    )

    job_agent = Agent(
        name="Job Agent",
        instructions=job_prompt,
        model=model_provider.get_model(),
        handoff_description="Delivers job market insights and actionable job-seeking advice"
    )

    triage_agent = Agent(
        name="Triage Agent",
        instructions=triage_prompt,
        model=model_provider.get_model(),
        handoffs=[career_agent, skill_agent, job_agent]
    )

    # Add triage agent to specialist agents' handoffs
    career_agent.handoffs.append(triage_agent)
    skill_agent.handoffs.append(triage_agent)
    job_agent.handoffs.append(triage_agent)

    # Store agents and config in session    
    cl.user_session.set("triage_agent", triage_agent)
    cl.user_session.set("config", config)
    cl.user_session.set("history", [])

    # Initialize Runner without agents parameter
    cl.user_session.set("runner", Runner())

    await cl.Message(content="""
## 👋 Welcome to Your Tech Career Assistant!

I'm your intelligent Career Mentor Agent — here to help you:
- 🎯 Explore the best career paths
- 🛠️ Build customized skill plans
- 💼 Navigate your job search with confidence

What would you like to get help with today?
""").send()


@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses with token streaming."""
    triage_agent = cast(Agent, cl.user_session.get("triage_agent"))
    config = cast(RunConfig, cl.user_session.get("config"))
    runner = cast(Runner, cl.user_session.get("runner"))
    history = cl.user_session.get("history") or []

    # Append user message to history
    history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="Thinking...")
    await msg.send()

    try:
        result = runner.run_streamed(triage_agent, history, config)
        full_response: str = ""

        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
                token = str(event.data.delta) # type: ignore
                if token:
                    full_response += token
                    msg.content = full_response
                    await msg.update()
                    await asyncio.sleep(0.05)   

        
        # Append assistant response to history
        history.append({"role": "assistant", "content": full_response})

        # Update session history
        cl.user_session.set("history", history)

    except Exception as e:
        print(f"Error: {str(e)}")  # Log error for debugging
        msg.content = f"⚠️ An error occurred: {str(e)}. Please try again."
        await msg.update()

