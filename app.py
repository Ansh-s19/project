from flask import Flask, render_template, redirect, request,session, url_for, jsonify, flash
import mysql.connector as db

app = Flask(__name__)
app.secret_key = "gymsupps_secret_key"

# Dummy data for products
products = [
    {"id": 1, "name": "Whey-Protein", "price": 2200, "image": "th.jpg"},
    {"id": 2, "name": "Creatine", "price": 639, "image": "th (1).jpg"},
    {"id": 3, "name": "Multivitamin", "price": 550, "image": "OIP (3).jpg"},
    {"id": 4, "name": "Fish Oil", "price": 499, "image": "OIP (5).jpg"},
    {"id": 5, "name": "Mass Gainer", "price": 1800, "image": "OIP (4).jpg"},
    {"id": 6, "name": "Shaker", "price": 399, "image": "th (2).jpg"},
    {"id": 7, "name": "Isolate protein", "price": 3399, "image": "OIP (6).jpg"},
    {"id": 8, "name": "L-carnitine", "price": 599, "image": "OIP (7).jpg"},
   
]

# Cart
cart = {}
connection = db.connect(user="root", 
                        password="anshit9850", 
                        host="127.0.0.1", 
                        database="gymsupps",
                        )

print("Connection Created.")
print(connection)
@app.route("/")
def landing_page():
    return render_template("home1.html")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/products")
def product_page():
    return render_template("products.html", products=products)


@app.route("/cart", methods=["GET", "POST"])
def cart_page():
    global cart
    if request.method == "POST":
        product_id = int(request.form.get("product_id"))
        action = request.form.get("action")
        
        # Add product to cart or update quantity
        if action == "add":
            if product_id in cart:
                cart[product_id]["quantity"] += 1
            else:
                product = next((p for p in products if p["id"] == product_id), None)
                if product:
                    cart[product_id] = {"name": product["name"], "price": product["price"], "quantity": 1}

        # Decrease quantity or remove product from cart
        elif action == "remove":
            if product_id in cart:
                if cart[product_id]["quantity"] > 1:
                    cart[product_id]["quantity"] -= 1
                else:
                    del cart[product_id]

    # Calculate total cost
    total = sum(item["price"] * item["quantity"] for item in cart.values())
    return render_template("cart.html", cart=cart, total=total)




@app.route("/payment")
def payment():
    global cart
    total = sum(item["price"] * item["quantity"] for item in cart.values())
    return render_template("payment.html", total=total)


@app.route('/buy', methods=['POST'])
def buy():
    card_number = request.form['card_number']
    expiry_date = request.form['expiry_date']
    cvv = request.form['cvv']

    # Simulate payment processing
    if card_number and expiry_date and cvv:
        # Clear the cart from the session
        session.pop('cart', None)  # Remove the cart
        flash("Order placed successfully!")
        return redirect(url_for('success'))
    else:
        flash("Payment failed! Please try again.")
        return redirect(url_for('home'))
    
@app.route("/clear_cart")
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('home'))

    
@app.route('/success')
def success():
    return render_template('success.html')    

@app.route("/customer_support")
def customer_support():
    return render_template("customer_support.html")

if __name__ == "__main__":
    app.run(debug=True)
