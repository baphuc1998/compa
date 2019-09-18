import stripe
from GladFood.StripePayment.API import api_key
stripe.api_key = api_key

def createCustomer():
    return stripe.Customer.create(
      description="Customer for jenny.rosen@example.com",
      source="tok_mastercard" # obtained with Stripe.js
    )
def delCustomer(customer_id):
    return stripe.Customer.delete(customer_id)


cus = createCustomer()

print(cus.id)

print(delCustomer(cus.id))