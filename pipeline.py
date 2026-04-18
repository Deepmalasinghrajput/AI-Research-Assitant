from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
from rag_store import search_db, add_to_db


def run_research_pipeline(topic: str) -> dict:

    state = {}

    # =========================
    # STEP 1 - SEARCH AGENTwhat
    # =========================
    print("\n" + "=" * 50)
    print("step 1 - search agent is working ...")
    print("=" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })

    state["search_results"] = search_result['messages'][-1].content
    print("\n🔎 Search result:\n", state['search_results'])


    # =========================
    # STEP 2 - READER AGENT
    # =========================
    print("\n" + "=" * 50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("=" * 50)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })

    messages = reader_result.get("messages", [])

    if messages and hasattr(messages[-1], "content"):
        state["scraped_content"] = messages[-1].content
    else:
        print("⚠️ Scraping failed, using search fallback")
        state["scraped_content"] = state["search_results"]

    print("\n📄 Scraped content:\n", state["scraped_content"][:1000])


    # =========================
    # 🔥 STEP 2.2 - STORE IN RAG DB
    # =========================
    print("\n📦 Storing scraped content into ChromaDB...")

    try:
        # basic filter (avoid junk / empty data)
        if state["scraped_content"] and len(state["scraped_content"]) > 100:
            add_to_db(
                state["scraped_content"],
                meta={"source": "web", "topic": topic}
            )
            print("✅ Stored in ChromaDB")
        else:
            print("⚠️ Content too small, skipped storing")

    except Exception as e:
        print("⚠️ Error storing in DB:", e)


    # =========================
    # STEP 2.5 - RAG RETRIEVAL
    # =========================
    print("\n" + "=" * 50)
    print("step 2.5 - RAG retrieval layer running...")
    print("=" * 50)

    rag_context = search_db(topic)
    state["rag_context"] = rag_context

    print("\n🧠 RAG Context:\n", rag_context)


    # =========================
    # STEP 3 - WRITER
    # =========================
    print("\n" + "=" * 50)
    print("step 3 - Writer is drafting the report ...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"SCRAPED CONTENT:\n{state['scraped_content']}\n\n"
        f"RAG MEMORY:\n{state['rag_context']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\n📝 Final Report:\n", state['report'])


    # =========================
    # STEP 4 - CRITIC
    # =========================
    print("\n" + "=" * 50)
    print("step 4 - critic is reviewing the report")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state['report']
    })

    print("\n📊 Critic Report:\n", state['feedback'])

    return state


if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)