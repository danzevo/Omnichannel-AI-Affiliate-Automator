from app.adapters.llm_client import LocalLLMClient
from app.adapters.scraper import webScraper
from app.schemas.payload import ProductPayload, UrlPayload

class ContentService:
    def __init__(self):
        self.llm = LocalLLMClient()
        self.scraper = webScraper()

    def create_telegram_post(self, product: ProductPayload) -> str:
        system_prompt = (
            "You are a Gen-Z affiliate marketer and influencer from Indonesia. "
            "I will give you raw, messy text scraped from a product page. "
            "Your job is to find the product name, price, and description from the text, "
            "and then write a highly engaging, viral 'Racun Shopee' style social media post. "
            "CRITICAL RULES: "
            "1. NEVER use the words 'Saya', 'Kamu', 'Anda', 'Teman-teman', 'Gue', or 'Lo'. "
            "2. DO USE words like 'Aku' (for yourself), 'Kalian' or 'Bestie' (for the audience). "
            "3. Do NOT translate technology words. Always use the English words for 'Charging Case', 'Power Bank', 'Earbuds', 'Wireless', etc. (Never say 'Kasus Baterai'). "
            "4. Keep paragraphs short, punchy, and use emojis. "
            "5. You MUST include the actual Price of the product in the text! "
            "6. Always end with a clear Call to Action and the link. "
            "7. Generate 5 hashtags at the bottom. "
            "8. Start directly with an Indonesian hook like 'Spill racun baru nih guys...' or 'Wah nemu harta karun...'.\n\n"
            "EXAMPLE VIBE/TONE:\n"
            "Spill racun baru nih guys, aku baru nemu barang sebagus ini harganya cuma [INSERT EXACT PRICE]! 💸\n\n"
            "Kualitasnya oke banget buat dipakai sehari-hari. Fitur andalannya:\n"
            "✅ Desain super premium\n"
            "✅ Baterai awet seharian\n\n"
            "Asli ini keren banget, wajib banget kalian checkout sekarang sebelum kehabisan! Langsung klik link ini ya:\n"
            "👉 [link]"
        )

        user_prompt = f"""
            Please create a universal social media post for this product found on {product.marketplace}:
            - Product: {product.product_name}
            - Price: {product.price}
            - Details: {product.product_description}
            - Link: {product.affiliate_link}
            """
        
        return self.llm.generate_text(system_prompt, user_prompt)
    
    def create_post_from_url(self, payload: UrlPayload) -> str:
        # 1. Decide which scraper to use dynamically!
        if payload.scraper_type == "playwright":            
            raw_website_text = self.scraper.scrape_with_playwright(payload.url)
        elif payload.scraper_type == "browserless":
            raw_website_text = self.scraper.scrape_with_browserless(payload.url)
        else:
            raw_website_text = self.scraper.scrape_with_bs4(payload.url)

        # 2. Tell the LLM to extract the data AND write the post
        system_prompt = (
            "You are a Gen-Z affiliate marketer and influencer from Indonesia. "
            "I will give you raw, messy text scraped from a product page. "
            "Your job is to find the product name, price, and description from the text, "
            "and then write a highly engaging, viral 'Racun Shopee' style social media post. "
            "CRITICAL RULES: "
            "1. NEVER use the words 'Saya', 'Kamu', 'Anda', 'Teman-teman', 'Gue', or 'Lo'. "
            "2. DO USE words like 'Aku' (for yourself), 'Kalian' or 'Bestie' (for the audience). "
            "3. Do NOT translate technology words. Always use the English words for 'Charging Case', 'Power Bank', 'Earbuds', 'Wireless', etc. (Never say 'Kasus Baterai'). "
            "4. Keep paragraphs short, punchy, and use emojis. "
            "5. You MUST include the actual Price of the product in the text! "
            "6. Always end with a clear Call to Action and the link. "
            "7. Generate 5 hashtags at the bottom. "
            "8. Start directly with an Indonesian hook like 'Spill racun baru nih guys...' or 'Wah nemu harta karun...'.\n\n"
            "EXAMPLE VIBE/TONE:\n"
            "Spill racun baru nih guys, aku baru nemu barang sebagus ini harganya cuma [INSERT EXACT PRICE]! 💸\n\n"
            "Kualitasnya oke banget buat dipakai sehari-hari. Fitur andalannya:\n"
            "✅ Desain super premium\n"
            "✅ Baterai awet seharian\n\n"
            "Asli ini keren banget, wajib banget kalian checkout sekarang sebelum kehabisan! Langsung klik link ini ya:\n"
            "👉 [link]"
        )

        # We limit the text to 3000 characters so we don't crash your local LLM
        user_prompt = f"""
        Please extract the product details and create a universal social media post for this product found on {payload.marketplace}:
        - Affiliate Link: {payload.url}
            
        RAW SCRAPED TEXT:
        {raw_website_text[:3000]}
        """

        return self.llm.generate_text(system_prompt, user_prompt)