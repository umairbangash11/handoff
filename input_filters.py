import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, handoff
from agents.run import RunConfig
from agents import enable_verbose_stdout_logging
from agents.extensions import handoff_filters
from openai import AsyncOpenAI

# Enable Logs
enable_verbose_stdout_logging()

# Load .env Variables
load_dotenv()

# Get Gemini API Key
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Initialize Gemini Client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Gemini Model Setup
model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.5-flash",
)

# RunConfig
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=False
)

# -------------------------
# Define FAQ Agent
# -------------------------
faq_agent = Agent(
    name="FAQ Agent",
    instructions="You answer frequently asked questions in a clear and friendly manner.",
    model=model
)

# -------------------------
# Define Handoff with Input Filter (remove_all_tools)
# -------------------------
custom_handoff = handoff(
    agent=faq_agent,
    input_filter=handoff_filters.remove_all_tools  # Remove all tool calls from history
)

# -------------------------
# Define Triage Agent
# -------------------------
triage_agent = Agent(
    name="Triage Agent",
    instructions="If the query is a general FAQ, hand it off to FAQ Agent.",
    handoffs=[custom_handoff],
    model=model
)

# -------------------------
# Main Async Function
# -------------------------
async def main():
    result = await Runner.run(
        triage_agent,
        input="Can you tell me about your refund policy?",
        run_config=config
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
