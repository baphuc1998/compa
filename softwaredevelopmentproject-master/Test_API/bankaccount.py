
import stripe

stripe.api_key = 'sk_test_cn39HFPhtmki2m3JSnnM9AKH00kmPuoEBR'


cards = stripe.Customer.list_sources(
    "cus_FsdytnM2JvsqJg",
    limit=2,
    object='card'
)
print(len(cards['data']) )
# mycard = cards['data'][0]
# acc = stripe.Account.create(
# type="custom",
# country="US",
# email="test@gmail.com",
# requested_capabilities=["card_payments", "transfers"],
# business_type="individual",
# )
# print(acc)
# # bank = stripe.Token.create(
# #   bank_account={
# #     'country': 'US',
# #     'currency': 'usd',
# #     'account_holder_name': 'Jenny Rosen',
# #     'account_holder_type': 'individual',
# #     'routing_number': '110000000',
# #     'account_number': '000123456789',
# #   },
# # )

# # print(bank)


# ba = stripe.Customer.create_source(
#     "acct_1FIQlQFRtuWcpUKH",
#     source="btok_1FIS0OHrvylkCYNZuKhFnLSF"
# )

# print(ba)