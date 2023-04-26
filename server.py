from flask import Flask, render_template, redirect, flash, request, session
import jinja2
from melons import get_all, get_by_id
from forms import LoginForm, AddMelonForm
from customers import get_by_username

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = get_by_username(username)

        if not user or user["password"] != password:
            flash("Invalid username or password")
            return redirect("/login")

        session["username"] = user["username"]
        flash("You are logged in!")
        return redirect("/melons")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    del session["username"]
    flash("You are logged out successfully.")
    return redirect("/login")


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/melons")
def all_melons():
    melon_list = get_all()
    return render_template("all_melons.html", melon_list=melon_list)


@app.route("/melon/<melon_id>", methods=["GET", "POST"])
def melon_details(melon_id):
    form = AddMelonForm(request.form)
    melon = get_by_id(melon_id)
    if form.validate_on_submit():
        qty = form.quantity.data
        return redirect(f"/add_to_cart/{melon_id}/{qty}")
    return render_template("melon_details.html", melon=melon, form=form)


@app.route("/add_to_cart/<melon_id>/<qty>")
def add_to_cart(melon_id, qty):
    if 'username' not in session:
        return redirect("/login")
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    cart[melon_id] = cart.get(melon_id, 0) + int(qty)
    session.modified = True
    flash(f"Melon {melon_id} successfully added to cart.")
    print(cart)
    return redirect("/cart")


@app.route("/cart")
def show_shopping_cart():
    if 'username' not in session:
        return redirect("/login")
    order_total = 0
    cart_melons = []
    cart = session.get("cart", {})
    for melon_id, qty in cart.items():
        melon = get_by_id(melon_id)
        total_cost = qty * melon.price
        order_total += total_cost
        melon.quantity = qty
        melon.total_cost = total_cost
        cart_melons.append(melon)
    return render_template("cart.html", cart_melons=cart_melons, order_total=order_total)


@app.route("/empty-cart")
def empty_cart():
    session['cart'] = {}
    return redirect("/cart")


@app.errorhandler(404)
def error_404(err):
    return render_template("404.html")


if __name__ == "__main__":
    app.env = "development"
    app.run(debug=True, port=8000, host="localhost")
