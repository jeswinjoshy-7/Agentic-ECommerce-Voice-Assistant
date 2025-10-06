import random
from typing import Optional, Dict, Any, List

# --- Mock E-commerce Database ---
MOCK_PRODUCTS = [
  {
    "id": "p001", "name": "Men's Trail Runner XT Shoes", "category": "Footwear",
    "description": "Lightweight and durable trail running shoes with waterproof Gore-Tex lining. Perfect for tackling any terrain in any weather. Features enhanced grip and cushioning.",
    "price": 139.99, "stock": 45, "rating": 4.7, "tags": ["running", "waterproof", "men", "outdoor", "trail"],
    "related_product_ids": ["p002", "p005"]
  },
  {
    "id": "p002", "name": "Performance Athletic Socks (3-Pack)", "category": "Apparel",
    "description": "Breathable, moisture-wicking socks designed for high-intensity sports. Cushioned for comfort and support.",
    "price": 24.99, "stock": 150, "rating": 4.9, "tags": ["socks", "running", "unisex", "apparel", "breathable"],
    "related_product_ids": ["p001", "p003"]
  },
  {
    "id": "p003", "name": "Women's Yoga Flex Leggings", "category": "Apparel",
    "description": "High-waisted, flexible leggings made from recycled materials. Four-way stretch fabric provides comfort and freedom of movement for yoga or gym workouts.",
    "price": 79.50, "stock": 80, "rating": 4.6, "tags": ["leggings", "women", "yoga", "gym", "sustainable"],
    "related_product_ids": ["p002", "p004"]
  },
  {
    "id": "p004", "name": "Eco-Friendly Yoga Mat", "category": "Accessories",
    "description": "A non-slip yoga mat made from natural tree rubber and cork. Provides excellent grip and is 100% biodegradable.",
    "price": 65.00, "stock": 60, "rating": 4.8, "tags": ["yoga", "fitness", "eco-friendly", "accessory"],
    "related_product_ids": ["p003"]
  },
  {
    "id": "p005", "name": "Smart Fitness Tracker v5", "category": "Electronics",
    "description": "Track your steps, heart rate, sleep patterns, and workouts with this sleek fitness tracker. Features a 10-day battery life and a vibrant color display.",
    "price": 89.99, "stock": 110, "rating": 4.5, "tags": ["fitness", "tracker", "smartwatch", "health", "electronics"],
    "related_product_ids": ["p001", "p002", "p003"]
  },
  {
    "id": "p007", "name": "ProNoise Cancelling Headphones", "category": "Electronics",
    "description": "Immerse yourself in sound with these over-ear active noise-cancelling headphones. Delivers crisp audio and deep bass with 30 hours of playtime.",
    "price": 249.00, "stock": 30, "rating": 4.8, "tags": ["headphones", "audio", "electronics", "noise-cancelling"],
    "related_product_ids": ["p005"]
  },
  {
    "id": "p009", "name": "4K Action Camera Bundle", "category": "Electronics",
    "description": "Capture your adventures in stunning 4K. This bundle includes a waterproof case, various mounts, and a spare battery.",
    "price": 199.99, "stock": 40, "rating": 4.6, "tags": ["camera", "4k", "action", "electronics", "waterproof"],
    "related_product_ids": ["p010"]
  }
]

MOCK_ORDERS = {
    "ord_12345": {"status": "Shipped", "items": [{"product_id": "p001", "quantity": 1}], "total": 139.99},
    "ord_67890": {"status": "Processing", "items": [{"product_id": "p006", "quantity": 1}, {"product_id": "p008", "quantity": 2}], "total": 109.97},
}

# --- NEW DUMMY DATA ---
MOCK_SHOPPING_CART = {} # Simulates a user's shopping cart

MOCK_PRODUCT_REVIEWS = {
    "p001": [
        {"username": "TrailRunnerZoe", "rating": 5, "comment": "Absolutely fantastic grip on wet rocks. Kept my feet dry through a stream!"},
        {"username": "HikerMike", "rating": 4, "comment": "Very comfortable, but they run a little narrow. Consider sizing up."}
    ],
    "p007": [
        {"username": "AudioPhileAnna", "rating": 5, "comment": "The noise cancellation is top-tier. Perfect for flights and noisy offices."},
        {"username": "CommuterChris", "rating": 5, "comment": "Battery life is insane! I charge it maybe once a week. Sound quality is superb."}
    ],
    "p009": [
        {"username": "AdelineVlogs", "rating": 4, "comment": "Great value for the price. The 4K footage is crisp, but the low-light performance could be better."}
    ]
}


# --- Tool Functions ---

def search_products(query: str, category: Optional[str] = None, max_price: Optional[float] = None) -> List[Dict[str, Any]]:
    """Searches for products in the e-commerce catalog."""
    results = [
        p for p in MOCK_PRODUCTS 
        if query.lower() in p['name'].lower() or 
           query.lower() in p['description'].lower() or
           any(query.lower() in tag for tag in p['tags'])
    ]
    if category:
        results = [p for p in results if p['category'].lower() == category.lower()]
    if max_price:
        results = [p for p in results if p['price'] <= max_price]
    return results

def get_order_status(order_id: str) -> Dict[str, Any]:
    """Retrieves the status and details of a specific order using its ID."""
    order_id_lower = order_id.lower()
    if order_id_lower in MOCK_ORDERS:
        return MOCK_ORDERS[order_id_lower]
    return {"error": "Order not found."}

def initiate_payment(order_id: str, payment_method: str) -> Dict[str, Any]:
    """Initiates the payment process for a given order ID."""
    order_id_lower = order_id.lower()
    if order_id_lower not in MOCK_ORDERS:
        return {"error": "Cannot initiate payment. Order not found."}
    transaction_id = f"txn_{random.randint(1000000, 9999999)}"
    return {
        "status": "success",
        "message": f"Payment of ${MOCK_ORDERS[order_id_lower]['total']} for order {order_id} initiated via {payment_method}.",
        "transaction_id": transaction_id
    }

def get_general_help(topic: str) -> str:
    """Provides general help or information about common topics."""
    topic_lower = topic.lower()
    if 'hour' in topic_lower:
        return "Our store is open from 9 AM to 8 PM, Monday to Saturday. Online support is available 24/7."
    if 'return' in topic_lower or 'refund' in topic_lower:
        return "You can return any item within 30 days of purchase for a full refund."
    if 'contact' in topic_lower:
        return "You can contact our support team via email at support@example.com."
    return "I'm sorry, I can't find information on that topic. Could you please rephrase?"

def recommend_products(product_id: str, criteria: str = "related") -> List[Dict[str, Any]]:
    """Recommends products based on a given product ID and criteria."""
    product = next((p for p in MOCK_PRODUCTS if p["id"] == product_id), None)
    if not product:
        return [{"error": "Product not found."}]
    if criteria == "related":
        related_ids = product.get("related_product_ids", [])
        return [p for p in MOCK_PRODUCTS if p["id"] in related_ids]
    elif criteria == "top-rated":
        category = product["category"]
        category_products = [p for p in MOCK_PRODUCTS if p["category"] == category and p["id"] != product_id]
        top_rated = sorted(category_products, key=lambda p: p.get("rating", 0), reverse=True)
        return top_rated[:3]
    return []

# --- NEW TOOL FUNCTIONS ---

def add_to_cart(product_id: str, quantity: int) -> Dict[str, Any]:
    """
    Adds a specified quantity of a product to the shopping cart.
    
    :param product_id: The ID of the product to add.
    :param quantity: The number of units to add.
    :return: A confirmation message.
    """
    product = next((p for p in MOCK_PRODUCTS if p["id"] == product_id), None)
    if not product:
        return {"error": f"Product with ID '{product_id}' not found."}
    if product["stock"] < quantity:
        return {"error": f"Insufficient stock for {product['name']}. Only {product['stock']} available."}
    
    if product_id in MOCK_SHOPPING_CART:
        MOCK_SHOPPING_CART[product_id] += quantity
    else:
        MOCK_SHOPPING_CART[product_id] = quantity
        
    return {"status": "success", "message": f"Added {quantity} x {product['name']} to your cart."}

def view_cart() -> Dict[str, Any]:
    """
    Views the contents of the shopping cart, including items and total price.
    
    :return: A summary of the cart.
    """
    if not MOCK_SHOPPING_CART:
        return {"items": [], "total_price": 0, "message": "Your shopping cart is empty."}
    
    cart_items = []
    total_price = 0.0
    
    for product_id, quantity in MOCK_SHOPPING_CART.items():
        product = next((p for p in MOCK_PRODUCTS if p["id"] == product_id), None)
        if product:
            item_total = product["price"] * quantity
            total_price += item_total
            cart_items.append({
                "product_name": product["name"],
                "quantity": quantity,
                "item_total": round(item_total, 2)
            })
            
    return {"items": cart_items, "total_price": round(total_price, 2)}

def get_product_reviews(product_id: str) -> List[Dict[str, Any]]:
    """
    Retrieves customer reviews for a specific product.
    
    :param product_id: The ID of the product to get reviews for.
    :return: A list of reviews or an error message.
    """
    if product_id not in MOCK_PRODUCT_REVIEWS:
        return [{"message": "No reviews found for this product yet."}]
    
    return MOCK_PRODUCT_REVIEWS[product_id]
