# shopping_cart.py

import os
from dotenv import load_dotenv
from datetime import datetime
from datetime import date
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

products = [
    {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50},
    {"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99},
    {"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49},
    {"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99},
    {"id":5, "name": "Green Chile Anytime Sauce", "department": "pantry", "aisle": "marinades meat preparation", "price": 7.99},
    {"id":6, "name": "Dry Nose Oil", "department": "personal care", "aisle": "cold flu allergy", "price": 21.99},
    {"id":7, "name": "Pure Coconut Water With Orange", "department": "beverages", "aisle": "juice nectars", "price": 3.50},
    {"id":8, "name": "Cut Russet Potatoes Steam N' Mash", "department": "frozen", "aisle": "frozen produce", "price": 4.25},
    {"id":9, "name": "Light Strawberry Blueberry Yogurt", "department": "dairy eggs", "aisle": "yogurt", "price": 6.50},
    {"id":10, "name": "Sparkling Orange Juice & Prickly Pear Beverage", "department": "beverages", "aisle": "water seltzer sparkling water", "price": 2.99},
    {"id":11, "name": "Peach Mango Juice", "department": "beverages", "aisle": "refrigerated", "price": 1.99},
    {"id":12, "name": "Chocolate Fudge Layer Cake", "department": "frozen", "aisle": "frozen dessert", "price": 18.50},
    {"id":13, "name": "Saline Nasal Mist", "department": "personal care", "aisle": "cold flu allergy", "price": 16.00},
    {"id":14, "name": "Fresh Scent Dishwasher Cleaner", "department": "household", "aisle": "dish detergents", "price": 4.99},
    {"id":15, "name": "Overnight Diapers Size 6", "department": "babies", "aisle": "diapers wipes", "price": 25.50},
    {"id":16, "name": "Mint Chocolate Flavored Syrup", "department": "snacks", "aisle": "ice cream toppings", "price": 4.50},
    {"id":17, "name": "Rendered Duck Fat", "department": "meat seafood", "aisle": "poultry counter", "price": 9.99},
    {"id":18, "name": "Pizza for One Suprema Frozen Pizza", "department": "frozen", "aisle": "frozen pizza", "price": 12.50},
    {"id":19, "name": "Gluten Free Quinoa Three Cheese & Mushroom Blend", "department": "dry goods pasta", "aisle": "grains rice dried goods", "price": 3.99},
    {"id":20, "name": "Pomegranate Cranberry & Aloe Vera Enrich Drink", "department": "beverages", "aisle": "juice nectars", "price": 4.25}
] # based on data from Instacart: https://www.instacart.com/datasets/grocery-shopping-2017


def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.

    Param: my_price (int or float) like 4000.444444

    Example: to_usd(4000.444444)

    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71


#Python code to produce the desired output

identifiers = []
selected_id = 0

valid_options = [item["id"] for item in products]
valid_options.append("DONE")

while selected_id != "DONE":
    selected_id = input("Please input a product identifier (1-20 are valid), or 'DONE' if there are no more items:")
    if str(selected_id) not in str(valid_options):
        print("Hey, are you sure that product identifier is correct? Please try again!")
    elif selected_id != "DONE":
        identifiers.append(selected_id)

#print("Shopping Cart Item Identifiers Include:", identifiers)

matching_products = []
total_price = 0.0

for count in identifiers:
    for product in products:
        if int(product["id"]) == int(count):
            matching_products.append(product) 

print("---------------------------------")
print("GREEN FOODS GROCERY")
print("WWW.GREEN-FOODS-GROCERY.COM")
print("---------------------------------")
print("CHECKOUT AT:", datetime.now().strftime("%Y-%m-%d %I:%M %p"))
print("---------------------------------")
print("SELECTED PRODUCTS:")

for item in matching_products:
    print("+", item["name"], "(" + to_usd(item["price"]) + ")")
    total_price = total_price + item["price"]

load_dotenv()
tax_rate = os.getenv("tax_rate", default = 0.0875)

tax = total_price*float(tax_rate)
total_with_tax = total_price + tax

print("---------------------------------")
print("SUBTOTAL:", to_usd(total_price))
print("TAX:", to_usd(tax))
print("Total:", to_usd(total_with_tax))
print("---------------------------------")
print("THANKS, SEE YOU AGAIN SOON!")
print("---------------------------------")

#Code to send receipt through email

email_option = input("Would you like to receive your receipt by email (Yes or No)?")

if email_option.lower() == "yes":
    email_address = input("Please enter your email address:")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", default="OOPS, please set env var called 'SENDGRID_API_KEY'")
    SENDER_ADDRESS = os.getenv("SENDER_ADDRESS", default="OOPS, please set env var called 'SENDER_ADDRESS'")
    SENDGRID_TEMPLATE_ID = os.getenv("SENDGRID_TEMPLATE_ID", default="OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'")
    template_data = {
    "total_price_usd": to_usd(total_with_tax),
    "human_friendly_timestamp": date.today().strftime("%B %d, %Y %I:%M %p"),
    "products": matching_products
    }
    client = SendGridAPIClient(SENDGRID_API_KEY)
    print("CLIENT:", type(client))
    message = Mail(from_email=SENDER_ADDRESS, to_emails=email_address)
    message.template_id = SENDGRID_TEMPLATE_ID
    message.dynamic_template_data = template_data
    print("MESSAGE:", type(message))
    try:
        response = client.send(message)
        print("RESPONSE:", type(response))
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as err:
        print(type(err))
        print(err)
