import stripe

stripe.api_key = 'sk_test_cn39HFPhtmki2m3JSnnM9AKH00kmPuoEBR'


tf = stripe.Transfer.create(
  amount=10000,
  currency="vnd",
  destination="acct_1FIVhjFWFkgsVFil",
  #destination="card_1FIRXlHrvylkCYNZCbRY4Me9",
  transfer_group="ORDER_95"
)
print(tf)