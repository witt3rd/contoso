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
    inventory_level: int


# Pydantic model for search results
class ProductMatch(BaseModel):
    id: int
    name: str
    description: str
    score: int


# Sample product data (now typed for clarity, though FastAPI will use models for I/O)
products: list[ProductData] = [  # Changed to built-in list
    ProductData(
        id=1,
        name="Widget A",
        description="A high-quality widget for everyday use.",
        inventory_level=100,
    ),
    ProductData(
        id=2,
        name="Widget B",
        description="An advanced widget with extra features.",
        inventory_level=50,
    ),
    ProductData(
        id=3,
        name="Gadget X",
        description="A versatile gadget for various applications.",
        inventory_level=75,
    ),
]


# Endpoint to search products by name or description
@app.get("/search_products/")
async def search_products(
    query: str = Query(..., description="Search query for product name or description"),
    threshold: int = Query(
        80, ge=0, le=100, description="Minimum score threshold for a match"
    ),
    max_results: int | None = Query(
        None, gt=0, description="Maximum number of results to return. If None, all matches above threshold are returned, sorted by score."
    ),
) -> list[ProductMatch]:  # Return a list of matches
    """
    Search for products by name or description using fuzzy matching.
    Returns a list of products that meet the score threshold, sorted by score.
    The number of results can be limited by max_results.
    """
    # Use attributes from ProductData instances
    all_texts = [p.name + " " + p.description for p in products]
    # Get all potential matches
    raw_matches = process.extract(query, all_texts, limit=None) # Get all matches to filter and sort later

    valid_matches: list[ProductMatch] = []
    for match_item in raw_matches:
        text, score_float, *_ = match_item
        score = int(score_float)

        if score >= threshold:
            # Find the original product
            original_product: ProductData | None = None
            for p in products:
                if (p.name + " " + p.description) == text:
                    original_product = p
                    break

            if original_product:
                valid_matches.append(
                    ProductMatch(
                        id=original_product.id,
                        name=original_product.name,
                        description=original_product.description,
                        score=score,
                    )
                )

    # Sort by score in descending order
    valid_matches.sort(key=lambda x: x.score, reverse=True)

    if max_results is not None and max_results > 0:
        return valid_matches[:max_results]

    return valid_matches


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
