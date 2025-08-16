# browser_agent.py
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor
from llm_agent import generate_answer
import requests
from bs4 import BeautifulSoup


# Browsers to search in parallel
BROWSERS = ["chromium", "firefox", "webkit"]

def search_in_browser(browser_name, query):
    with sync_playwright() as p:
        # Launch browser in visible mode to avoid bot detection
        browser = getattr(p, browser_name).launch(headless=False, args=["--start-maximized"])
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})
        # Spoof navigator.webdriver to look like a real user
        page.evaluate("() => { Object.defineProperty(navigator, 'webdriver', {get: () => undefined}) }")
        
        # Go to Bing search page
        page.goto(f"https://www.bing.com/search?q={query}", timeout=15000)
        page.wait_for_selector('li.b_algo h2 a')
        
        # Extract top 5 links
        results = page.query_selector_all('li.b_algo h2 a')
        links = [r.get_attribute('href') for r in results[:5]]
        
        browser.close()
        return links

def run_parallel_search(query):
    all_results = []
    with ThreadPoolExecutor(max_workers=len(BROWSERS)) as executor:
        futures = [executor.submit(search_in_browser, b, query) for b in BROWSERS]
        for f in futures:
            try:
                all_results.extend(f.result())
            except Exception as e:
                print(f"Error in browser search: {e}")
    return all_results

def fetch_page_text(url):
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)
        return text[:1000]  # Limit length for LLM
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

if __name__ == "__main__":
    query = "Mera gehu ke khet me keede lag gaye hain, kya dawa lagau?"
    results = run_parallel_search(query)
    print("Top search results:", results)

    # Fetch and print page summaries
    summaries = []
    for url in results:
        if "youtube.com" in url:
            print(f"Skipping YouTube link: {url}")
            continue
        summary = fetch_page_text(url)
        print(f"\nSummary for {url}:\n{summary[:500]}...\n")  # Print first 500 chars
        summaries.append(summary)
    
    # Generate answer using LLM
    user_question = "Mera gehu ke khet me keede lag gaye hain, kya dawa lagau?"
    answer = generate_answer(summaries, user_question)
    print("\nLLM Answer:\n", answer)
# ...existing code...