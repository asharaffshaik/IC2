Ice Cream Parlor Cafe Application
=================================

This is a simple Python application for a fictional ice cream parlor cafe that uses SQLite to manage seasonal flavor offerings, ingredient inventory, customer flavor suggestions, and allergy concerns. The application allows users to maintain a cart of their favorite products, search and filter the offerings, and add allergens if they don't already exist.

Features
--------

- Manage seasonal flavor offerings
- Track ingredient inventory
- Accept customer flavor suggestions
- Handle allergy concerns
- Maintain a cart of favorite products
- Search and filter flavor offerings
- Add new allergens

Technologies Used
-----------------

- Python
- SQLite (database)
- Streamlit (for user interface)

Getting Started
---------------

1. Clone the repository or download the source code.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Run the application by executing `streamlit run app.py`.
4. The application will open in your default web browser.

Usage
-----

1. Use the sidebar menu to navigate through different features of the application.
2. Add new flavors, ingredients, customer suggestions, and allergens using the corresponding menu options.
3. Search for flavors by name or description using the "Search Flavors" option.
4. Filter flavors based on seasonality and allergens using the "Filter Flavors" option.
5. View and manage your cart of favorite products using the "Cart" option.

Database Structure
------------------

The application uses an SQLite database named `icecream_cafe.db` to store the following data:

- `flavors` table: Stores information about available ice cream flavors.
- `ingredients` table: Stores information about ingredients used in the flavors.
- `customer_suggestions` table: Stores customer suggestions for new flavors.
- `allergens` table: Stores a list of known allergens.
- `flavor_ingredients` table: Maps flavors to their respective ingredients.
- `flavor_allergens` table: Maps flavors to their respective allergens.
- `cart` table: Stores the flavors added to the user's cart.

Contributing
------------

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

License
-------

This project is licensed under the [MIT License](LICENSE).