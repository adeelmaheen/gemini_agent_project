# Gemini Agent Project

Created by Maheen Arif

✅ **Summary**
- 🧠 Gemini model powered using Agents SDK (no OpenAI key)
- 🔍 Official Chainlit web tool for real-time info
- 🔗 Clickable source links improve transparency
- 🛠️ Clean, docs-aligned implementation ready for classroom presentation

A Python project that demonstrates a simple agent and a chat interface using Chainlit and Gemini API.

## Features
- Simple Python entry point (`main.py`)
- Chat interface powered by Chainlit
- Integration with Gemini API (Google's generative language model)
- Environment variable management with `python-dotenv`

## Project Structure
```
gemini_agent_project/
│   
│   pyproject.toml
│   requirements.txt
│   uv.lock
│   README.md
└───chat_interface/
        app.py
        
```

## Getting Started

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (for dependency management)

### Installation
1. Clone the repository or download the project files.
2. Install dependencies:
   ```sh
   uv sync
   ```
3. Set up your environment variables (e.g., `GEMINI_API_KEY`) in a `.env` file.

### Running the Project
- To run the main script:
  ```sh
  python main.py
  ```
- To start the chat interface:
  ```sh
  uv start
  ```
  or
  ```sh
  uv run chainlit run chat_interface/app.py -w
  ```

## Configuration
- Place your Gemini API key in a `.env` file at the project root:
  ```env
  GEMINI_API_KEY=your_api_key_here
  ```

## Dependencies
- chainlit
- openai-agents
- python-dotenv

All dependencies are listed in `requirements.txt` and `pyproject.toml`.

## License
This project is for educational purposes.
