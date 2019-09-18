import stripe

stripe.api_key = 'sk_test_cn39HFPhtmki2m3JSnnM9AKH00kmPuoEBR'

cards = stripe.Customer.list_sources(
  'cus_FnhbvCc17cHvRI',
  limit=3,
  object='card'
)
print(cards)
print(len(cards['data']))
#print(cards['data'][0])