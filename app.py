import streamlit as st

from agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResearchOS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "research_started" not in st.session_state:
    st.session_state.research_started = False


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #050505;
        color: #eeeeee;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    [data-testid="stHeader"] {
        background: #050505;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ---------- SIDEBAR ---------- */

    [data-testid="stSidebar"] {
        background: #0a0a0a;
        border-right: 1px solid #222222;
    }

    [data-testid="stSidebar"] * {
        color: #dddddd;
    }


    /* ---------- TEXT ---------- */

    h1, h2, h3 {
        color: #f5f5f5 !important;
    }

    p {
        color: #a5a5a5;
    }


    /* ---------- INPUT ---------- */

    .stTextInput input {
        background: #101010 !important;
        color: #ffffff !important;

        border: 1px solid #303030 !important;
        border-radius: 10px !important;

        padding: 14px !important;
    }

    .stTextInput input:focus {
        border-color: #777777 !important;
        box-shadow: none !important;
    }


    /* ---------- BUTTON ---------- */

    .stButton button {
        width: 100%;

        background: #f2f2f2 !important;
        color: #050505 !important;

        border: none !important;
        border-radius: 9px !important;

        min-height: 45px;

        font-weight: 700;

        transition: 0.2s ease;
    }

    .stButton button:hover {
        background: #ffffff !important;
        transform: translateY(-1px);
    }


    /* ---------- SECONDARY BUTTONS ---------- */

    [data-testid="stDownloadButton"] button {
        background: #111111 !important;
        color: #eeeeee !important;

        border: 1px solid #333333 !important;
        border-radius: 8px !important;
    }


    /* ---------- EXPANDERS ---------- */

    [data-testid="stExpander"] {
        background: #0b0b0b !important;
        border: 1px solid #242424 !important;
        border-radius: 10px !important;
    }


    /* ---------- STATUS ---------- */

    [data-testid="stStatusWidget"] {
        background: #0b0b0b !important;
        border: 1px solid #292929 !important;
        border-radius: 12px !important;
    }


    /* ---------- DIVIDER ---------- */

    hr {
        border-color: #222222 !important;
    }


    /* ---------- METRICS ---------- */

    [data-testid="stMetric"] {
        background: #0b0b0b;
        border: 1px solid #242424;
        border-radius: 10px;
        padding: 15px;
    }


    /* ---------- CODE ---------- */

    code {
        background: #111111 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🧠 ResearchOS")

    st.caption("MULTI-AGENT RESEARCH SYSTEM")

    st.divider()

    st.subheader("Research Pipeline")

    st.write("🔎  Search Agent")
    st.caption("Finds relevant web sources")

    st.write("📖  Reader Agent")
    st.caption("Reads and extracts useful content")

    st.write("✍️  Writer Agent")
    st.caption("Creates the research report")

    st.write("🧠  Critic Agent")
    st.caption("Reviews the final answer")

    st.divider()

    st.subheader("System")

    st.success("System ready")

    st.caption("Web search enabled")
    st.caption("Source scraping enabled")
    st.caption("Multi-agent workflow enabled")

    st.divider()

    st.caption("ResearchOS v1.0")


# ============================================================
# TOP BAR
# ============================================================

top_left, top_right = st.columns([5, 1])

with top_left:

    st.title("AI Research Workspace")

    st.caption(
        "Turn a research question into a structured, "
        "source-backed report using specialized AI agents."
    )




st.divider()


# ============================================================
# RESEARCH INPUT
# ============================================================

st.subheader("Start a Research Mission")

st.write(
    "Enter a topic. The system will search, read, write and critique automatically."
)

topic = st.text_input(
    "Research topic",
    placeholder="Example: How AI agents are changing software development in 2026",
    label_visibility="collapsed"
)


# ============================================================
# QUICK TOPICS
# ============================================================

st.caption("SUGGESTED TOPICS")

q1, q2, q3, q4 = st.columns(4)

with q1:
    st.info("Generative AI")

with q2:
    st.info("AI Agents")

with q3:
    st.info("Quantum Computing")

with q4:
    st.info("Cybersecurity")


st.write("")


run = st.button(
    "🚀  EXECUTE RESEARCH",
    use_container_width=True
)


# ============================================================
# AGENT PIPELINE DISPLAY
# ============================================================

st.divider()

st.subheader("Agent Network")

a1, a2, a3, a4 = st.columns(4)

with a1:

    st.metric(
        "01 · SEARCH",
        "READY"
    )

    st.caption(
        "Searches the web for recent and relevant information."
    )

with a2:

    st.metric(
        "02 · READ",
        "READY"
    )

    st.caption(
        "Selects and scrapes useful sources for deeper research."
    )

with a3:

    st.metric(
        "03 · WRITE",
        "READY"
    )

    st.caption(
        "Combines the research into a structured report."
    )

with a4:

    st.metric(
        "04 · CRITIC",
        "READY"
    )

    st.caption(
        "Evaluates the report for quality and completeness."
    )


# ============================================================
# RESEARCH EXECUTION
# ============================================================

if run:

    if not topic.strip():

        st.error(
            "Please enter a research topic before starting."
        )

    else:

        st.session_state.research_started = True

        result = {}

        st.divider()

        st.subheader("Live Agent Activity")

        with st.status(
            "Research mission in progress...",
            expanded=True
        ) as status:

            # ==================================================
            # SEARCH AGENT
            # ==================================================

            st.write(
                "🔎 **Search Agent:** searching the web..."
            )

            search_agent = build_search_agent()

            search_result = search_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            f"""
                            Find recent, reliable and detailed
                            information about:

                            {topic}

                            Search the web and return useful
                            sources with URLs and relevant details.
                            """
                        )
                    ]
                }
            )

            result["search"] = (
                search_result["messages"][-1].content
            )

            st.write(
                "✅ Search Agent completed."
            )


            # ==================================================
            # READER AGENT
            # ==================================================

            st.write(
                "📖 **Reader Agent:** reading the best source..."
            )

            reader_agent = build_reader_agent()

            reader_result = reader_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            f"""
                            Research topic:

                            {topic}

                            Below are the search results:

                            {result["search"][:3000]}

                            Identify the most relevant URL
                            and use the scrape_url tool to
                            extract deeper useful information.
                            """
                        )
                    ]
                }
            )

            result["reader"] = (
                reader_result["messages"][-1].content
            )

            st.write(
                "✅ Reader Agent completed."
            )


            # ==================================================
            # WRITER
            # ==================================================

            st.write(
                "✍️ **Writer Agent:** creating the report..."
            )

            combined_research = (
                f"""
                SEARCH RESULTS:

                {result["search"]}

                ------------------------------

                SCRAPED CONTENT:

                {result["reader"]}
                """
            )

            result["report"] = writer_chain.invoke(
                {
                    "topic": topic,
                    "research": combined_research
                }
            )

            st.write(
                "✅ Writer Agent completed."
            )


            # ==================================================
            # CRITIC
            # ==================================================

            st.write(
                "🧠 **Critic Agent:** reviewing the report..."
            )

            result["feedback"] = critic_chain.invoke(
                {
                    "report": result["report"]
                }
            )

            st.write(
                "✅ Critic Agent completed."
            )


            status.update(
                label="Research mission completed",
                state="complete"
            )


        st.session_state.result = result


# ============================================================
# RESULTS
# ============================================================

if st.session_state.result:

    result = st.session_state.result

    st.divider()

    st.subheader("Research Intelligence")

    st.caption(
        f"FINAL REPORT · {topic}"
    )

    # --------------------------------------------------------
    # SUMMARY METRICS
    # --------------------------------------------------------

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "Search",
            "Completed"
        )

    with m2:
        st.metric(
            "Deep Reading",
            "Completed"
        )

    with m3:
        st.metric(
            "Critical Review",
            "Completed"
        )


    st.write("")


    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    st.subheader("📄 Final Research Report")

    st.markdown(
        result["report"]
    )


    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    st.download_button(
        label="⬇️ Download Report",
        data=result["report"],
        file_name="research_report.md",
        mime="text/markdown"
    )


    # --------------------------------------------------------
    # CRITIC
    # --------------------------------------------------------

    st.divider()

    st.subheader("🧠 Critic Analysis")

    st.info(
        result["feedback"]
    )


    # --------------------------------------------------------
    # EVIDENCE
    # --------------------------------------------------------

    st.divider()

    st.subheader("🔍 Research Evidence")

    with st.expander(
        "Search Agent — Web Research"
    ):

        st.write(
            result["search"]
        )

    with st.expander(
        "Reader Agent — Extracted Source Content"
    ):

        st.write(
            result["reader"]
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "RESEARCHOS  •  LANGCHAIN  •  TAVILY  •  GROQ  •  MULTI-AGENT AI"
)