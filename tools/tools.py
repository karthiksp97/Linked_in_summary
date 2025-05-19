from langchain_tavily import TavilySearch




def get_profile_url_tavily(name:str):
    search = TavilySearch(tavily_api_key="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")
    res = search.run(f"{name}")
    for r in res["results"]:
        if "linkedin.com" in r["url"]:
            return r["url"]  # ✅ Clean string
    return "No LinkedIn URL found."