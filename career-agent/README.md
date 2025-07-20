# Career Mentor Agent

## 🎯 Overview

The **Career Mentor Agent** is a multi-agent AI system that guides users in discovering and planning their careers. It delivers personalized career advice, skill development plans, and industry insights for students, professionals, and career-switchers.

## 💡 Key Features

- Personalized career suggestions based on interests and skills.
- Skill-gap analysis with learning resource recommendations.
- Custom career roadmaps with milestones and job opportunities.
- Real-time industry trends and goal tracking.
- Multi-agent system for career matching, resources, and coaching.

## 🚀 Usage

1. Launch via Chainlit and ask: *“What career fits my data science interest?”*
2. Get a tailored roadmap with resources and job suggestions.
3. Track progress with queries like *“What’s my next step?”*
4. Refine plans based on feedback.

## 🛠️ Technology

- **Framework**: Chainlit for interactive web UI.
- **AI Backend**: OpenAI Agents SDK for multi-agent orchestration.
- **Additional AI**: Gemini API for content generation.
- **Environment**: `python-dotenv` for secure API key management.
- **Processing**: `asyncio` and `run_streamed` for real-time responses.
- **Data**: Custom career ontology and job market APIs.

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
Helping you find your career path with AI.

## 📜 License

MIT License. See `LICENSE` for details.
