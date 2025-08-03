import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
from pydantic import BaseModel
from openai import AsyncOpenAI
from agents import enable_verbose_stdout_logging

enable_verbose_stdout_logging()
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.5-flash",
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=False
)

# billing_agent = Agent(
#     name="Billing Agent",
#     instructions="You handle all billing-related queries."
# )

math = Agent(
    name="MathAgent",
    instructions="you handle math related querries",
)

piaic = Agent(
    name="PiaicAgent",
    instructions="you handle piaic related querries",
)

# refund_agent = Agent(
#     name="Refund Agent",
#     instructions="You handle refund-related queries.",
    
# )

# Main Triage Agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="You are a triage agent. If the query is about math, hand it off to math."
    "If it’s about piaic, hand off to piaic.",
    handoffs=[math, piaic],
    )

async def main():
    result = await Runner.run(
        triage_agent,
        input="what is 2 + 2?.",
        run_config=config,
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

