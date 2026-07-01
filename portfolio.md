# 🤖 Omnichannel AI Affiliate Automation System
*(Role: Automation Engineer & AI Integrator)*

## 📸 System Interface
`[ ➔ INSERT SCREENSHOT HERE ]`  
*(Tip: Take a screenshot of the completed n8n workflow canvas showing the Telegram Trigger, the Switch node routing logic, and the HTTP requests to your Python backend. Include a screenshot of the generated Telegram post!)*

---

## 💡 The Problem
Affiliate marketing on Asian e-commerce platforms (like Shopee and Tokopedia) is highly lucrative but intensely manual. Marketers spend hours manually copying product details, fighting aggressive anti-bot protections to scrape prices, and writing culturally relevant, engaging social media copy. Existing automation tools fail because modern marketplaces heavily obfuscate their data using client-side JavaScript, and generic AI models sound too formal and robotic when translating English marketing copy into local slang like "Racun Shopee."

## 🎯 The Solution
I engineered a fully autonomous, local-first AI copywriting system using n8n and Python. The system acts as a "smart assistant" accessible via Telegram. When a user sends a Shopee or Tokopedia link to the bot, an n8n workflow intelligently routes the request to a custom Python FastAPI backend. The backend utilizes the Browserless API to bypass complex datacenter anti-bot protections and render the JavaScript-heavy DOM. Finally, the extracted raw text is passed to a local LLaMA 3.1 8B model. Through advanced prompt engineering and strict negative constraints, the LLM generates a highly engaging, perfectly formatted "Soft Sell" review using authentic Gen-Z Indonesian slang, which is automatically posted back to the user's social channels.

---

## 🛠️ The Tech Stack
* **Automation Platform:** n8n (Node-based orchestration)
* **Backend API:** Python 3, FastAPI, Pydantic
* **Web Scraping:** Browserless (Headless Chromium REST API), BeautifulSoup4
* **AI / ML:** Local LLaMA 3.1 8B Instruct, LM Studio (Zero-Data-Leakage)
* **Integrations:** Telegram Bot API

---

## 🏗️ Engineering & Architecture Highlights

### 1. Intelligent Multi-Path Routing
Designed an event-driven n8n workflow utilizing a Switch node and inline JavaScript ternary operators. The system automatically detects the incoming payload (JSON vs URL) and the specific marketplace (Shopee, Tokopedia, or TikTok Shop), intelligently routing the payload to the appropriate FastAPI endpoint (`/generate-post` or `/process-url`).

### 2. Bypassing E-Commerce Anti-Bot Protections
Successfully circumvented strict scraping protections on Shopee and Tokopedia by transitioning from standard `requests` to a headless Browserless integration. This allows client-side JavaScript to render before extraction, defeating obfuscation techniques and CAPTCHAs without managing complex local browser environments.

### 3. LLM "Hallucination" Mitigation & Prompt Engineering
Prevented the 8B local model from inventing fake slang or literally translating English marketing phrases by implementing **Few-Shot Prompting**, strict negative constraints (e.g., banning formal pronouns like 'Saya' and 'Kamu'), and precise Temperature tuning (0.3). The AI successfully maintains English technology terms (like "Charging Case") while speaking authentic local slang.

### 4. Local-First AI & Zero API Costs
Eliminated commercial AI API costs and ensured complete data privacy by running Llama 3.1 locally via LM Studio, seamlessly integrated with the lightweight Python FastAPI backend.

---

## 📂 Repository Structure
*   `n8n-workflows/` - Contains the exported `telegram_affiliate_router.json` workflow.
*   `app/` - The Python FastAPI backend (routers, schemas, scraper adapters).

---

## 🔗 Links
* **[GitHub Repository / Demo Video]** -> `[Insert Link Here]`
