import sqlite3
import streamlit as st
# Connect to the SQLite database
conn = sqlite3.connect('icecream_cafe.db')
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS flavors
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, seasonal BOOLEAN)''')

c.execute('''CREATE TABLE IF NOT EXISTS ingredients
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, quantity INTEGER)''')

c.execute('''CREATE TABLE IF NOT EXISTS customer_suggestions
             (id INTEGER PRIMARY KEY AUTOINCREMENT, flavor TEXT, description TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS allergens
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS flavor_ingredients
             (flavor_id INTEGER, ingredient_id INTEGER, FOREIGN KEY(flavor_id) REFERENCES flavors(id), FOREIGN KEY(ingredient_id) REFERENCES ingredients(id))''')

c.execute('''CREATE TABLE IF NOT EXISTS flavor_allergens
             (flavor_id INTEGER, allergen_id INTEGER, FOREIGN KEY(flavor_id) REFERENCES flavors(id), FOREIGN KEY(allergen_id) REFERENCES allergens(id))''')

c.execute('''CREATE TABLE IF NOT EXISTS cart
             (id INTEGER PRIMARY KEY AUTOINCREMENT, flavor_id INTEGER, FOREIGN KEY(flavor_id) REFERENCES flavors(id))''')

# Functions

def add_flavor(name, description, seasonal):
    c.execute("INSERT INTO flavors (name, description, seasonal) VALUES (?, ?, ?)", (name, description, seasonal))
    conn.commit()

def add_ingredient(name, quantity):
    c.execute("INSERT INTO ingredients (name, quantity) VALUES (?, ?)", (name, quantity))
    conn.commit()

def add_customer_suggestion(flavor, description):
    c.execute("INSERT INTO customer_suggestions (flavor, description) VALUES (?, ?)", (flavor, description))
    conn.commit()

def add_allergen(name):
    c.execute("INSERT INTO allergens (name) VALUES (?)", (name,))
    conn.commit()

def add_flavor_ingredient(flavor_id, ingredient_id):
    c.execute("INSERT INTO flavor_ingredients (flavor_id, ingredient_id) VALUES (?, ?)", (flavor_id, ingredient_id))
    conn.commit()

def add_flavor_allergen(flavor_id, allergen_id):
    c.execute("INSERT INTO flavor_allergens (flavor_id, allergen_id) VALUES (?, ?)", (flavor_id, allergen_id))
    conn.commit()

def add_to_cart(flavor_id):
    c.execute("INSERT INTO cart (flavor_id) VALUES (?)", (flavor_id,))
    conn.commit()

def search_flavors(query):
    c.execute("SELECT * FROM flavors WHERE name LIKE ? OR description LIKE ?", ('%' + query + '%', '%' + query + '%'))
    return c.fetchall()

def filter_flavors(seasonal=None, allergens=None):
    query = "SELECT f.* FROM flavors f"
    conditions = []

    if seasonal is not None:
        conditions.append("f.seasonal = ?")

    if allergens:
        allergen_condition = " AND ".join(["f.id NOT IN (SELECT flavor_id FROM flavor_allergens WHERE allergen_id = (SELECT id FROM allergens WHERE name = ?))" for _ in allergens])
        conditions.append(allergen_condition)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        params = [seasonal] + allergens if allergens else [seasonal]
        c.execute(query, params)
    else:
        c.execute(query)

    return c.fetchall()

def view_cart():
    c.execute("SELECT f.name, f.description FROM cart c JOIN flavors f ON c.flavor_id = f.id")
    return c.fetchall()

# Example usage
add_flavor("Vanilla", "Classic vanilla flavor", False)
add_flavor("Strawberry", "Sweet strawberry flavor", True)
add_ingredient("Milk", 100)
add_ingredient("Sugar", 50)
add_flavor_ingredient(1, 1)
add_flavor_ingredient(1, 2)
add_customer_suggestion("Chocolate Hazelnut", "Rich chocolate with hazelnut chunks")
add_allergen("Nuts")
add_allergen("Dairy")
add_flavor_allergen(1, 2)

print("Flavors containing 'berry':")
for flavor in search_flavors("berry"):
    print(flavor)

print("\nSeasonal flavors without dairy allergen:")
for flavor in filter_flavors(seasonal=True, allergens=["Dairy"]):
    print(flavor)

add_to_cart(1)
print("\nCart contents:")
for flavor in view_cart():
    print(flavor)

def main():

    st.title("Ice Cream Parlor Cafe")

    # Sidebar navigation
    menu = ["Add Flavor", "Add Ingredient", "Add Suggestion", "Add Allergen", "Search Flavors", "Filter Flavors", "Cart"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Flavor":
        st.subheader("Add Flavor")
        name = st.text_input("Flavor Name")
        description = st.text_area("Description")
        seasonal = st.checkbox("Seasonal")
        if st.button("Add Flavor"):
            add_flavor(name, description, seasonal)
            st.success("Flavor added successfully!")

    elif choice == "Add Ingredient":
        st.subheader("Add Ingredient")
        name = st.text_input("Ingredient Name")
        quantity = st.number_input("Quantity", min_value=0, step=1)
        if st.button("Add Ingredient"):
            add_ingredient(name, quantity)
            st.success("Ingredient added successfully!")

    elif choice == "Add Suggestion":
        st.subheader("Add Customer Suggestion")
        flavor = st.text_input("Flavor Suggestion")
        description = st.text_area("Description")
        if st.button("Add Suggestion"):
            add_customer_suggestion(flavor, description)
            st.success("Suggestion added successfully!")

    elif choice == "Add Allergen":
        st.subheader("Add Allergen")
        name = st.text_input("Allergen Name")
        if st.button("Add Allergen"):
            add_allergen(name)
            st.success("Allergen added successfully!")

    elif choice == "Search Flavors":
        st.subheader("Search Flavors")
        query = st.text_input("Search Query")
        if st.button("Search"):
            results = search_flavors(query)
            for flavor in results:
                st.write(f"{flavor[1]} - {flavor[2]}")

    elif choice == "Filter Flavors":
        st.subheader("Filter Flavors")
        seasonal = st.checkbox("Seasonal")
        allergens = st.multiselect("Allergens", [allergen[0] for allergen in c.execute("SELECT name FROM allergens")])
        if st.button("Filter"):
            results = filter_flavors(seasonal, allergens)
            for flavor in results:
                st.write(f"{flavor[1]} - {flavor[2]}")

    elif choice == "Cart":
        st.subheader("Cart")
        cart_items = view_cart()
        for item in cart_items:
            st.write(f"{item[0]} - {item[1]}")
        flavor_id = st.number_input("Flavor ID to add to cart", min_value=1, step=1)
        if st.button("Add to Cart"):
            add_to_cart(flavor_id)
            st.success("Flavor added to cart!")

if __name__ == "__main__":
    main()

# Close the database connection
conn.close()