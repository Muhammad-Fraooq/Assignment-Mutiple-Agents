# Multi-Agent AI Assistants

## 🎯 Overview

This repository delivers three multi-agent AI systems for real-world impact: **Career Mentor Agent**, **AI Travel Designer Assistant**, and **Game Assistant Agent**. Powered by cutting-edge AI, these tools empower users globally—helping professionals land dream jobs, travelers plan unforgettable trips, and gamers dive into immersive RPG adventures.

- **Career Mentor Agent**: Provides tailored career paths, skill development plans, and job market insights for students, professionals, and career-switchers.
- **AI Travel Designer Assistant**: Designs budget-friendly travel itineraries with real-time destination insights for seamless adventures.
- **Game Assistant Agent**: Crafts dynamic RPG experiences with interactive storytelling and gameplay support for solo or group players.

## 💡 Key Features

- **Career Mentor**:
  - Matches skills and interests to ideal careers.
  - Offers skill-gap analysis and curated learning resources.
  - Tracks career progress with actionable roadmaps.
- **AI Travel Designer**:
  - Creates daily itineraries with optimized flights and hotels.
  - Provides weather, cultural tips, and destination suggestions.
  - Adapts plans to user preferences in real time.
- **Game Assistant**:
  - Generates immersive narratives, monsters, and loot.
  - Assists with RPG rules and strategic decisions.
  - Supports customizable solo or group adventures.
- **Shared**:
  - Multi-agent collaboration for seamless, real-time results.
  - Practical outputs for career growth, travel booking, and gaming fun.

## 🚀 Usage

1. **Access the App**: Launch via Chainlit at `http://localhost:8000` after setup.
2. **Engage with Agents**:
   - **Career**: *“Suggest a career for my data analysis skills.”* → Get a roadmap with jobs and courses.
   - **Travel**: *“Plan a 5-day Japan trip under $1000.”* → Receive a detailed itinerary with booking links.
   - **Game**: *“Start as a mage in a cursed forest.”* → Dive into a narrated RPG adventure.
3. **Apply Results**: Follow career steps, book travel plans, or enjoy immersive gameplay.
4. **Refine**: Use follow-up queries to tweak outputs (e.g., *“Add more outdoor activities to my trip.”*).

## 🛠️ Technology

- **Framework**: Chainlit for intuitive web interfaces.
- **AI Backend**: OpenAI Agents SDK for multi-agent orchestration.
- **Additional AI**: Gemini API for enhanced content generation.
- **Environment**: `python-dotenv` for secure API key management.
- **Processing**: `asyncio` and `run_streamed` for real-time performance.
- **Data**: Custom ontologies (career, travel, RPG) and APIs (job markets, flights, weather).

## ⚙️ Setup and Configuration

- **Prerequisites**: Ensure Python 3.8+ and `uv` are installed for dependency management.
- **Clone**: Download the repo from `https://github.com/Muhammad-Fraooq/Assignment-Mutiple-Agents.git`.
- **Environment**: Create a `.env` file with:

  ```
  GEMINI_API_KEY=your_gemini_api_key
  ```
- **Dependencies**: Use `uv` to manage packages (Chainlit, OpenAI, python-dotenv, google-generativeai).
- **Run**: Execute `chainlit run app.py` to start the app locally.
- **Access**: Open `http://localhost:8000` in a browser.

## 🛡️ Troubleshooting

- **API Errors**: Verify `GEMINI_API_KEY` in `.env` are valid.
- **Dependency Issues**: Ensure `uv` is updated and Python is 3.8+. Reinstall packages if conflicts arise.
- **Performance**: Check system resources for `asyncio` tasks; increase memory for large-scale use.
- **Support**: File issues on GitHub or check logs in the Chainlit interface.

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Submit a pull request with clear descriptions.

## 📬 Contact Us

Have questions or ideas? Let’s connect!

- 👨‍💻 **Name** : Muhammad Farooq
- 📧 **Email**: [Email](mailto:muhammad888xyz@gmail.com)
- 🌐 **Portfolio**: [Muhammad Farooq](https://porfolio-milestone-2-pk.vercel.app/)
- **Social Media**:
  - **Facebook**: [Facebook](https://web.facebook.com/)
  - **Medium**: [Medium](https://medium.com/@muhammad888xyz)
  - **LinkedIn**: [LinkedIn](https://www.linkedin.com/in/muhammad-farooq-developer/)
  - **Twitter**: [Twitter](https://x.com/Muhammaddev2007)

## 🧑‍💻 Creator

Crafted by **Muhammad Farooq**\
Empowering careers, travel, and adventures with AI.

## 📜 License

MIT License. See `LICENSE` for details.