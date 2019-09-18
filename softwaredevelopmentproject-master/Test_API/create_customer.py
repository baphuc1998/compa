import stripe

stripe.api_key = 'sk_test_cn39HFPhtmki2m3JSnnM9AKH00kmPuoEBR'
cus = stripe.Customer.create(
  description="Customer for jenny.rosen@example.com",
  #source="tok_mastercard" # obtained with Stripe.js
)

print(cus)