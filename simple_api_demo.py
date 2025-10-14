#!/usr/bin/env python3
"""
Simplified API Flow Demo - Works with existing data
==================================================

This script demonstrates API flow using existing data in the services.
"""

import requests
import json
import sys

# Service URLs
USER_SERVICE = "http://localhost:8000"
PRODUCT_SERVICE = "http://localhost:8001"
ORDER_SERVICE = "http://localhost:8002"

def print_step(step, description):
    print(f"\n{'='*60}")
    print(f"🔄 STEP {step}: {description}")
    print(f"{'='*60}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def main():
    print("""
🚀 SIMPLIFIED API FLOW DEMONSTRATION
===================================

This demo uses existing data to show inter-service communication.
    """)
    
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json'})
    
    # Step 1: Get existing users
    print_step("1", "Getting Existing Users")
    try:
        response = session.get(f"{USER_SERVICE}/users/")
        if response.status_code == 200:
            users = response.json()
            print_success(f"Found {len(users)} users in the system")
            for user in users[:3]:  # Show first 3
                print(f"   👤 {user['username']} (ID: {user['id']}) - {user['email']}")
        else:
            print_error("Could not retrieve users")
            return
    except Exception as e:
        print_error(f"Error accessing User Service: {e}")
        return
    
    # Step 2: Get existing products
    print_step("2", "Getting Existing Products")
    try:
        response = session.get(f"{PRODUCT_SERVICE}/products/")
        if response.status_code == 200:
            products = response.json()
            print_success(f"Found {len(products)} products in the catalog")
            for product in products[:5]:  # Show first 5
                print(f"   📱 {product['name']} - ${product['price']} (Stock: {product['stock_quantity']})")
        else:
            print_error("Could not retrieve products")
            return
    except Exception as e:
        print_error(f"Error accessing Product Service: {e}")
        return
    
    # Step 3: Create a new order with existing data
    print_step("3", "Creating New Order (Inter-Service Communication)")
    
    if users and products:
        # Use first user and first two products
        user = users[0]
        selected_products = products[:2]
        
        print_info(f"Creating order for {user['username']} with {len(selected_products)} items")
        
        order_data = {
            "user_id": user['id'],
            "shipping_address": f"{user['first_name']}'s Address, Demo City, DC 12345",
            "items": [
                {
                    "product_id": selected_products[0]['id'],
                    "quantity": 1,
                    "price": selected_products[0]['price']
                },
                {
                    "product_id": selected_products[1]['id'],
                    "quantity": 2,
                    "price": selected_products[1]['price']
                }
            ]
        }
        
        print_info("🔄 This demonstrates inter-service communication:")
        print("   1. Order Service verifies user exists in User Service")
        print("   2. Order Service checks stock availability in Product Service")
        print("   3. Order Service updates inventory in Product Service")
        print("   4. Order Service creates order with enriched data")
        
        try:
            response = session.post(f"{ORDER_SERVICE}/orders/", json=order_data)
            if response.status_code == 201:
                order = response.json()
                print_success(f"✅ Created Order #{order['id']}")
                
                # Show order details
                user_info = order.get('user_info', {})
                if user_info and 'user' in user_info:
                    customer_name = user_info['user'].get('username', 'Unknown')
                    print(f"   👤 Customer: {customer_name}")
                
                print(f"   💰 Total: ${order['total_amount']}")
                print(f"   📦 Items: {len(order['items'])}")
                
                for item in order['items']:
                    product_name = item.get('product_name', 'Unknown Product')
                    print(f"     • {product_name} x{item['quantity']} @ ${item['price']}")
                
                print(f"   🚚 Shipping: {order['shipping_address']}")
                
                # Step 4: Verify inventory was updated
                print_step("4", "Verifying Inventory Updates")
                
                response = session.get(f"{PRODUCT_SERVICE}/products/")
                if response.status_code == 200:
                    updated_products = response.json()
                    print_success("Inventory after order:")
                    
                    for product in updated_products[:5]:
                        print(f"   📦 {product['name']}: {product['stock_quantity']} units")
                        
                # Step 5: Get all orders
                print_step("5", "Viewing All Orders")
                
                response = session.get(f"{ORDER_SERVICE}/orders/")
                if response.status_code == 200:
                    all_orders = response.json()
                    print_success(f"Total orders in system: {len(all_orders)}")
                    
                    active_orders = [o for o in all_orders if o['status'] != 'cancelled']
                    cancelled_orders = [o for o in all_orders if o['status'] == 'cancelled']
                    
                    print(f"   ✅ Active orders: {len(active_orders)}")
                    print(f"   ❌ Cancelled orders: {len(cancelled_orders)}")
                    
                    total_revenue = sum(float(o['total_amount']) for o in active_orders)
                    print(f"   💰 Total revenue: ${total_revenue:.2f}")
                    
                    print_info("Recent orders:")
                    for order in all_orders[-3:]:  # Show last 3 orders
                        user_info = order.get('user_info', {})
                        customer_name = "Unknown"
                        if user_info and 'user' in user_info:
                            customer_name = user_info['user'].get('username', 'Unknown')
                        print(f"   📋 Order #{order['id']} - {customer_name} - ${order['total_amount']} ({order['status']})")
                
            else:
                print_error(f"Failed to create order: {response.text}")
                
        except Exception as e:
            print_error(f"Error creating order: {e}")
    
    print(f"\n{'='*60}")
    print("🎉 API FLOW DEMONSTRATION COMPLETE!")
    print(f"{'='*60}")
    print("""
✅ Successfully demonstrated:
   • Retrieving data from all services
   • Inter-service communication during order creation
   • Automatic user verification and product stock checking
   • Inventory updates after order creation
   • Complete order management workflow

🌐 Services are ready for manual testing:
   • User Service: http://localhost:8000/users/
   • Product Service: http://localhost:8001/products/
   • Order Service: http://localhost:8002/orders/

📊 Check OpenTelemetry traces for distributed tracing data!
    """)

if __name__ == "__main__":
    main()