# Game Assistant Agent

## 🎯 Overview

The **Game Assistant Agent** is a multi-agent AI that creates immersive fantasy RPG experiences. It narrates adventures, generates content, and assists with gameplay for solo or group players.

## 💡 Key Features

- Dynamic storytelling with vivid narratives.
- Generates monsters, loot, and events.
- Assists with rules and strategic choices.
- Multi-agent system (Narrator, Monster, Item, Triage).
- Customizable adventures based on user input.

## 🚀 Usage

1. Begin: *“Start as a rogue elf in a dark forest.”*
2. Explore, fight enemies, and collect treasures.
3. Ask for help: *“What does this potion do?”*
4. Shape the story with your choices.

## 🛠️ Technology

- **Framework**: Chainlit for interactive gaming UI.
- **AI Backend**: OpenAI Agents SDK for multi-agent storytelling.
- **Additional AI**: Gemini API for narrative creativity.
- **Environment**: `python-dotenv` for API key management.
- **Processing**: `asyncio` and `run_streamed` for real-time gameplay.
- **Game Logic**: Custom RPG system.

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

4. **Access**: Open `http://localhost:8000`.

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
Your gateway to epic fantasy adventures.

## 📜 License

MIT License. See `LICENSE` for details.
