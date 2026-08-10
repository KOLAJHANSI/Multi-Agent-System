from agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain
)


# ============================================================
# RESEARCH PIPELINE
# ============================================================

def run_research_pipeline(topic: str) -> dict:

    state = {}

    print("\n" + "=" * 60)
    print("RESEARCHOS — MULTI-AGENT RESEARCH PIPELINE")
    print("=" * 60)

    print(f"\nResearch Topic: {topic}")


    # ========================================================
    # STEP 1 — SEARCH AGENT
    # ========================================================

    print("\n" + "-" * 60)
    print("STEP 1 — SEARCH AGENT")
    print("-" * 60)

    try:

        search_agent = build_search_agent()

        search_result = search_agent.invoke({
            "messages": [
                (
                    "user",
                    f"""
                    Find recent, reliable and detailed information
                    about the following research topic:

                    {topic}

                    Use the available web search tool.

                    Return:
                    - Relevant information
                    - Important findings
                    - Source titles
                    - Source URLs

                    Prefer reliable and recent sources.
                    """
                )
            ]
        })

        state["search_results"] = (
            search_result["messages"][-1].content
        )

        print("\n✓ Search Agent completed.")

    except Exception as e:

        print(f"\n✗ Search Agent failed: {e}")

        state["search_results"] = (
            f"Search Agent failed: {str(e)}"
        )


    # ========================================================
    # STEP 2 — READER AGENT
    # ========================================================

    print("\n" + "-" * 60)
    print("STEP 2 — READER AGENT")
    print("-" * 60)

    try:

        reader_agent = build_reader_agent()

        reader_result = reader_agent.invoke({
            "messages": [
                (
                    "user",
                    f"""
                    We are researching the following topic:

                    {topic}

                    Here are the search results:

                    {state["search_results"][:4000]}

                    Identify the most relevant URL from the
                    search results.

                    Then use the scrape_url tool to read that
                    webpage.

                    Extract useful factual information that
                    can help prepare a research report.
                    """
                )
            ]
        })

        state["scraped_content"] = (
            reader_result["messages"][-1].content
        )

        print("\n✓ Reader Agent completed.")

    except Exception as e:

        print(f"\n✗ Reader Agent failed: {e}")

        state["scraped_content"] = (
            f"Reader Agent failed: {str(e)}"
        )


    # ========================================================
    # STEP 3 — WRITER CHAIN
    # ========================================================

    print("\n" + "-" * 60)
    print("STEP 3 — WRITER")
    print("-" * 60)

    try:

        research_combined = (
            f"""
            SEARCH RESULTS:

            {state["search_results"]}


            ================================================


            DETAILED SCRAPED CONTENT:

            {state["scraped_content"]}
            """
        )

        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined
        })

        print("\n✓ Writer completed.")

    except Exception as e:

        print(f"\n✗ Writer failed: {e}")

        state["report"] = (
            f"Writer failed: {str(e)}"
        )


    # ========================================================
    # STEP 4 — CRITIC CHAIN
    # ========================================================

    print("\n" + "-" * 60)
    print("STEP 4 — CRITIC")
    print("-" * 60)

    try:

        state["feedback"] = critic_chain.invoke({
            "report": state["report"]
        })

        print("\n✓ Critic completed.")

    except Exception as e:

        print(f"\n✗ Critic failed: {e}")

        state["feedback"] = (
            f"Critic failed: {str(e)}"
        )


    # ========================================================
    # PIPELINE COMPLETE
    # ========================================================

    print("\n" + "=" * 60)
    print("RESEARCH PIPELINE COMPLETED")
    print("=" * 60)

    print("\nFINAL REPORT:\n")
    print(state["report"])

    print("\n" + "-" * 60)
    print("CRITIC FEEDBACK:\n")
    print(state["feedback"])

    return state


# ============================================================
# TERMINAL ENTRY POINT
# ============================================================

if __name__ == "__main__":

    topic = input(
        "\nEnter a research topic: "
    ).strip()

    if not topic:

        print(
            "\nPlease enter a valid research topic."
        )

    else:

        run_research_pipeline(topic)