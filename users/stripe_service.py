import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(name, description):
    product = stripe.Product.create(
        name=name,
        description=description or "Описание курса",
    )
    return product


def create_stripe_price(product_id, unit_amount):
    price = stripe.Price.create(
        unit_amount=unit_amount,
        currency="rub",
        product=product_id,
    )
    return price


def create_stripe_checkout_session(price_id, success_url, cancel_url):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session
