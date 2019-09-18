import stripe
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"
def charge():
    return stripe.Charge.create(
      amount=2000,
      currency="usd",
      #   token when create card
      source="tok_1FFHeG2eZvKYlo2CqQfO6Stx", # obtained with Stripe.js
      description="Charge for jenny.rosen@example.com"
    )

print(charge())