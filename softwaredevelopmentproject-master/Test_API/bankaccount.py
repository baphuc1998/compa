
import stripe

stripe.api_key = 'sk_test_cn39HFPhtmki2m3JSnnM9AKH00kmPuoEBR'

# bank = stripe.Token.create(
#   bank_account={
#     'country': 'US',
#     'currency': 'usd',
#     'account_holder_name': 'Jenny Rosen',
#     'account_holder_type': 'individual',
#     'routing_number': '110000000',
#     'account_number': '000123456789',
#   },
# )

# print(bank)


ba = stripe.Customer.create_source(
    "acct_1FIQlQFRtuWcpUKH",
    source="btok_1FIS0OHrvylkCYNZuKhFnLSF"
)

print(ba)