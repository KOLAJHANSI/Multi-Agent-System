from langchain.tools import tool

from ddgs import DDGS

import requests
from bs4 import BeautifulSoup


# ============================================================
# WEB SEARCH TOOL
# ============================================================

@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and relevant information.

    Returns:
    - Page titles
    - URLs
    - Search result snippets
    """

    try:

        search_results = DDGS().text(
            query,
            max_results=5
        )

        if not search_results:
            return "No web search results were found."

        results = []

        for item in search_results:

            title = item.get(
                "title",
                "Untitled"
            )

            url = item.get(
                "href",
                ""
            )

            snippet = item.get(
                "body",
                ""
            )

            results.append(
                f"""
Title: {title}

URL: {url}

Snippet:
{snippet[:500]}
"""
            )

        return "\n-------------------------\n".join(results)

    except Exception as error:

        return (
            "Web search failed.\n"
            f"Error: {str(error)}"
        )


# ============================================================
# WEBPAGE SCRAPING TOOL
# ============================================================

@tool
def scrape_url(url: str) -> str:
    """
    Fetch a webpage and extract readable text
    for deeper research.
    """

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/131.0 Safari/537.36"
                )
            }
        )

        response.raise_for_status()


        # ----------------------------------------------------
        # PARSE HTML
        # ----------------------------------------------------

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        # ----------------------------------------------------
        # REMOVE UNNECESSARY ELEMENTS
        # ----------------------------------------------------

        unwanted_tags = [
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form",
            "noscript"
        ]

        for tag in soup.find_all(unwanted_tags):
            tag.decompose()


        # ----------------------------------------------------
        # EXTRACT TEXT
        # ----------------------------------------------------

        text = soup.get_text(
            separator=" ",
            strip=True
        )


        if not text:

            return (
                "The webpage was accessed, "
                "but no readable text was found."
            )


        # ----------------------------------------------------
        # LIMIT CONTENT
        # ----------------------------------------------------

        return text[:6000]


    except requests.exceptions.Timeout:

        return (
            "Could not scrape the webpage "
            "because the request timed out."
        )


    except requests.exceptions.RequestException as error:

        return (
            "Could not access the webpage.\n"
            f"Error: {str(error)}"
        )


    except Exception as error:

        return (
            "Could not scrape the webpage.\n"
            f"Error: {str(error)}"
        )