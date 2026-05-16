# MomentumAI 🏏

**[🚀 Try it Live on Google Cloud Run](https://momentum-ai-283188353851.us-central1.run.app/)**
## 🎯 The problem
When the IPL final is on, your girlfriend gets ignored, your mom worries, your boss waits, your food shows up at the wrong time, and you still miss the clutch moment fumbling on a delivery app. Every sports app makes this worse.

## 🤖 What MomentumAI does
A Gemini-powered agent watches the live match. When key moments happen — a wicket, a lull, a clutch over, a message from your girlfriend — it decides whether to act on your behalf:
- ✉️ Drafts and sends replies (girlfriend, mom, boss) in your tone
- 🍕 Orders food timed to halftime
- 🔕 Silences your phone during clutch overs
- 🚗 Books your Uber before the final whistle
- 🏠 Triggers smart home celebration when your team wins
- 🤝 Coordinates with friends' agents across cities

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
