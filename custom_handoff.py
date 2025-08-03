import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, handoff, RunContextWrapper
from agents.run import RunConfig
from openai import AsyncOpenAI
from agents import enable_verbose_stdout_logging

# Enable verbose logs
enable_verbose_stdout_logging()

# Load environment variables
load_dotenv()

# Load GEMINI API KEY
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Initialize Gemini client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Gemini Model for SDK
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
# Custom Handoff Function
# -------------------------
def on_handoff(ctx: RunContextWrapper[None]):
    print("Handoff was called successfully!")  # Custom logic on handoff trigger

# -------------------------
# Agents
# -------------------------

# Sub-Agent to be handed off to
money_sender_agent = Agent(
    name="Money Sender Agent",
    instructions="You are responsible for sending money."
    "When a handoff is made to you, process the transaction with provided sender and receiver details.",
)


# Create Custom Handoff Object
custom_handoff = handoff(
    agent=money_sender_agent,
    on_handoff=on_handoff,
    tool_name_override="send_money_tool",
    tool_description_override="Handles sending money from Umair to Uzair."
)

# Traige Agent that does the handoff
agent = Agent(
    name="TraigeAgent",
    instructions="You are a triage agent. If you cannot handle the task, use the handoff tool.",
    handoffs=[money_sender_agent]
)

# -------------------------
# Main Async Function
# -------------------------
async def main():
    result = await Runner.run(
        agent,
        input="I need to send money to uzair",
        run_config=config
    )
    print(f"\nFinal Output: {result.final_output}")

# -------------------------
# Run the Code
# -------------------------
if __name__ == "__main__":
    asyncio.run(main())
