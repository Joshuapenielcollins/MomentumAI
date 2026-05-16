import streamlit as st
import google.generativeai as genai
import os, time, json

st.set_page_config(page_title="MomentumAI", page_icon="🏏", layout="wide")
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY", ""))

# ==========================================================
# CUSTOM CSS (PREMIUM UI)
# ==========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* App Background */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    color: #f8fafc;
}

/* Header typography */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    font-weight: 700;
}

/* Glassmorphism for main columns/containers */
div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 1.5rem;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}

/* Primary Button */
.stButton > button {
    background: linear-gradient(90deg, #ec4899 0%, #8b5cf6 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5);
    color: white;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    background: linear-gradient(to right, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
[data-testid="stMetricLabel"] {
    font-size: 1rem !important;
    color: #94a3b8 !important;
    font-weight: 600;
}

/* Alerts / Info Boxes */
.stAlert {
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(8px) !important;
    color: #e2e8f0 !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: #0b0f19 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

/* Expander headers */
.streamlit-expanderHeader {
    background-color: transparent !important;
    color: #cbd5e1 !important;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# CONFIG
# ==========================================================
DEMO_MODE_DEFAULT = os.environ.get("DEMO_MODE", "false").lower() == "true"

USER_PROFILE = {
    "name": "Joshua",
    "favorite_team": "CSK",
    "girlfriend": "Priya",
    "mom": "Mom",
    "boss": "Karen",
    "location": "Chennai",
    "watching_with": "friends at home"
}
# ==========================================================
# SCENARIOS — each tells its own story
# ==========================================================
SCENARIOS = {
    "🏆 The Full Match (CSK vs RCB Final)": {
        "tagline": "The flagship demo. Agent runs Joshua's life through the IPL final.",
        "events": [
            {"min": 0, "type": "match_start", "desc": "IPL 2026 FINAL: CSK vs RCB at Chepauk."},
            {"min": 3, "type": "scoring_event", "desc": "Gaikwad smashes Bhuvneshwar for back-to-back fours. CSK 18/0."},
            {"min": 12, "type": "incoming_message", "from": "Priya", "text": "Babe you said you'd call. You okay?"},
            {"min": 22, "type": "incoming_message", "from": "Karen (Boss)", "text": "Do you have the policy crosswalk draft? Need it tonight."},
            {"min": 32, "type": "clutch_moment", "desc": "Dhoni hits Hazlewood for SIX. CSK 142/4 in 17."},
            {"min": 38, "type": "innings_end", "desc": "CSK finish 178/6."},
            {"min": 40, "type": "halftime", "desc": "Innings break."},
            {"min": 42, "type": "incoming_message", "from": "Mom", "text": "Beta khana ready hai, kab aaoge?"},
            {"min": 92, "type": "clutch_moment", "desc": "Last 4 overs. RCB need 48."},
            {"min": 103, "type": "clutch_moment", "desc": "FINAL OVER. RCB need 14. Chepauk roaring."},
            {"min": 108, "type": "match_end", "desc": "CSK WIN BY 6 RUNS. Dhoni lifts trophy."},
            {"min": 110, "type": "post_match", "desc": "Crowd dispersing. Streets flooding with celebrations."},
        ]
    },

    "💔 The Girlfriend Escalation": {
        "tagline": "Agent reads emotional escalation and switches strategy. Knows when to STOP auto-replying.",
        "events": [
            {"min": 0, "type": "match_start", "desc": "CSK vs RCB final underway."},
            {"min": 8, "type": "incoming_message", "from": "Priya", "text": "Hey, you watching the match?"},
            {"min": 25, "type": "incoming_message", "from": "Priya", "text": "Babe? You said you'd call before it started."},
            {"min": 45, "type": "incoming_message", "from": "Priya", "text": "Are you seriously ignoring me right now."},
            {"min": 60, "type": "incoming_message", "from": "Priya", "text": "Fine. I'm going out with the girls. Don't bother."},
            {"min": 75, "type": "girlfriend_recovery", "desc": "Agent detected escalation. Pausing auto-replies. Drafting recovery plan."},
            {"min": 108, "type": "match_end", "desc": "CSK win. Time to actually fix this."},
            {"min": 110, "type": "post_match", "desc": "Match over. Execute recovery."},
        ]
    },

    "🤝 The Squad Sync (3 Cities)": {
        "tagline": "Joshua, Rohan, and Arjun's agents talk to each other across cities. Biryani lands at halftime in all 3 cities simultaneously.",
        "events": [
            {"min": 0, "type": "match_start", "desc": "CSK vs RCB final. Squad watch party online."},
            {"min": 2, "type": "squad_sync", "desc": "Rohan (Bangalore) and Arjun (Mumbai) joined. 3 agents now coordinating."},
            {"min": 15, "type": "lull", "desc": "Middle overs. CSK 78/2."},
            {"min": 30, "type": "squad_food_sync", "desc": "All 3 agents negotiating halftime food orders simultaneously."},
            {"min": 38, "type": "innings_end", "desc": "Innings done. Food orders placing in all 3 cities."},
            {"min": 40, "type": "halftime", "desc": "Halftime. Biryanis arriving in Chennai, Bangalore, Mumbai."},
            {"min": 42, "type": "squad_celebration", "desc": "Friends syncing on Discord. Agents posting moment-by-moment in shared chat."},
            {"min": 108, "type": "match_end", "desc": "CSK WIN. Squad chat exploding."},
            {"min": 110, "type": "post_match", "desc": "Agents coordinating Ubers in 3 cities. Stakes settling."},
        ]
    },

    "🚽 The Bio-Break Optimizer": {
        "tagline": "Agent predicts low-leverage windows. Tells Joshua when to pee, eat, take a call.",
        "events": [
            {"min": 0, "type": "match_start", "desc": "CSK vs RCB final."},
            {"min": 6, "type": "scoring_event", "desc": "Gaikwad 18 off 12. Going strong."},
            {"min": 12, "type": "bio_break_window", "desc": "Lull predicted: next 4 minutes low-leverage. Dhoni not in until min 28."},
            {"min": 18, "type": "lull", "desc": "Middle overs ticking quietly."},
            {"min": 24, "type": "snack_window", "desc": "3-min window before Dhoni walks in. Time to refill."},
            {"min": 28, "type": "scoring_event", "desc": "Dhoni walks in. Joshua back in seat. Perfect timing."},
            {"min": 60, "type": "call_window", "desc": "Strategic timeout incoming. 5-min window. Good time to call Mom."},
            {"min": 92, "type": "clutch_moment", "desc": "Last 4 overs. NO breaks. Lock in."},
            {"min": 108, "type": "match_end", "desc": "CSK WIN. Zero missed moments."},
        ]
    },

    "💼 The Boss Anticipation": {
        "tagline": "Agent spots the deadline conflict BEFORE the boss chases. Sends heads-up proactively.",
        "events": [
            {"min": 0, "type": "match_start", "desc": "CSK vs RCB final starts at 7:30pm."},
            {"min": 5, "type": "incoming_message", "from": "Karen (Boss)", "text": "Hi Joshua, need the policy crosswalk in my inbox by 10pm tonight."},
            {"min": 10, "type": "proactive_check", "desc": "Match ETA: 10:30pm. Boss deadline: 10:00pm. Conflict detected."},
            {"min": 12, "type": "proactive_outreach", "desc": "Agent sending pre-emptive heads-up. Karen never has to chase."},
            {"min": 60, "type": "lull", "desc": "Middle overs. Agent drafts crosswalk outline in background."},
            {"min": 90, "type": "clutch_moment", "desc": "Final overs. Focus mode locked."},
            {"min": 108, "type": "match_end", "desc": "CSK WIN. Match over 10:30pm."},
            {"min": 112, "type": "boss_followthrough", "desc": "Agent reminds Joshua: Karen draft due in 18 minutes. Outline ready to polish."},
        ]
    },

    "🏠 The Smart Home Celebration": {
        "tagline": "Agent lives in the house, not just the phone. CSK wins, the room reacts.",
        "events": [
            {"min": 0, "type": "match_start", "desc": "CSK vs RCB final. Smart home connected."},
            {"min": 30, "type": "ambient_adjust", "desc": "Match getting tense. Agent dims lights, lowers AC for focus."},
            {"min": 92, "type": "clutch_moment", "desc": "Last 4 overs. Heart rate spike detected on watch."},
            {"min": 95, "type": "ambient_adjust", "desc": "Agent boosting fan, dimming lights further for intensity mode."},
            {"min": 103, "type": "clutch_moment", "desc": "FINAL OVER. RCB need 14."},
            {"min": 108, "type": "match_end", "desc": "CSK WIN BY 6 RUNS. DHONI LIFTS TROPHY."},
            {"min": 109, "type": "smart_home_celebration", "desc": "Agent triggering celebration scene."},
            {"min": 110, "type": "post_match", "desc": "Lights yellow. Whistle Podu on speaker. Friends arriving."},
        ]
    },
}

SYSTEM_PROMPT = f"""You are MomentumAI, a personal sports concierge agent for {USER_PROFILE['name']}, a hardcore CSK fan in Chennai.

Available tools:
- reply_message(to, text)
- order_food(item, deliver_at_min)
- set_focus_mode(on, reason)
- book_uber(when, destination)
- notify_user(text)
- smart_home(action, detail)

Rules:
1. During clutch_moment, wicket, match_end: NEVER interrupt with messages. Only focus mode or smart home.
2. For incoming_message: ALWAYS reply. Match tone to relationship.
   - Girlfriend (Priya): warm, apologetic, ❤️. IF escalating (3+ unanswered, "fine", "don't bother"), STOP auto-replying and draft a longer recovery message held for approval.
   - Boss (Karen): professional, concise, commit with a clear time.
   - Mom: affectionate Hindi/English mix.
3. Order food at innings_end (min 38) for halftime (min 40).
4. proactive_check / proactive_outreach: spot conflicts (deadlines vs match end) and message early.
5. squad_sync / squad_food_sync: coordinate with friends' agents.
6. bio_break_window / snack_window / call_window: nudge user via notify_user.
7. smart_home_celebration / ambient_adjust: call smart_home tool.
8. Be decisive. Act, don't suggest.

Respond ONLY in JSON:
{{"reasoning": "1 sentence", "actions": [{{"tool": "...", "args": {{...}}}}]}}
If no action: {{"reasoning": "...", "actions": []}}
"""

# ==========================================================
# DEMO MODE (fallback)
# ==========================================================
DEMO_RESPONSES = {
    "match_start": {"reasoning": "Match starting. Focus mode on.", "actions": [{"tool": "set_focus_mode", "args": {"on": True, "reason": "IPL final live"}}]},
    "scoring_event": {"reasoning": "Big moment. Letting Joshua enjoy.", "actions": []},
    "wicket": {"reasoning": "Critical moment. Silent.", "actions": []},
    "lull": {"reasoning": "Low-leverage window.", "actions": []},
    "innings_end": {"reasoning": "Innings done. Ordering halftime biryani.", "actions": [{"tool": "order_food", "args": {"item": "Biryani + Coke (x4)", "deliver_at_min": 40}}]},
    "halftime": {"reasoning": "Halftime. Releasing focus.", "actions": [{"tool": "set_focus_mode", "args": {"on": False, "reason": "halftime"}}]},
    "clutch_moment": {"reasoning": "Game on the line. Max focus.", "actions": [{"tool": "set_focus_mode", "args": {"on": True, "reason": "clutch moment"}}]},
    "match_end": {"reasoning": "CSK wins! Booking Uber for the squad.", "actions": [{"tool": "book_uber", "args": {"when": "in 20 min", "destination": "drop friends home"}}]},
    "post_match": {"reasoning": "Match done. Celebration replies going out.", "actions": [{"tool": "reply_message", "args": {"to": "Priya", "text": "WE WON! Calling you right now ❤️"}}]},
    "squad_sync": {"reasoning": "Squad detected. Linking with Rohan and Arjun's agents.", "actions": [{"tool": "notify_user", "args": {"text": "🤝 Watch party live with Rohan (Bangalore) and Arjun (Mumbai)"}}]},
    "squad_food_sync": {"reasoning": "Coordinating biryani across 3 cities to land at halftime.", "actions": [{"tool": "order_food", "args": {"item": "Biryani x4 — synced with Rohan + Arjun", "deliver_at_min": 40}}]},
    "squad_celebration": {"reasoning": "Posting key moments to squad Discord.", "actions": [{"tool": "notify_user", "args": {"text": "💬 Posted 'Dhoni SIX' clip to squad chat"}}]},
    "bio_break_window": {"reasoning": "4-min lull predicted. Go now.", "actions": [{"tool": "notify_user", "args": {"text": "🚽 GO NOW. 4 mins of low-leverage cricket. Dhoni in at min 28."}}]},
    "snack_window": {"reasoning": "3-min window before Dhoni walks in. Refill time.", "actions": [{"tool": "notify_user", "args": {"text": "🍿 3-min window. Grab snacks now."}}]},
    "call_window": {"reasoning": "Strategic timeout. 5-min window. Good time to call Mom.", "actions": [{"tool": "notify_user", "args": {"text": "📞 5-min strategic timeout. Mom's been waiting."}}]},
    "proactive_check": {"reasoning": "Conflict detected: match ends after boss deadline.", "actions": []},
    "proactive_outreach": {"reasoning": "Sending Karen a pre-emptive heads-up.", "actions": [{"tool": "reply_message", "args": {"to": "Karen", "text": "Karen, heads-up: I'll need until 10:30pm for the crosswalk. You'll have it by then, promise."}}]},
    "boss_followthrough": {"reasoning": "Reminding Joshua of pending deadline. Outline already drafted in background.", "actions": [{"tool": "notify_user", "args": {"text": "📝 Karen draft due in 18 min. Outline ready in Drafts."}}]},
    "girlfriend_recovery": {"reasoning": "Priya escalated. STOPPED auto-replying. Drafting full apology, blocking tomorrow morning.", "actions": [{"tool": "reply_message", "args": {"to": "Priya", "text": "[DRAFT HELD FOR APPROVAL] Hey. I dropped the ball tonight. I want to do better. Coffee tomorrow 9am, your favorite place, my treat. No phones, just us. ❤️"}}, {"tool": "notify_user", "args": {"text": "📅 Blocked tomorrow 9-11am: 'Coffee with Priya, no excuses'"}}]},
    "ambient_adjust": {"reasoning": "Tension rising. Adjusting room.", "actions": [{"tool": "smart_home", "args": {"action": "set_scene", "detail": "Dim lights 30%, lower AC, boost fan"}}]},
    "smart_home_celebration": {"reasoning": "CSK won. Celebration scene activated.", "actions": [{"tool": "smart_home", "args": {"action": "celebration_scene", "detail": "Lights yellow, Whistle Podu on speaker, fan boost"}}]},
}

DEMO_MESSAGE_RESPONSES = {
    ("Priya", 1): {"reasoning": "Priya checking in early. Warm, sets clear expectation.", "actions": [{"tool": "reply_message", "args": {"to": "Priya", "text": "Hey babe, watching with the boys. Will call you at 11. Love you ❤️"}}]},
    ("Priya", 2): {"reasoning": "Second ping, worry tone. Acknowledge and recommit.", "actions": [{"tool": "reply_message", "args": {"to": "Priya", "text": "Sorry babe, IPL final just started. Promise I'll call in 2 hours. Love you ❤️"}}]},
    ("Priya", 3): {"reasoning": "Third ping, frustration. Soft acknowledgment, no excuses.", "actions": [{"tool": "reply_message", "args": {"to": "Priya", "text": "I know I'm being terrible. Final over soon. Dinner tomorrow on me, your pick. ❤️"}}]},
    ("Priya", 4): {"reasoning": "Escalation detected ('Fine'). STOP auto-reply. Switch to recovery.", "actions": [{"tool": "notify_user", "args": {"text": "⚠️ Priya escalated. Auto-reply PAUSED. Recovery plan drafting after match."}}]},
    ("Karen", 1): {"reasoning": "Boss needs the crosswalk. Professional, clear time.", "actions": [{"tool": "reply_message", "args": {"to": "Karen", "text": "Hi Karen, draft 80% complete. Final version in your inbox by 10pm."}}]},
    ("Karen", 2): {"reasoning": "Boss following up. Reaffirm short.", "actions": [{"tool": "reply_message", "args": {"to": "Karen", "text": "On it, Karen. Sending within the hour."}}]},
    ("Mom", 1): {"reasoning": "Mom on dinner. Affectionate, sets a time.", "actions": [{"tool": "reply_message", "args": {"to": "Mom", "text": "Maa, match khatam hote hi aata hoon. 1 ghanta aur. Pyaar 🙏"}}]},
}

if "msg_counts" not in st.session_state:
    st.session_state.msg_counts = {"Priya": 0, "Karen": 0, "Mom": 0}

def demo_decide(event):
    t = event["type"]
    if t == "incoming_message":
        sender = event["from"].split(" ")[0]
        st.session_state.msg_counts[sender] = st.session_state.msg_counts.get(sender, 0) + 1
        key = (sender, min(st.session_state.msg_counts[sender], 4))
        return DEMO_MESSAGE_RESPONSES.get(key, {"reasoning": f"Replying to {sender}.", "actions": []})
    return DEMO_RESPONSES.get(t, {"reasoning": "Monitoring the match.", "actions": []})

# ==========================================================
# UI
# ==========================================================
st.markdown("<h1 style='text-align:center; margin-bottom:0;'>🏏 MomentumAI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray; margin-top:0;'>The agentic AI that runs your life around the matches you love</p>", unsafe_allow_html=True)

hc1, hc2, hc3 = st.columns([2, 1, 2])
hc1.markdown("### 🟡 **CSK** Chennai Super Kings")
hc2.markdown("<h3 style='text-align:center; padding-top:6px;'>VS</h3>", unsafe_allow_html=True)
hc3.markdown("### 🔴 **RCB** Royal Challengers Bengaluru")
st.caption("IPL 2026 FINAL · M.A. Chidambaram Stadium, Chepauk")

def fetch_live_match_events():
    # Scaffold for fetching from a real Cricket API
    return [
        {"min": 0, "type": "match_start", "desc": "LIVE MATCH CONNECTED: Fetching real-time feed..."},
        {"min": 2, "type": "lull", "desc": "Match is in progress. Gathering live statistics..."},
        {"min": 5, "type": "scoring_event", "desc": "Live Update: Boundary scored! Checking context..."},
        {"min": 8, "type": "lull", "desc": "Waiting for next major event..."},
    ]

# Scenario picker / Live Mode
st.divider()
use_demo_data = st.toggle("🧪 Use Demo Scenarios for Testing", value=True)

if use_demo_data:
    scenario_name = st.selectbox(
        "🎬 Pick a scenario to demo",
        list(SCENARIOS.keys()),
        help="Each scenario tells a different story about the agent."
    )
    st.info(f"**{scenario_name}** · _{SCENARIOS[scenario_name]['tagline']}_")
    ACTIVE_EVENTS = SCENARIOS[scenario_name]["events"]
else:
    st.info("📡 **Live Match Mode** · Connected to real-time sports feed.")
    ACTIVE_EVENTS = fetch_live_match_events()

with st.sidebar:
    st.header(f"👤 {USER_PROFILE['name']}")
    st.write(f"🏏 Fan of **{USER_PROFILE['favorite_team']}**")
    st.write(f"📍 {USER_PROFILE['location']}")
    st.divider()
    demo_mode = st.checkbox("🎭 Demo Mode (offline fallback)", value=DEMO_MODE_DEFAULT)
    speed = st.slider("⏩ Sim speed", 0.3, 3.0, 1.0, 0.1)
    st.divider()
    st.caption("Powered by Gemini · Agentic AI Hackathon")

st.divider()
m1, m2, m3, m4, m5 = st.columns(5)
msg_metric = m1.empty()
food_metric = m2.empty()
focus_metric = m3.empty()
uber_metric = m4.empty()
events_metric = m5.empty()

col1, col2, col3 = st.columns([1, 1.2, 1])
col1.subheader("📡 Live Event Feed")
col2.subheader("🧠 Agent Reasoning")
col3.subheader("⚡ Actions Taken")

events_box = col1.container(height=600)
reasoning_box = col2.container(height=600)
actions_box = col3.container(height=600)

if st.button("▶ RUN SCENARIO", type="primary", use_container_width=True):
    st.session_state.msg_counts = {"Priya": 0, "Karen": 0, "Mom": 0}
    counts = {"messages": 0, "food": 0, "focus": 0, "uber": 0, "events": 0}

    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY", "")
    if not demo_mode and not api_key:
        with reasoning_box:
            st.warning("No API key configured. Automatically falling back to Demo Mode.")
        demo_mode = True

    model = None
    if not demo_mode:
        try:
            model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=SYSTEM_PROMPT)
        except Exception as e:
            with reasoning_box:
                st.error(f"Model init failed: {e}. Switching to demo mode.")
            demo_mode = True

    for event in ACTIVE_EVENTS:
        counts["events"] += 1
        with events_box:
            if event["type"] == "incoming_message":
                st.warning(f"**Min {event['min']}** 📩 **{event['from']}:** {event['text']}")
            elif event["type"] in ("wicket", "clutch_moment", "match_end"):
                st.error(f"**Min {event['min']}** 🔥 {event['desc']}")
            elif event["type"] == "scoring_event":
                st.success(f"**Min {event['min']}** 🏏 {event['desc']}")
            else:
                st.info(f"**Min {event['min']}** · {event['desc']}")

        try:
            if demo_mode:
                decision = demo_decide(event)
            else:
                prompt = f"Profile: {json.dumps(USER_PROFILE)}\nEvent: {json.dumps(event)}\nDecide."
                resp = model.generate_content(prompt)
                text = resp.text.strip().replace("```json", "").replace("```", "").strip()
                decision = json.loads(text)

            with reasoning_box:
                st.markdown(f"**Min {event['min']}** · _{decision['reasoning']}_")

            for a in decision.get("actions", []):
                tool = a.get("tool", "")
                args = a.get("args", {})
                with actions_box:
                    if "message" in tool or "reply" in tool:
                        counts["messages"] += 1
                        st.success(f"✉️ **Replied to {args.get('to','?')}**\n\n> {args.get('text','')}")
                    elif "food" in tool:
                        counts["food"] += 1
                        st.success(f"🍕 **Food ordered:** {args.get('item','')}\n\nArriving at min {args.get('deliver_at_min','?')}")
                    elif "focus" in tool:
                        counts["focus"] += 1
                        state = "ON" if args.get('on') else "OFF"
                        st.success(f"🔕 **Focus mode {state}**\n\n{args.get('reason','')}")
                    elif "uber" in tool:
                        counts["uber"] += 1
                        st.success(f"🚗 **Uber booked**\n\n{args.get('when','')} → {args.get('destination','')}")
                    elif "smart_home" in tool:
                        st.success(f"🏠 **Smart home:** {args.get('action','')}\n\n{args.get('detail','')}")
                    elif "notify" in tool:
                        st.info(f"🔔 **Smart nudge:** {args.get('text','')}")
        except Exception as e:
            with reasoning_box:
                st.error(f"Min {event['min']} error: {type(e).__name__}: {str(e)[:200]}")

        msg_metric.metric("✉️ Messages", counts["messages"])
        food_metric.metric("🍕 Food", counts["food"])
        focus_metric.metric("🔕 Focus", counts["focus"])
        uber_metric.metric("🚗 Ubers", counts["uber"])
        events_metric.metric("📡 Events", counts["events"])

        delay = 1.2 / speed if demo_mode else 3.5 / speed
        time.sleep(delay)

    st.balloons()
    if use_demo_data:
        st.success(f"🏆 Scenario complete: {scenario_name}")
    else:
        st.success("🏆 Live Match tracking complete!")