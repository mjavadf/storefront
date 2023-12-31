from os import name
from locust import HttpUser, between, task
from random import randint


class WebsiteUser(HttpUser):
    # Wait 1 to 5 seconds before executing next task
    wait_time = between(1, 5)
    
    @task(2)
    def view_products(self):
        collection_id = randint(2, 10)
        self.client.get(f"/products/?collection_id={collection_id}", name="/products/")

    # weight:4 that means it has most important priority
    @task(4)
    def view_product(self):
        product_id = randint(1, 1000)
        self.client.get(f"/products/{product_id}", name="/products/:id/")

    @task(1)
    def add_to_cart(self):
        product_id = randint(1, 10)
        self.client.post(
            f"/carts/{self.cart_id}/items/",
            name="/carts/:id/items/",
            json={"product_id": product_id, "quantity": 1},
        )
        
    @task
    def say_hello(self):
        self.client.get('/playground/hello/')

    # this method runs every time a user start browsing website
    def on_start(self):
        response = self.client.post("/carts/")
        result = response.json()
        self.cart_id = result["id"]
