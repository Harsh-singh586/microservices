#!/usr/bin/env python
"""
Sample data creation script for the microservices
Run this after all services are up and running
"""

import requests
import json
import time

# Service URLs
USER_SERVICE = "http://localhost:8000"
PRODUCT_SERVICE = "http://localhost:8001"
ORDER_SERVICE = "http://localhost:8002"

def wait_for_services():
    """Wait for all services to be available"""
    services = [
        ("User Service", USER_SERVICE),
        ("Product Service", PRODUCT_SERVICE),
        ("Order Service", ORDER_SERVICE)
    ]
    
    for name, url in services:
        while True:
            try:
                response = requests.get(f"{url}/admin/")
                if response.status_code in [200, 302]:
                    print(f"✓ {name} is running")
                    break
            except requests.ConnectionError:
                print(f"⏳ Waiting for {name}...")
                time.sleep(2)

def create_sample_data():
    """Create sample data for all services"""
    
    print("\n🚀 Creating sample data...")
    
    # 1. Create Users
    print("\n👤 Creating users...")
    users_data = [
        {
            "username": "john_doe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "password123",
            "phone": "1234567890",
            "address": "123 Main St, New York, NY"
        },
        {
            "username": "jane_smith",
            "email": "jane@example.com", 
            "first_name": "Jane",
            "last_name": "Smith",
            "password": "password123",
            "phone": "0987654321",
            "address": "456 Oak Ave, Los Angeles, CA"
        }
    ]
    
    created_users = []
    for user_data in users_data:
        try:
            response = requests.post(f"{USER_SERVICE}/users/", json=user_data)
            if response.status_code == 201:
                user = response.json()
                created_users.append(user)
                print(f"✓ Created user: {user['username']}")
            else:
                print(f"✗ Failed to create user {user_data['username']}: {response.text}")
        except Exception as e:
            print(f"✗ Error creating user: {e}")
    
    # 2. Create Categories
    print("\n📂 Creating categories...")
    categories_data = [
        {"name": "Electronics", "description": "Electronic gadgets and devices"},
        {"name": "Books", "description": "Books and literature"},
        {"name": "Clothing", "description": "Apparel and fashion items"}
    ]
    
    created_categories = []
    for category_data in categories_data:
        try:
            response = requests.post(f"{PRODUCT_SERVICE}/categories/", json=category_data)
            if response.status_code == 201:
                category = response.json()
                created_categories.append(category)
                print(f"✓ Created category: {category['name']}")
            else:
                print(f"✗ Failed to create category {category_data['name']}: {response.text}")
        except Exception as e:
            print(f"✗ Error creating category: {e}")
    
    # 3. Create Products
    print("\n📱 Creating products...")
    products_data = [
        {
            "name": "iPhone 15",
            "description": "Latest Apple iPhone with advanced features",
            "price": "999.99",
            "category_id": 1,
            "stock_quantity": 50
        },
        {
            "name": "Samsung Galaxy S23",
            "description": "Premium Android smartphone",
            "price": "899.99", 
            "category_id": 1,
            "stock_quantity": 30
        },
        {
            "name": "MacBook Pro",
            "description": "Professional laptop for developers",
            "price": "1999.99",
            "category_id": 1,
            "stock_quantity": 20
        },
        {
            "name": "Python Programming Book",
            "description": "Learn Python programming from scratch",
            "price": "29.99",
            "category_id": 2,
            "stock_quantity": 100
        },
        {
            "name": "T-Shirt",
            "description": "Comfortable cotton t-shirt",
            "price": "19.99",
            "category_id": 3,
            "stock_quantity": 200
        }
    ]
    
    created_products = []
    for product_data in products_data:
        try:
            response = requests.post(f"{PRODUCT_SERVICE}/products/", json=product_data)
            if response.status_code == 201:
                product = response.json()
                created_products.append(product)
                print(f"✓ Created product: {product['name']}")
            else:
                print(f"✗ Failed to create product {product_data['name']}: {response.text}")
        except Exception as e:
            print(f"✗ Error creating product: {e}")
    
    # 4. Create Sample Orders
    print("\n🛒 Creating sample orders...")
    orders_data = [
        {
            "user_id": 1,
            "shipping_address": "123 Main St, New York, NY",
            "items": [
                {"product_id": 1, "quantity": 1, "price": "999.99"},
                {"product_id": 4, "quantity": 2, "price": "29.99"}
            ]
        },
        {
            "user_id": 2,
            "shipping_address": "456 Oak Ave, Los Angeles, CA",
            "items": [
                {"product_id": 2, "quantity": 1, "price": "899.99"},
                {"product_id": 5, "quantity": 3, "price": "19.99"}
            ]
        }
    ]
    
    created_orders = []
    for order_data in orders_data:
        try:
            response = requests.post(f"{ORDER_SERVICE}/orders/", json=order_data)
            if response.status_code == 201:
                order = response.json()
                created_orders.append(order)
                user_name = order.get('user_info', {}).get('user', {}).get('username', 'Unknown')
                print(f"✓ Created order #{order['id']} for user: {user_name}")
            else:
                print(f"✗ Failed to create order: {response.text}")
        except Exception as e:
            print(f"✗ Error creating order: {e}")
    
    print("\n✅ Sample data creation complete!")
    print(f"Created {len(created_users)} users, {len(created_categories)} categories, {len(created_products)} products, {len(created_orders)} orders")
    
    print("\n🔗 You can now test the APIs:")
    print(f"- User Service: {USER_SERVICE}/users/")
    print(f"- Product Service: {PRODUCT_SERVICE}/products/")
    print(f"- Order Service: {ORDER_SERVICE}/orders/")

if __name__ == "__main__":
    print("🏗️  Sample Data Creator for Django Microservices")
    print("=" * 50)
    
    wait_for_services()
    create_sample_data()
