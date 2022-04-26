# Display a message asking the user to enter the name of the customer.

customer_name = input("Please enter your name:\n")
print("Name of the customer " + customer_name)

# Display a message asking the user to enter the name of the product the customer chooses. In
# this part, you can assume the product to be entered is always a valid product.

product_list = {"coffe": 10, "honey": 20, "tea": 15}
print("this are the available product " + str(product_list))
product_name = input("please enter the product name you want:\n")
if not product_name in product_list:
    print("product is not available")
else:
    print("the product is " + product_name)

# Display a message asking the quantity of the product ordered by the customer that was entered earlier.
# In this part, you can assume the quantity to be entered is always a positive integer, e.g., 1, 2, 3 ...

quantity_of_product = int(input("please enter the product quantity:\n"))
if quantity_of_product < 0:
    print("not a valid entry")
else:
    print("the quantity_of_product is " + str(quantity_of_product))
# Calculate the total cost for the customer including the discount
print(product_list[product_name]*quantity_of_product)
# For customers with membership, 5% discount will apply.
# TODO : We have to make a customer List
member_customer = []


