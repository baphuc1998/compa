import stripe
# stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"
from GladFood.StripePayment.API import api_key

def createToken():
    stripe.api_key = api_key;

    return stripe.Token.create(
        card={
            'number': '4242424242424242',
            'exp_month': 12,
            'exp_year': 2020,
            'cvc': '123',
        },
    )

print(createToken())