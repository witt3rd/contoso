from fastapi import FastAPI, Query

# Removed List, Dict, Any from typing
from fuzzywuzzy import process
from pydantic import BaseModel

app = FastAPI()


# Pydantic model for individual product data
class ProductData(BaseModel):
    id: int
    name: str
    description: str


# Pydantic model for search results
class ProductMatch(BaseModel):
    id: int
    name: str
    description: str
    score: int


# Sample product data (now typed for clarity, though FastAPI will use models for I/O)
products: list[ProductData] = [  # Changed to built-in list
    ProductData(
        id=1, name="Widget A", description="A high-quality widget for everyday use."
    ),
    ProductData(
        id=2, name="Widget B", description="An advanced widget with extra features."
    ),
    ProductData(
        id=3,
        name="Gadget X",
        description="A versatile gadget for various applications.",
    ),
]


# Endpoint to search products by name or description
@app.get("/search_products/")
async def search_products(
    query: str = Query(..., description="Search query for product name or description"),
) -> list[ProductMatch]:  # Changed to built-in list
    """
    Search for products by name or description using fuzzy matching.
    Returns a list of potential matches with confidence scores.
    """
    # Use attributes from ProductData instances
    all_texts = [p.name + " " + p.description for p in products]
    matches = process.extract(query, all_texts, limit=5)
    result: list[ProductMatch] = []  # Changed to built-in list
    for match_item in matches:  # Renamed 'match' to 'match_item' to avoid conflict
        # Safely unpack, ignoring potential extra elements from fuzzywuzzy
        text, score, *_ = match_item
        # Find the original product
        # This search logic could be improved if all_texts could map back to ProductData more directly
        # For now, we find by matching the concatenated text
        original_product: ProductData | None = None
        for p in products:
            if (p.name + " " + p.description) == text:
                original_product = p
                break

        if original_product:
            result.append(
                ProductMatch(
                    id=original_product.id,
                    name=original_product.name,
                    description=original_product.description,
                    score=int(score),  # Ensure score is int
                )
            )
    return result


# Endpoint to get product details by ID
@app.get("/product/{product_id}")
async def get_product(
    product_id: int,
) -> ProductData | dict[str, str]:  # Changed to built-in dict
    """
    Get product details by ID.
    """
    for product in products:
        if product.id == product_id:  # Access by attribute
            return product
    return {"error": "Product not found"}
