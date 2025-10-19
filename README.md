# TreadWise Tire Co. - AI Business Agent

**Student:** Mounir Khalil
**ID:** 202100437
**Course:** EECE798S Agentic Systems

## Overview

An AI-powered chatbot for TreadWise Tire Co., a modern tire company combining smart technology, mobile service, and sustainability. The agent can answer questions about the business, collect customer leads, and log feedback for questions it cannot answer.

## Business Description

TreadWise Tire Co. is a tire company built for today's drivers and fleets. Our mission is to make road travel safer and greener by pairing premium tires with mobile service and sensor-driven analytics that extend tire life and reduce waste.

### Key Features:
- **Smart Tread™ Platform:** IoT pressure & temperature sensors with predictive analytics
- **Mobile Installation:** Same-day service at your home or workplace
- **Circular Economy:** Retreading, refurbishment, and certified recycling programs
- **Fleet Solutions:** Commercial tire management and monitoring

## Project Structure

```
treadwise-tires-co/
├── About_business.pdf          # Detailed business profile
├── Business_summary.txt         # Short business summary
├── Business_agent.ipynb         # Main chatbot implementation (Jupyter)
├── app.py                       # Deployment script for Gradio
├── requirements.txt             # Python dependencies
├── .env                         # API keys (not committed to git)
├── .gitignore                   # Git ignore file
└── README.md                    # This file
```

## Features

### 1. Tool Functions

The agent implements two tool-calling functions:

#### `record_customer_interest(email, name, message)`
- Records customer contact information when they express interest
- Logs leads to `customer_leads.jsonl`
- Used when customers want to schedule service, get quotes, or learn more

#### `record_feedback(question)`
- Logs questions the agent cannot answer
- Saves to `feedback_log.jsonl`
- Helps improve the knowledge base

### 2. System Prompt

The agent is configured with a comprehensive system prompt that:
- Defines TreadWise's brand voice (friendly, professional, solution-oriented)
- Provides business context from the summary and PDF
- Guides behavior for lead collection and feedback logging
- Ensures the agent stays in character

### 3. OpenAI Integration

- Uses OpenAI's GPT-4o-mini model
- Implements function calling for tool use
- Maintains conversation history for context

### 4. Gradio Interface

Interactive web interface with:
- Clean, modern design
- Example questions to get started
- Real-time conversation
- Clear chat and delete previous message options

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_key_here
   ```

## Usage

### Option 1: Run the Jupyter Notebook

Open `Business_agent.ipynb` in Jupyter Lab or Google Colab and run all cells.

### Option 2: Run the Python Script

```bash
python app.py
```

This will launch a Gradio interface accessible via a local URL and a shareable public URL.

## Example Interactions

**User:** What services does TreadWise offer?
**Agent:** [Explains retail sales, mobile installation, IoT monitoring, etc.]

**User:** I'm interested in scheduling a mobile tire installation
**Agent:** [Asks for name, email, and details, then uses `record_customer_interest` tool]

**User:** What's your pricing for 18-wheelers?
**Agent:** [If not in knowledge base, uses `record_feedback` tool and apologizes]

## Tool Call Examples

### Lead Collection
```json
{
  "timestamp": "2025-10-19 14:30:22",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "message": "Interested in fleet monitoring for 20 vehicles"
}
```

### Feedback Logging
```json
{
  "timestamp": "2025-10-19 14:35:10",
  "question": "Do you ship tires internationally?"
}
```

## Technologies Used

- **OpenAI API:** GPT-4o-mini for conversational AI
- **Gradio:** Web interface for the chatbot
- **Python-dotenv:** Environment variable management
- **PyPDF2:** PDF processing (if needed)

## Deployment

### Local Deployment
Run `app.py` to launch locally with a shareable Gradio link.

### HuggingFace Spaces (Bonus)
1. Create a new Space on HuggingFace
2. Upload all files except `.env`
3. Add `OPENAI_API_KEY` as a Space secret
4. The app will automatically deploy

## Assignment Requirements Checklist

- [x] Business identity created (TreadWise Tire Co.)
- [x] Mission and services defined
- [x] Team profiles included
- [x] Unique value proposition articulated
- [x] `About_business.pdf` created
- [x] `Business_summary.txt` created
- [x] `record_customer_interest` tool implemented
- [x] `record_feedback` tool implemented
- [x] System prompt configured
- [x] OpenAI chat integration with tool calling
- [x] Gradio interface implemented
- [x] `Business_agent.ipynb` created
- [x] `requirements.txt` created
- [x] `.env` file setup (not committed)
- [x] Tools actually called by the model
- [ ] Deployed to HuggingFace Spaces (optional bonus)

## Author

**Mounir Khalil**
Student ID: 202100437
American University of Beirut
EECE798S Agentic Systems - Chapter 3 Assignment
