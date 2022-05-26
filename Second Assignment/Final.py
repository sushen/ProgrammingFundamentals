import sys
from abc import ABC, abstractmethod
import os
from datetime import datetime
sys.path.append("../../../Desktop/")

class RetailABC(ABC):
    @abstractmethod
    def get_discount(self, price):
        pass

    @abstractmethod
    def display_info(self):
        pass


class Customer(RetailABC):

    def __init__(self, id, name, discount_rate=0, value=0, membership="C") -> None:
        """_summary_

        Args:
            id (string): id of the customer
            name (string): name of the customer
            value (int, optional): total money the customer spent. Defaults to 0.
            membership (str, optional):which membership belong to customer. Defaults to "customer".
        """
        self.ID = id
        self.Name = name
        self.Value = value
        self.Membership = membership
        self.Discount_rate = discount_rate

    def get_id(self):
        return self.ID

    def get_name(self):
        return self.Name

    def get_value(self):
        return self.Value

    def set_id(self, _id):
        self.ID = _id

    def set_name(self, _name):
        self.Name = _name

    def set_value(self, _value):
        self.Value = _value

    def get_discount(self, price):
        """_summary_

        Args:
            price (float): This takes price of order 
        Returns: discount_rate(float),price(float) price after discount
        """
        return (self.Discount_rate, price)

    def display_info(self):
        """_summary_
        prints the values of customer attributes and the
        discount rate associate with the customer.
        """
        print(self.ID, self.Name, self.Value, self.Discount_rate)


class Member(Customer):
    def __init__(self, id, name, value, discount_rate=5, membership="M") -> None:
        super(Member, self).__init__(id, name, value)
        self.Membership = membership
        self.Discount_rate = discount_rate

    def get_discount(self, _price):
        """_summary_

        Args:
            _price (flaot): price of order


        Returns:
            discount_rate(float):discount rate
            price after discount: float
        """
        price_after_discount = _price - _price*self.Discount_rate

        return self.Discount_rate, price_after_discount

    def display_info(self):
        """display various member attributes
        """
        print(self.ID, self.Name, self.Membership,
              self.Value, self.Discount_rate)

    def set_rate(self, _rate):
        """This rate will effect all members

        Args:
            _rate (float): _description_
        """
        self.Discount_rate = _rate


class VIPMember(Customer):
    discount_rate: float
    threshold = 1000
    first_discount_rate = 10/100
    second_discount_rate = 15/100

    def __init__(self, id, name, value, discount_rate=10, membership="V") -> None:
        super(VIPMember, self).__init__(id, name, value)
        self.Membership = membership
        self.discount_rate = discount_rate

    def get_discount(self, _price):
        """_summary_

        Args:
            _price (flaot): price of order


        Returns:
            discount_rate(float):discount rate
            price after discount: float
        """
        if _price <= self.threshold:
            self.discount_rate = self.first_discount_rate
            price_after_discount = _price - _price*self.discount_rate
            return self.discount_rate, price_after_discount

        elif _price > self.threshold:
            self.discount_rate = self.second_discount_rate
            price_after_discount = _price - _price*self.discount_rate
            return self.discount_rate, price_after_discount

    def display_info(self):
        """display various member attributes
        """
        print(self.id, self.name, self.value,
              self.discount_rate, self.membership)

    def set_rate(self, _rate):
        """This rate will effect all members

        Args:
            _rate (float): _rate input as a dollar
        """
        self.discount_rate = _rate /100

    def set_threshold(self, _threshold_limit):
        self.threshold = _threshold_limit


class Product:
    def __init__(self, id, name, price, stock) -> None:
        self.ID = id
        self.Name = name
        self.Price = price
        self.Stock = stock

    def get_price(self):
        return self.Price

    def get_stock(self):
        return self.Stock

    def set_price(self, _price):
        self.Price = _price

    def set_stock(self, _quantity):
        self.Stock = self.Stock - _quantity


class Order:
    def __init__(self, customer, product, quantity) -> None:
        self.customer = customer
        self.product = product
        self.quantity = quantity
    


    
    # print order dummary of customer 
    def total_cost_order(self,customer_name,product_name,quantity,price,discount,total):
        print(f"""{customer_name}   purchase   {quantity} x {product_name}\n
                    Unit Price:                      {price}AUD\n
                    {customer_name}       get discount of <{discount}>%\n
                    Total price:                      {total}  AUD         
                """)
    
    # incrise the customer of value with every order in customer.txt file
    def incrise_value_of_customer(self, customer_name, value):
        with open("customers.txt","r") as file:
            data = file.readlines()
            line_num = None
            for i,line in enumerate(data):
                if customer_name in line:
                    line_num = i
                    break
            id,name,discount,val = data[line_num].split(",")
            new_value = float(val) + value
            data[line_num] = f"{id},{name},{discount},{new_value}\n"

            with open('customers.txt', 'w') as w_file:
                w_file.writelines( data )        

    # update stock in product.txt file
    def update_stock(self,product_name,quantity):
        with open("products.txt","r") as file:
            data = file.readlines()
            line_num = None
            for i,line in enumerate(data):
                if product_name in line:
                    line_num = i
                    break
            id,name,price,stock = data[line_num].split(",")
            stock = int(stock) - quantity
            data[line_num] = f"{id},{name},{price},{stock}\n"

            with open('products.txt', 'w') as w_file:
                w_file.writelines( data )
                   
                
                
class Bundle:
    def __init__(self, id, name,products,quantity) -> None:
        self.ID = id
        self.Name = name
        self.products = products
        self.quantity = quantity


                                            

    def stock_quantity(self):
        quantity = 0
        for product in self.products:
            quantity += product.Stock
        return quantity

    def adding_products(self, products):
        for product in products:
            self.products.append(product)
        return self.products


class Record:
    unique_id = []
    unique_name = []

    def __init__(self) -> None:
        self.customers = []
        self.products = []
        self.orders = []
        self.bunldes = []
        self.vip_customer = []

        
    # check order file exist in correct directory
    def check_order_file(self):
        if os.path.isfile("orders.txt") :
            return True
        else:
            print ("Cannot load the order file. Run as if there is no order previously.")

    # check customers file and products file exist in correct directory
    def check_both_files(self):
        """_summary_
        This function will check if the files are avaible"""
        if os.path.isfile("customers.txt") and os.path.isfile("products.txt"):
            return True

    # check customer exist in customer.txt file
    def check_customer_exist(self, id, name):
        """_summary_
        This function will check if the customer exist in the record"""

        if id in self.unique_id or name in self.unique_name:
            return False
        else:
            return True
        

    # read customers from txt file
    def read_customers(self):

        with open("customers.txt") as file:
            for string in file.readlines():
                id, name, discount_rate, value = string.split(",")
                # print(id,name,discount_rate,float(value[:-1]))
                if id.startswith("C"):
                    if not id[1:] in self.unique_id:
                        customer = Customer(
                            id=id.strip(), name=name.strip(), discount_rate=float(discount_rate), value=float(value[:-1].strip()))
                        self.customers.append(customer)
                        self.unique_id.append(id[1:])
                        self.unique_name.append(name)
                    else:
                        return("Id already registered")

                elif id.startswith("M"):
                    if not id[1:] in self.unique_id:
                        member = Member(
                            id=id.strip(), name=name.strip(), discount_rate=float(discount_rate), value=float(value[:-1].strip()))
                        self.customers.append(member)
                        self.unique_id.append(id[1:])
                        self.unique_name.append(name)
                    else:
                        return("Id already registered")

                elif id.startswith("V"):
                    if not id[1:] in self.unique_id:
                        vip = VIPMember(id=id.strip(), name=name.strip(), discount_rate=float(
                            discount_rate), value=float(value[:-1].strip()))
                        self.customers.append(vip)
                        self.vip_customer.append(vip)
                        self.unique_id.append(id[1:])
                        self.unique_name.append(name)
                    else:
                        return("Id already registered")


    # read products from products.txt file
    def read_products(self):
        with open("products.txt") as file:
            for string in file.readlines():
                id = string.split(",")
                if id[0].strip().startswith("P"):
                    id, name, price, stock = string.split(",")
                    product = Product(id=id.strip(), name=name.strip(),
                                      price=float(price), stock=int(stock))
                    self.products.append(product)
                  
                else:
                    arr = string.split(",")
                    bundle = Bundle(arr[0].strip(), arr[1].strip(),arr[2:-1],arr[-1].strip())
                    self.bunldes.append(bundle)

    # read orders from orders.txt file
    def read_orders(self):
        with open("orders.txt") as file:
            for string in file.readlines():
                id = string.split(",")
                self.orders.append(id)

    # print all the orders from orders.txt file
    def list_orders(self):
        with open("orders.txt") as file:
            for string in file.readlines():
                print(string)

    # print all orders  from single customer
    def get_all_order_by_one_customer(self,customer):
        all_orders =[]
        for i in range(0,len(self.orders)):
            if self.orders[i][0].strip() == customer.strip():
                all_orders.append(self.orders[i])
        if all_orders:
            for i in range(0,len(all_orders)):
                print(f"customer name: {all_orders[i][0]} , products : {all_orders[i][1]} , quantity :{all_orders[i][2]} , order time : {all_orders[i][3]}",end=" ")
        else:
            print("Invalid customer!") 
   

    def find_customer(self, _name):
        for customer in self.customers:
            if customer.Name == _name:
                return customer
        return None
        

    def find_product(self, _name):
        for product in self.products:
            if product.Name == _name:
                return product
        return None

    
    # check product by id in products.txt file
    def find_product_by_id(self, _id:str):
        for product in self.products:
            if product.ID == _id:
                return product
        return None


    # list all customers in the record from customers.txt file
    def list_customers(self):
        for customer in self.customers:
            print(f"ID: {customer.ID} Name: {customer.Name}, Discount: {customer.Discount_rate},Value: {customer.Value}, Membership: {customer.Membership}")

    # list all products in the record from products.txt file
    def list_products(self):
        for product in self.products:
            if product.ID.startswith('P'):
                print(
                f"Product ID: {product.ID}, Name: {product.Name}, Price: {product.Price},Stock: {product.Stock}")
        for bundle in self.bunldes:
                if bundle.ID.startswith('B'):
                    print(
                        f"Bundle ID: {bundle.ID}, Name: {bundle.Name}, Items: {','.join(bundle.products)},Stock: {bundle.quantity}")
                
   
    # calculate total bundle price
    def total_bundle_cost(self,products,quantity):
        cost = 0
        for i in products:
            for j in self.products:
                if j.ID.strip() == i.strip():
                    if j.Price == 0 or j.Price <0 or j.Price is None:   
                        return 'product price is not set'
                    else:
                        cost+=j.Price
                        break
                    
        return cost*0.80*int(quantity)
    
    # print bundle orders summary
    def bundle_order_format(self,customer_name,quantity,products,total):
        print(f"""{customer_name}   purchase   {quantity} x {products}\n
                    Total price:                      {total}  AUD         
                """)

    # set vip discount update to customers.txt file
    def set_vip_discount_rate(self,customer_name,discount_rate):
        for customer in self.customers:
            if customer.Name == customer_name and customer.ID.startswith('V'):
                with open("customers.txt","r") as file:
                    data = file.readlines()
                    line_num = None
                    for i,line in enumerate(data):
                        if customer_name in line:
                            line_num = i
                            break
                    id,name,discount,value = data[line_num].split(",")
                    current_discount = int(discount_rate) /100
                    data[line_num] = f"{id},{name},{current_discount},{value}\n"

                    with open('customers.txt', 'w') as w_file:
                        w_file.writelines( data )
                        print('Updated User Discount Rate')
        else:
            print("Customer not found")
        
    def append_customer(self, customer):
        self.customers.append(customer)

    def append_product(self, product):
        self.products.append(product)

    def append_order(self, order):
        self.orders.append(order)


def print_menu():
    print("""
 ##############################################################
 #                                                            #
 #   Welcome to the Retail Management System!                 #
 #                                                            #
 #   1. Place an order.                                       #
 #   2. Display existing customer.                            #
 #   3. Display existing product.                             #
 #   4. Adjust the discount rates of a VIP member.            #
 #   5. Adjust the threshold limit of all VIP members.        #
 #   6. Display all orders.                                   #
 #   7. Display all orders of a customer.                     #
 #   0. Exit the program.                                     #
 #                                                            #
 ##############################################################
    """)


if __name__ == "__main__":
    
    record = Record()
    if record.check_both_files():
        print_menu()
    else:
        raise Exception("Files not found")
    
    record.check_order_file()
    record.read_customers()
    record.read_products()
    record.read_orders()
    vip_membership_cost = 200

    while True:
        choice_option = input("Enter your choice: ")
        if choice_option == "1":
            print("1. Place an order: ")
            customer_name = input("\tEnter customer name: ")
            while True:
                is_bundle = input("\t Order bundle or not? y(Yes) or n(No) or b(back):")
                if is_bundle == "b":
                    break
                if is_bundle == "y":
                    user_bundle = input("\t Enter bundle id to order : " )
    
                    for i in range(0, len(record.bunldes)):
                        if record.bunldes[i].ID == user_bundle:
                            products = record.bunldes[i].products
                            quantity = record.bunldes[i].quantity
                            total_cost = record.total_bundle_cost(products,quantity)
                            order = Order(customer=customer_name, products=','.join(products), quantity=quantity)
                            record.bundle_order_format(customer_name,quantity,','.join(products),total_cost)
                    with open("orders.txt","a") as file:
                                            file.write(f"\n{customer_name},{','.join(products)},{quantity_product},{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                                            break
                            


                elif is_bundle == "n":
                    # Check customer exist
                    if record.find_customer(customer_name):
                        while True:
                            product_name = input("\t\tEnter product name:(e.g:shirt,towel,oven,kettle,microwave,candle or product id: ")
                            
                            if record.find_product(product_name) or record.find_product_by_id(product_name):
                                quantity_product = int(
                                    input("\t\t\tEnter quantity of product: "))
                                product = record.find_product(product_name)
                                customer = record.find_customer(customer_name)
                                
                                if quantity_product < 1 or not isinstance(quantity_product, int)\
                                        or quantity_product > product.Stock:
                                    print("\t\t\tProduct quantity can't be zero, float and less than stock of product")
                                                        
                                else:
                                    
                                    product.set_stock(quantity_product)
                                    customer.Value += customer.get_discount(product.Price)[1]
                                    total_price = customer.get_discount(product.Price*quantity_product)[1]
                                    order = Order(customer=customer, product=product, quantity=quantity_product)
                                    order.update_stock(product.Name,quantity_product)
                                    order.incrise_value_of_customer(customer.Name,total_price)
                                    if customer.Membership == "V":
                                        order.total_cost_order(customer.Name,product.Name,quantity_product,product.Price,'.10',total_price)

                                    else:
                                        order.total_cost_order(customer.Name,product.Name,quantity_product,product.Price,customer.Discount_rate,total_price)

                                    with open("orders.txt","a") as file:
                                            file.write(f"\n{customer_name},{product.Name},{quantity_product},{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                                            break
                            else:
                                print("\t\t\tProduct is not valid . enter a valid product ")    
                            
                    # If customer not exist.
                    else:
                        while True:
                            product_name = input("\t\tEnter product name:(e.g:shirt,towel,oven,kettle,microwave,candle or product id) ")
                            
                            if record.find_product(product_name) or record.find_product_by_id(product_name):
                                quantity_product = int(
                                    input("\t\t\tEnter quantity of product: "))
                                product = record.find_product(product_name)
                                
                                if quantity_product < 1 or not isinstance(quantity_product, int)\
                                        or quantity_product > product.Stock:
                                    print("\t\t\tProduct quantity can't be zero, float and less than stock of product")
                                                        
                                else:
                                    
                                    product.set_stock(quantity_product)
                                    order = Order(customer=customer_name, product=product, quantity=quantity_product)
                                    print("\t\t\t total product price: ",product.Price*quantity_product)
                                    print("\t\t\tOrder successfully placed")
                                    with open("orders.txt","a") as file:
                                            file.write(f"\n{customer_name},{product.Name},{quantity_product},{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                                    break
                            else:
                                print("\t\t\tProduct is not valid . enter a valid product ")
                            
                            
                        # Need membership or not
                        while True:
                            membership = input(
                                "\t\t\t\tDo you want to be a member? y(yes) or n(No) ")
                            if membership == "y":
                                choice_membership = input(
                                    "\t\t\t\t\tEnter your membership: V(VIP) or M(member) ")
                                if choice_membership == "V":
                                    id = input(
                                        "\t\t\t\tEnter CustomerID: ")
                                    int_id = id[1:]
                                    if record.check_customer_exist(int_id, customer_name):
                                        vip = VIPMember(id=id, name=customer_name,
                                                    value=vip_membership_cost)
                                        total_price = product.Price*quantity_product
                                        order.total_cost_order(customer_name,product.Name,quantity_product,product.Price,'.10',total_price+vip_membership_cost)
                                    
                                        with open("customers.txt","a") as file:
                                            file.write(f"\n{id},{customer_name},{vip.first_discount_rate},{vip_membership_cost}")
                                            break
                                    else:
                                        print("\t\t\t\tCustomer  already exist")
                                        break

                                elif choice_membership == "M":
                                    id = input(
                                        "\t\t\t\tEnter CustomerID: ")
                                    name = input(
                                        "\t\t\t\tEnter CustomerName: ")
                                    int_id = id[1:]
                                    if record.check_customer_exist(int_id, name):
                                        member = Member(id=id, name=name,value=product.Price*quantity_product)
                                    
                                        with open("customers.txt","a") as file:
                                            file.write(f"\n{id},{name},{member.Discount_rate},{product.Price*quantity_product}")
                                            break
                                    else:
                                        print("\t\t\t\tCustomer already exist")
                                        break
                                else:
                                    print("\t\t\t\tPlease enter a valid option")

                            elif membership == "n":
                                id = input("\t\t\t\tEnter CustomerID: ")
                                customer = Customer(id=id, name=customer_name,value=product.Price*quantity_product)
                                int_id = id[1:]
                                if record.check_customer_exist(int_id, customer_name):
                                    with open("customers.txt","a") as file:
                                            file.write(f"\n{id},{customer_name},{customer.Discount_rate},{product.Price*quantity_product}")
                                            break
                                
                                else:
                                    break
                            
                            else:
                                print("\t\t\t\tPlease enter a valid option ")
                                
                        

        elif choice_option == "2":
            record.list_customers()
            
        elif choice_option == "3":
            record.list_products()

        elif choice_option =="4":
            customer_name = input('Enter customer name :')
            discount_rate = input('Discount rate:')
            record.set_vip_discount_rate(customer_name,discount_rate)

        elif choice_option == "5":
            threshold = int(input('Enter trashhold:'))
            for i in range(len(record.vip_customer)):
                record.vip_customer[i].threshold = threshold
            print('Threshold updated')

        elif choice_option == "6":
            record.list_orders()

        elif choice_option == "7" :
            customer_name = input('Enter customer name :')
            record.get_all_order_by_one_customer(customer_name)
        

        elif choice_option == "0":
            sys.exit()
        else:
            print("please enter a valid option.")
