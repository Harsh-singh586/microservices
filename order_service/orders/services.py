import requests
from django.conf import settings


class ExternalServiceClient:
    """Client to communicate with other microservices"""
    
    @staticmethod
    def get_user_info(user_id):
        """Get user information from User Service"""
        try:
            response = requests.get(f"{settings.USER_SERVICE_URL}/api/user/{user_id}/")
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None
    
    @staticmethod
    def get_product_info(product_id):
        """Get product information from Product Service"""
        try:
            response = requests.get(f"{settings.PRODUCT_SERVICE_URL}/api/product/{product_id}/")
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None
    
    @staticmethod
    def check_product_stock(product_id, quantity):
        """Check if product has sufficient stock"""
        try:
            response = requests.post(
                f"{settings.PRODUCT_SERVICE_URL}/api/check-stock/",
                json={"product_id": product_id, "quantity": quantity}
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None
    
    @staticmethod
    def update_product_stock(product_id, quantity, operation='decrease'):
        """Update product stock in Product Service"""
        try:
            response = requests.post(
                f"{settings.PRODUCT_SERVICE_URL}/api/update-stock/",
                json={
                    "product_id": product_id, 
                    "quantity": quantity, 
                    "operation": operation
                }
            )
            return response.status_code == 200
        except requests.RequestException:
            return False
