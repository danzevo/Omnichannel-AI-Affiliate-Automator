# 🤖 Omnichannel AI Affiliate Automation System

## 🚀 Project Overview
An automated, local-first AI system designed to generate high-converting affiliate marketing content for Asian e-commerce marketplaces (Shopee, Tokopedia, TikTok Shop). The system acts as a "smart assistant" where a user can message a Telegram Bot with a simple product URL, and the system automatically scrapes the page, extracts the data, and writes a culturally-tuned, ready-to-post review.

## 📂 Repository Structure
Since this project connects two different environments (n8n orchestration and a Python AI worker), the repository is organized into two main components:

```text
Omnichannel-AI-Affiliate/
│
├── n8n-workflows/
│   └── telegram_affiliate_router.json  # Exported n8n workflow 
│
├── python-worker/
│   ├── app/                            # FastAPI Application
│   │   ├── api/                        # API Routing endpoints
│   │   ├── adapters/                   # Scraper (Browserless) & LLM interfaces
│   │   ├── core/                       # Config and Environment variables
│   │   ├── schemas/                    # Pydantic data models
│   │   └── services/                   # Core business logic and prompt engineering
│   ├── main.py                         # FastAPI entry point
│   └── requirements.txt                # Python dependencies
│
└── README.md                           # This documentation file
```

## 🏗️ Architecture & Tech Stack
*   **Workflow Orchestration:** n8n (Node-based automation)
*   **Backend Worker:** Python 3, FastAPI, Pydantic
*   **Web Scraping:** Browserless (Headless Chromium REST API), BeautifulSoup4
*   **AI / LLM:** Local Llama 3.1 8B (via LM Studio)
*   **Integrations:** Telegram Bot API

## ⚙️ System Flow
1.  **Telegram Trigger:** The user sends a product URL or raw JSON product data to a Telegram Bot.
2.  **Smart Routing (n8n):** A Switch node in n8n detects the payload type.
    *   If **URL**: Routes to the Python worker's `/process-url` endpoint.
    *   If **JSON**: Routes to the Python worker's `/generate-post` endpoint.
3.  **Data Extraction (Browserless):** To bypass complex datacenter anti-bot protections (like Cloudflare) and render JavaScript-heavy e-commerce pages, the Python worker utilizes the Browserless API to fetch the fully-rendered DOM.
4.  **AI Copywriting (Local LLM):** The scraped HTML is passed to Llama 3.1. Through advanced prompt engineering, the LLM is constrained to:
    *   Extract the exact product name, key features, and price from noisy HTML.
    *   Generate an engaging, natural "Soft Sell" review.
    *   Use highly specific Gen-Z Indonesian slang (known locally as "Racun Shopee" style).
    *   Maintain strict negative constraints (e.g., avoiding formal pronouns or literal English translations).
5.  **Omnichannel Delivery:** The generated text is passed back to n8n, which automatically sends the formatted post (complete with emojis, bullet points, and hashtags) back to Telegram.

## 🧠 Key Technical Challenges Solved
*   **Bypassing E-Commerce Anti-Bot:** Successfully circumvented strict scraping protections on Shopee and Tokopedia by transitioning from standard `requests` to a headless Browserless integration, allowing client-side JavaScript to render before extraction.
*   **LLM "Hallucination" Mitigation:** Prevented the 8B local model from inventing fake slang or literally translating English marketing phrases by implementing **Few-Shot Prompting**, strict negative constraints, and precise Temperature tuning (0.3).
*   **Local-First AI:** Eliminated AI API costs and ensured complete data privacy by running Llama 3.1 locally via LM Studio, integrated seamlessly with a lightweight FastAPI backend.

## 🛠️ Setup Instructions

### 1. Python Worker Setup
Navigate to the `python-worker` directory and install dependencies:
```bash
pip install -r requirements.txt
```
Create a `.env` file based on your local configuration and start the server:
```bash
uvicorn app.main:app --reload
```

### 2. n8n Workflow Setup
1. Open your local n8n instance.
2. Click **Import from File** and select `n8n-workflows/telegram_affiliate_router.json`.
3. Configure your Telegram Credentials inside the Telegram Trigger node.
4. Activate the workflow!
