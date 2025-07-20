# AI Travel Designer Assistant

## 🎯 Overview

The **AI Travel Designer Assistant** is a multi-agent AI that crafts personalized travel itineraries based on budget, interests, and destinations. It simplifies real-world travel planning for seamless adventures.

## 💡 Key Features

- Custom itineraries with daily plans.
- Budget-optimized flights, hotels, and activities.
- Destination suggestions with weather and cultural insights.
- Travel tips and packing lists.
- Multi-agent system for planning, budgeting, and research.

## 🚀 Usage

1. Start with: *“Plan a 5-day Japan trip under $1000.”*
2. Review your itinerary with activities and costs.
3. Get tips for safety and packing.
4. Adjust plans with feedback like *“Add hiking.”*

## 🛠️ Technology

- **Framework**: Chainlit for web-based UI.
- **AI Backend**: OpenAI Agents SDK for multi-agent coordination.
- **Additional AI**: Gemini API for destination insights.
- **Environment**: `python-dotenv` for API key management.
- **Processing**: `asyncio` and `run_streamed` for real-time planning.
- **Data**: Flight, hotel, and weather APIs.

## 📦 Installation

1. **Install dependencies**:

   ```bash
   uv add chainit openai-agents python-dotenv
   ```

2. **Set Up Environment**:

   - Create a `.env` file:

     ```
     GEMINI_API_KEY=your_gemini_api_key
     ```

3. **Run the Application**:

   ```bash
   chainlit run app.py
   ```

4. **Access**: Visit `http://localhost:8000`.

## 📋 Requirements

- Python 3.8+
- Chainlit
- OpenAI Agents SDK
- python-dotenv
- Gemini API
- asyncio
- uv (for dependency management)

## 🧑‍💻 Creator

Crafted by **Muhammad Farooq**\
Making travel planning effortless with AI.

## 📜 License

MIT License. See `LICENSE` for details.
