from app.adapters.llm_client import LocalLLMClient
from app.adapters.scraper import webScraper
from app.schemas.payload import ProductPayload, UrlPayload
import re

class ContentService:
    SLANG_REPLACEMENT = {
        "mendengarkan": "dengerin",
        "terdengar": "kedengaran",
        "menggunakan": "pake",
        "digunakan": "dipake",
        "dipakai": "dipake", 
        "mengisi": "nge-charge",
        "diisi ulang": "di-charge ulang",
        "merasakan": "ngerasain",
        "ponsel": "HP",
        "telepon genggam": "HP",
        "perangkat": "gadget",
        "membeli": "beli",
        "melihat": "liat",
        "mendapatkan": "dapetin",
        "memiliki": "punya",
        "kasus baterai": "Charging Case",
    }

    def __init__(self):
        self.llm = LocalLLMClient()
        self.scraper = webScraper()

    def _apply_slang_fixes(self, text: str) -> str:
        """Replace formal Indonesian words with Gen-Z slang equivalents."""
        result = text
        for formal, slang in self.SLANG_REPLACEMENT.items():
            # Case-insensitive replacement while preserving sentence flow
            result = re.sub(re.escape(formal), slang, result, flags=re.IGNORECASE)

        return result

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
            "4. Use casual/slang Indonesian verbs. For example use 'dengerin' NOT 'terdengar', use 'ngerasain' NOT 'merasakan', use 'pake' NOT 'menggunakan'. Always prefer informal Gen-Z verb forms. "
            "5. NEVER use formal Indonesian words like 'mendengarkan', 'mengisi', 'daya', 'diisi ulang', 'menggunakan', 'merasakan'. Always replace with slang equivalents like 'dengerin', 'nge-charge', 'pake', 'ngerasain'. "
            "6. Keep paragraphs short, punchy, and use emojis. "
            "7. You MUST include the actual Price of the product in the text! "
            "8. Always end with a clear Call to Action and the link. "
            "9. Generate 5 hashtags at the bottom. "
            "10. Start directly with an Indonesian hook like 'Spill racun baru nih guys...' or 'Wah nemu harta karun...'.\n\n"
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
        raw_text = self.llm.generate_text(system_prompt, user_prompt)
        
        return self._apply_slang_fixes(raw_text)
    
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
            "4. Use casual/slang Indonesian verbs. For example use 'dengerin' NOT 'terdengar', use 'ngerasain' NOT 'merasakan', use 'pake' NOT 'menggunakan'. Always prefer informal Gen-Z verb forms. "
            "5. NEVER use formal Indonesian words like 'mendengarkan', 'mengisi', 'daya', 'diisi ulang', 'menggunakan', 'merasakan'. Always replace with slang equivalents like 'dengerin', 'nge-charge', 'pake', 'ngerasain'. "
            "6. Keep paragraphs short, punchy, and use emojis. "
            "7. You MUST include the actual Price of the product in the text! "
            "8. Always end with a clear Call to Action and the link. "
            "9. Generate 5 hashtags at the bottom. "
            "10. Start directly with an Indonesian hook like 'Spill racun baru nih guys...' or 'Wah nemu harta karun...'.\n\n"
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

        raw_text = self.llm.generate_text(system_prompt, user_prompt)

        return self._apply_slang_fixes(raw_text)