# Handoff - AI Agent Handoff System

A Python project demonstrating AI agent handoff capabilities using the `openai-agents` library with Google Gemini integration. This project showcases different approaches to implementing agent handoffs, from basic triage systems to advanced custom handoff functions with input filtering and prompt optimization.

## 🚀 Features

- **Multi-Agent Triage System**: Route queries to specialized agents based on content
- **Custom Handoff Functions**: Execute custom logic when handoffs occur
- **Input Filtering**: Clean conversation history during handoffs
- **Structured Data Handoffs**: Pass typed data between agents
- **Prompt Optimization**: Automatic prompt enhancement for better handoff performance
- **Gemini Integration**: Uses Google's Gemini 2.5 Flash model

## 📁 Project Structure

```
handoff/
├── main.py              # Basic triage agent with math and PIAIC agents
├── custom_handoff.py    # Custom handoff function with callback
├── handoffInput.py      # Structured data handoffs with Pydantic models
├── input_filters.py     # Input filtering during handoffs
├── prompt.py            # Prompt optimization techniques
├── pyproject.toml       # Project dependencies
└── README.md           # This file
```

## 🛠️ Setup

### Prerequisites

- Python 3.12 or higher
- Google Gemini API key

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd handoff
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## 📖 Usage Examples

### 1. Basic Triage Agent (`main.py`)

Simple agent handoff system that routes queries to specialized agents:

```python
# Math queries → MathAgent
# PIAIC queries → PiaicAgent
python main.py
```

### 2. Custom Handoff Function (`custom_handoff.py`)

Demonstrates custom callback functions during handoffs:

```python
def on_handoff(ctx: RunContextWrapper[None]):
    print("Handoff was called successfully!")

# Usage
python custom_handoff.py
```

### 3. Structured Data Handoffs (`handoffInput.py`)

Shows how to pass typed data between agents using Pydantic models:

```python
class EscalationData(BaseModel):
    reason: str

# Usage
python handoffInput.py
```

### 4. Input Filtering (`input_filters.py`)

Demonstrates cleaning conversation history during handoffs:

```python
# Removes tool calls from conversation history
custom_handoff = handoff(
    agent=faq_agent,
    input_filter=handoff_filters.remove_all_tools
)

# Usage
python input_filters.py
```

### 5. Prompt Optimization (`prompt.py`)

Shows two methods for optimizing prompts for better handoff performance:

- **Method 1**: Manual prompt prefix addition
- **Method 2**: Automatic prompt enhancement

```python
# Usage
python prompt.py
```

## 🔧 Configuration

### Model Configuration

The project uses Google Gemini 2.5 Flash model:

```python
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.5-flash",
)
```

### Run Configuration

```python
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=False
)
```

## 🎯 Key Concepts

### Agent Handoffs

Agent handoffs allow one agent to transfer control to another agent when it encounters queries outside its expertise:

```python
triage_agent = Agent(
    name="Triage Agent",
    instructions="Route queries to appropriate specialized agents",
    handoffs=[math_agent, piaic_agent]
)
```

### Custom Handoff Functions

Execute custom logic when handoffs occur:

```python
def on_handoff(ctx: RunContextWrapper[None]):
    print("Custom handoff logic executed!")

custom_handoff = handoff(
    agent=specialized_agent,
    on_handoff=on_handoff
)
```

### Input Filtering

Clean conversation history during handoffs:

```python
custom_handoff = handoff(
    agent=faq_agent,
    input_filter=handoff_filters.remove_all_tools
)
```

### Structured Data

Pass typed data between agents:

```python
class EscalationData(BaseModel):
    reason: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: EscalationData):
    print(f"Escalation reason: {input_data.reason}")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [openai-agents](https://github.com/openai/agents) library
- Powered by Google Gemini 2.5 Flash model
- Inspired by modern AI agent architectures

## 📞 Support

For questions or issues, please open an issue on the GitHub repository.
