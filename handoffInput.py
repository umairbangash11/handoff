import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, handoff, RunContextWrapper
from agents.run import RunConfig
from openai import AsyncOpenAI
from pydantic import BaseModel
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

class EscalationData(BaseModel):
    reason: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: EscalationData):
    print(f"Escalation agent called with reason: {input_data.reason}")

agent = Agent(name="Escalation agent")

handoff_obj = handoff(
    agent=agent,
    on_handoff=on_handoff,
    input_type=EscalationData,
    
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="You are a triage agent. If you cannot handle the task, use the handoff tool.",
    handoffs=[handoff_obj]
)

async def main():
    result = await Runner.run(
        triage_agent,
        input="I need a reason why my info is not in escalation",
        run_config=config
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
