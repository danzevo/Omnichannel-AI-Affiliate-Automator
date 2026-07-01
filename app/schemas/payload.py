from pydantic import BaseModel
from typing import Optional

class ProductPayload(BaseModel):
    product_name: str
    product_description: str
    price: str
    affiliate_link: str
    marketplace: str

class PostResponse(BaseModel):
    telegram_post: str

class UrlPayload(BaseModel):
    url: str
    marketplace: str
    scraper_type: Optional[str] = "beautifulsoup" # Can be "playwright" or "beautifulsoup"
    