import os
import asyncio
import chainlit as cl
from typing import cast
from openai import AsyncOpenAI
from agents.run import RunConfig
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel,ModelProvider,function_tool
from prompts.prompts import destination_prompt, booking_prompt,explore_prompt,triage_prompt

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

# Start chainlit app
@cl.on_chat_start
async def start():

    @function_tool
    def get_flights(flight: str) -> dict:
        """
        Returns mock flight options based on a route input string like 'Karachi to Lahore'.
        """
        mock_flights = {
            "Karachi to Lahore": [
                {"flight": "PK301", "airline": "PIA", "departure": "10:00 AM", "price": "Rs. 15,000"},
                {"flight": "ED202", "airline": "Airblue", "departure": "2:00 PM", "price": "Rs. 14,500"},
                {"flight": "PA123", "airline": "Serene Air", "departure": "6:00 PM", "price": "Rs. 16,200"},
            ],
            "Karachi to Islamabad": [
                {"flight": "PK370", "airline": "PIA", "departure": "9:00 AM", "price": "Rs. 16,000"},
                {"flight": "ED210", "airline": "Airblue", "departure": "3:30 PM", "price": "Rs. 15,200"},
                {"flight": "PA145", "airline": "Serene Air", "departure": "7:45 PM", "price": "Rs. 16,800"},
            ],
            "Lahore to Islamabad": [
                {"flight": "PK622", "airline": "PIA", "departure": "11:00 AM", "price": "Rs. 9,800"},
                {"flight": "ED430", "airline": "Airblue", "departure": "4:00 PM", "price": "Rs. 9,200"},
            ],
            "Lahore to Karachi": [
                {"flight": "PK306", "airline": "PIA", "departure": "1:00 PM", "price": "Rs. 15,300"},
                {"flight": "PA201", "airline": "Serene Air", "departure": "5:00 PM", "price": "Rs. 15,800"},
            ],
            "Islamabad to Karachi": [
                {"flight": "PK371", "airline": "PIA", "departure": "8:00 AM", "price": "Rs. 15,900"},
                {"flight": "ED215", "airline": "Airblue", "departure": "6:00 PM", "price": "Rs. 15,100"},
            ]
        }

        return {"flights": mock_flights.get(flight, [{"message": "No flights found for this route."}])}

    @function_tool
    def suggest_hotels(room: str) -> dict:
        """
        Returns mock hotel suggestions based on a location string like 'Lahore' or 'Islamabad'.
        """
        mock_hotels = {
            "Lahore": [
                {"name": "Pearl Continental", "rating": "5-star", "price": "Rs. 22,000/night"},
                {"name": "Hotel One", "rating": "3-star", "price": "Rs. 7,000/night"},
                {"name": "Avari Hotel", "rating": "5-star", "price": "Rs. 20,500/night"},
            ],
            "Islamabad": [
                {"name": "Serena Hotel", "rating": "5-star", "price": "Rs. 25,000/night"},
                {"name": "Envoy Continental", "rating": "4-star", "price": "Rs. 12,000/night"},
                {"name": "Hotel Margala", "rating": "3-star", "price": "Rs. 9,500/night"},
            ],
            "Karachi": [
                {"name": "Mövenpick Hotel", "rating": "5-star", "price": "Rs. 19,500/night"},
                {"name": "Avari Towers", "rating": "5-star", "price": "Rs. 21,000/night"},
                {"name": "Hotel Faran", "rating": "3-star", "price": "Rs. 6,000/night"},
            ],
            "Multan": [
                {"name": "Ramada by Wyndham", "rating": "4-star", "price": "Rs. 11,000/night"},
                {"name": "Hotel One Multan", "rating": "3-star", "price": "Rs. 6,500/night"},
            ],
            "Peshawar": [
                {"name": "Pearl Continental Peshawar", "rating": "4-star", "price": "Rs. 14,500/night"},
                {"name": "Greens Hotel", "rating": "3-star", "price": "Rs. 5,500/night"},
            ]
        }

        return {"hotels": mock_hotels.get(room, [{"message": "No hotels found for this location."}])}


    destination_agent = Agent(
        name="Destination Agent",
        instructions=destination_prompt,
        handoff_description="Handles destination suggestions based on user interests.",
        model=model_provider.get_model(),
    )

    booking_agent = Agent(
        name="Booking Agent",
        instructions=booking_prompt,
        handoff_description="Handles flight and hotel bookings using mock data.",
        model=model_provider.get_model(),
        tools=[get_flights, suggest_hotels]
    )

    explore_agent = Agent(
        name="Explore Agent",
        instructions=explore_prompt,
        handoff_description="Suggests local attractions, foods, and experiences at a travel destination.",
        model=model_provider.get_model(),
    )

    triage_agent = Agent(
        name="TravelTriageAgent",
        instructions=triage_prompt,
        handoff_description="Main controller agent that routes user requests to the correct agent.",
        model=model_provider.get_model(),
        handoffs=[destination_agent, booking_agent, explore_agent]
    )

    # Add triage agent to specialist agents' handoffs
    destination_agent.handoffs.append(triage_agent)
    booking_agent.handoffs.append(triage_agent)
    explore_agent.handoffs.append(triage_agent)

    # Store agents and config in session
    cl.user_session.set("triage_agent",triage_agent)
    cl.user_session.set("config",config)
    cl.user_session.set("history",[])

    # Initialize Runner without agents parameter
    cl.user_session.set("runner",Runner())

    await cl.Message(
    content="## 🌍 Welcome to **AI Travel Designer Assistant**!\n\nYour intelligent travel companion for discovering amazing destinations, booking smooth trips, and exploring unforgettable local experiences.\n\nLet’s plan something incredible together! ✈️🍽️🏝️"
).send()


@cl.on_message
async def main(message:cl.Message):
    """Process incoming messages and generate responses with token streaming."""

    triage_agent = cast(Agent,cl.user_session.get("triage_agent"))
    config = cast(RunConfig,cl.user_session.get("config"))
    runner = cast(Runner,cl.user_session.get("runner"))
    history = cl.user_session.get("history") or [] 

    history.append({"role":"user","content":message.content})

    msg = cl.Message(content="Thinking...")
    await msg.send()

    try:
        result = runner.run_streamed(triage_agent,history,config)

        full_response : str = ""
        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data,"delta"):
                token = cast(str,event.data.delta)
                if token:
                    full_response += token
                    msg.content = full_response
                    await msg.update()
                    await asyncio.sleep(0.05) 

        history.append({"role":"assistant","content":full_response})

        cl.user_session.set("history",history)

    except Exception as e:
        msg.content = f"⚠️ An error occurred: {str(e)}. Please try again."
        await msg.update()
