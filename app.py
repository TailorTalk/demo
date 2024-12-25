import streamlit as st
import requests
import base64

# Set API endpoints
CREATE_AGENT_URL = "https://statix-preview.up.railway.app/create"  # Replace with actual endpoint
QUERY_URL = "https://statix-preview.up.railway.app//query"  # Replace with actual endpoint

# Initialize chatbot state
if "agent_id" not in st.session_state:
    st.session_state.agent_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to create an agent
def create_agent():
    response = requests.post(CREATE_AGENT_URL, json={"system_message": ""})
    if response.status_code == 200:
        st.session_state.agent_id = response.json()
        st.session_state.messages.append({"role": "system", "content": "Agent created successfully."})
    else:
        st.error("Failed to create agent.")

# Function to query the agent
def query_agent(agent_id, query):
    response = requests.post(QUERY_URL, json={"agent_id": agent_id, "query": query})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to query agent.")
        return None

# UI layout
st.title("Analyst Agent by TailorTalk")

# Create agent on load
if st.session_state.agent_id is None:
    create_agent()

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "agent":
        st.markdown(f"**Agent:** {msg['content']}")
        if msg.get("image"):
            st.image(base64.b64decode(msg["image"]), caption="Agent Response")

# Chat input box below
def handle_input():
    user_message = st.session_state.chat_input.strip()
    if user_message and st.session_state.agent_id:
        # Append user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_message})

        # Query the agent
        response = query_agent(st.session_state.agent_id, user_message)
        if response:
            message = response.get("message", "No response")
            image = response.get("image")

            # Append bot response to chat history
            st.session_state.messages.append({"role": "agent", "content": message, "image": image})

        # Clear input box
        st.session_state.chat_input = ""

st.text_input(
    label="",
    placeholder="Type your message...",
    key="chat_input",
    on_change=handle_input,
)

