## Description in a few words
This is a shop of shops.

Each shop has products. A product has details and images.

## User's perspective
Creates an account and logs in.

The user sees a list of shops. Can access a shop and view it's products.

The user can select a product and add it to the cart.

In the cart, user will see all the products added, each quantity per product, total for each product, and a total calculated on cart level.

The user can place the order. The cart will be emptied.
The user can see the list of placed orders.

#### The cart
The cart will be created automatically when the user adds a product. The cart is now assigned to the shop.

If the user decides to change the shop and add a product, the cart will be emptied of the current products because it only accepts products from the same shop.

#### The order
The order is snapshot of the cart. That means it takes the cart total and products total based on quantity.

This way, if the product changes or is removed, details of it will be maintained on order history.

The order will also be assigned to the shop, as the cart. 

Can watch an order for status change.


## Shop's perspective
Creates an account and logs in.

Can create and manage shops. For each shop, it can create and manage products.

Can view orders received by the shop. 

Can update order's status.

---

### Implementation ideas

Something for backend:
* Payment process before an order is created and a cart is emptied
* Order notification update (for user and shop)
* Filtering, sorting in general
* Product extra options. When a product is added to cart, it can be added with extra options that alter the price
* Taxes layer on the cart, for example VAT
* Invoices for created orders

Something for the frontend:
* Authentication flow
* Shops view (This would be cool on a map, to see what shops are in your area)
* Shop view / Product listing
* Cart Listing and management
* Payment integration
* Order listing
* Active order view


### Development process
This is a flask app with flask-restful.

```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python app/main.py
```

There is a Sendgrid email integration for password reset, that requires an api key variable. Add `MAIL=api_key` to your local env. See [app/services/mail.py](app/services/mail.py)

