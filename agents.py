from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, scrape_url


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GROQ LLM SETUP
# ============================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


# ============================================================
# SEARCH AGENT
# ============================================================

def build_search_agent():

    return create_agent(
        model=llm,
        tools=[web_search]
    )


# ============================================================
# READER AGENT
# ============================================================

def build_reader_agent():

    return create_agent(
        model=llm,
        tools=[scrape_url]
    )


# ============================================================
# WRITER CHAIN
# ============================================================

writer_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        """
        You are an expert research writer.

        Write clear, structured, factual,
        and insightful research reports.

        Use only the research information provided.
        Do not invent facts, statistics, or sources.
        """
    ),

    (
        "human",
        """
        Write a detailed research report on the topic below.

        Topic:
        {topic}

        Research Gathered:
        {research}

        Structure the report as:

        # Introduction

        # Key Findings
        - Finding 1
        - Finding 2
        - Finding 3

        # Conclusion

        # Sources
        - List all relevant URLs found in the research.

        Requirements:
        - Be detailed and professional.
        - Explain the important findings clearly.
        - Use factual information from the research.
        - Do not invent facts.
        - Do not invent URLs or sources.
        """
    )

])


writer_chain = (
    writer_prompt
    | llm
    | StrOutputParser()
)


# ============================================================
# CRITIC CHAIN
# ============================================================

critic_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        """
        You are a sharp and constructive research critic.

        Evaluate research reports honestly and specifically.

        Focus on:
        - Factual quality
        - Completeness
        - Clarity
        - Structure
        - Source quality
        - Possible unsupported claims
        """
    ),

    (
        "human",
        """
        Review the research report below and evaluate it strictly.

        Report:
        {report}

        Respond in exactly this format:

        Score: X/10

        Strengths:
        - ...
        - ...

        Areas to Improve:
        - ...
        - ...

        One line verdict:
        ...
        """
    )

])


critic_chain = (
    critic_prompt
    | llm
    | StrOutputParser()
)