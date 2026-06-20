# backend.py
import os
from crewai import Agent, Crew, Process, Task
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Use faster model for better speed
llm = ChatOpenAI(
    model="gpt-4o-mini",      # Faster & cheaper than gpt-4o
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# ==================== AGENTS ====================
market_research_agent = Agent(
    role="Market Research Agent",
    goal="Find trending products on Meesho for women ethnic wear.",
    backstory="Expert in Indian fashion trends and Meesho market.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

content_agent = Agent(
    role="Content Agent",
    goal="Create attractive WhatsApp marketing messages.",
    backstory="Creative content writer for Meesho resellers.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

pricing_agent = Agent(
    role="Pricing Agent",
    goal="Suggest profitable yet competitive pricing.",
    backstory="Expert in pricing strategy for online resellers.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

def create_crew(user_query: str):
    research_task = Task(
        description=f"Analyze trending products for: {user_query}",
        expected_output="List of trending products with reasons.",
        agent=market_research_agent
    )

    content_task = Task(
        description=f"Create 2 attractive WhatsApp messages for: {user_query}",
        expected_output="Numbered list of ready WhatsApp messages.",
        agent=content_agent
    )

    pricing_task = Task(
        description=f"Suggest best pricing for products in: {user_query}",
        expected_output="Recommended price range with reasoning.",
        agent=pricing_agent
    )

    crew = Crew(
        agents=[market_research_agent, content_agent, pricing_agent],
        tasks=[research_task, content_task, pricing_task],
        process=Process.sequential,
        verbose=1
    )
    return crew