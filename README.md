# MomentumAI 🏏

**[🚀 Try it Live on Google Cloud Run](https://momentum-ai-283188353851.us-central1.run.app/)**
MomentumAI is an agentic AI concierge built with Streamlit and Google's Gemini API, designed to run your life around the sports matches you love. It acts as an autonomous agent that manages incoming messages, anticipates conflicts, monitors live matches, and makes decisions on your behalf so you never miss a clutch moment.

## 🎯 The Problem It Solves

As die-hard sports fans, we've all been there: **Life doesn't stop just because the finals are on.**
MomentumAI was built to solve the ultimate fan dilemmas:
- **The Social Tax:** Getting into arguments with a significant other because you ignored their texts during a tight chase. MomentumAI dynamically reads the tone of messages, auto-replies based on the match situation, and knows when to escalate or back off.
- **The Work Conflict:** Missing a crucial deadline because the match went into a super over. The agent proactively compares match ETAs with your work deadlines and sends heads-ups to your boss *before* they ask.
- **The Biological Timing:** Missing a hat-trick because you went to grab a snack or use the restroom. The agent predicts "low-leverage" lull periods in the match and explicitly tells you when it's safe to step away.
- **The Group Coordination:** Losing focus because you have to coordinate food delivery for the squad. The agent syncs with your friends' agents to automatically order halftime biryani so it arrives perfectly at the innings break.

## Features
- 📡 **Live Match Mode**: Architecture designed to hook into real-time sports APIs for live event tracking.
- 🧪 **Smart Scenarios (Demo Mode)**: Test the AI against complex social situations like managing a boss's deadline or de-escalating an argument while a match is ongoing.
- 🎨 **Premium UI**: Sleek, glassmorphic dark mode interface.
- ☁️ **Cloud Ready**: Configured with a `Dockerfile` for seamless deployment to Google Cloud Run.

## Installation & Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Joshuapenielcollins/MomentumAI.git
   cd MomentumAI
   ```

2. **Install dependencies:**
   Make sure you have Python 3.11+ installed.
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your API Key:**
   The application requires a Gemini API key.
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Deploying to Google Cloud Run

This project includes a `Dockerfile` that allows it to be deployed instantly to Google Cloud.

1. Authenticate with Google Cloud CLI:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

2. Deploy the service:
   ```bash
   gcloud run deploy momentum-ai \
     --source . \
     --region us-central1 \
     --allow-unauthenticated
   ```

## Architecture
The application uses the `gemini-2.5-flash` model, fed with a system prompt detailing the user's profile and available "tools" (e.g., `reply_message`, `order_food`, `set_focus_mode`). For every event in the match timeline, the agent is queried to determine the best course of action.
