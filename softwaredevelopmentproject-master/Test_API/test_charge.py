import stripe

stripe.api_key = 'sk_test_cn39HFPhtmki2m3JSnnM9AKH00kmPuoEBR'


# charge = stripe.Charge.create(
#     amount=350000,
#     currency='vnd',
#     customer= "cus_FnhbvCc17cHvRI",
#     receipt_email='baphucb1605354f@gmail.com',
# )
# print(charge.id)
#ch_1FNF1GHrvylkCYNZbLylSBEn

re = stripe.Refund.create(
  charge="ch_1FNFGKHrvylkCYNZitf96XX9",
  amount=80000
)
print(re)


# ch = stripe.Charge.create(
#   amount=50000,
#   currency="usd",
#   #source="tok_mastercard", # obtained with Stripe.js
#   description="Charge for jenny.rosen@example.com",
#   customer="cus_Fo3byKhcVH2aZO"
# )
# print(ch)

# payout = stripe.Payout.create(
#     amount=10000, # Amount in cents
#     currency="vnd",
#     destination="ba_1FIQh8HrvylkCYNZMHSCcI5O",
#     statement_descriptor="JUNE SALES"
# )
# print(payout)

# re = stripe.Refund.create(
#     amount=2,
#     currency='usd',
#     receipt_number="card_1FIQ6FHrvylkCYNZYyu7w41O"
# )

# tran = stripe.Customer.create_balance_transaction(
#     'cus_Fo2ARlz3rNCujf',
#     amount=20,
#     currency='usd',
# )
# print(tran)

# tf = stripe.Transfer.create(
#   amount=1000,
#   currency="usd",
#   destination="acct_1FIT3iDlmyrQRrWo",
#   #destination="card_1FIRXlHrvylkCYNZCbRY4Me9",
#   transfer_group="ORDER_95"
# )
# print(tf)

# payout = stripe.Payout.create(
#     amount=500,
#     currency='usd',
# )
# print(payout)

# print(stripe.Balance.retrieve())

# acc= stripe.Account.create(
#     type="custom",
#     country="US",
#     email="bob@example.com",
#     requested_capabilities=["card_payments", "transfers"],
#     business_type="individual",
#     payouts_enabled= "True"
# )
# print(acc)

# import time
# stripe.Account.modify(
#   "acct_1FISHkEgsB1bcri7",
#   tos_acceptance={
#     'date': int(time.time()),
#     'ip': '8.8.8.8', # Depends on what web framework you're using
#   }
# )
# print(acc.id)
#stripe.Account.delete('acct_1FISNsJUFtvpWRpw')