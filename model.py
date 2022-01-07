import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as mysql


try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

def close():
    root.destroy()

import numpy as np
import pandas as pd

data = pd.read_csv("car.csv")
data.head()

data.drop(['Car_Name'],axis=1,inplace=True)

FuelType = ['Fuel_Type']
data = pd.get_dummies(data,columns=FuelType)

Transmission = ['Transmission']
data = pd.get_dummies(data,columns=Transmission)

SellerType = ['Seller_Type']
data = pd.get_dummies(data,columns=SellerType)


data.drop(['Year'],axis=1,inplace=True)
data.head()


from sklearn.model_selection import train_test_split

X = data.drop(['Selling_Price'],axis=1).values
y = data['Selling_Price'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=101)

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential()

model.add(Dense(10,activation='relu'))
model.add(Dense(10,activation='relu'))
model.add(Dense(10,activation='relu'))
model.add(Dense(10,activation='relu'))
model.add(Dense(10,activation='relu'))

model.add(Dense(1))
model.compile(optimizer='adam',loss='mse')

model.fit(x=X_train,y=y_train,validation_data=(X_test,y_test),batch_size=128,epochs=400)


def success():
    w = ttk.Label(root, text='Signup Successful', font="50")
    w.grid()
    messagebox.showinfo("Signup", "Successful")
    w.mainloop()


class CarPricePrediction(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Car price prediction")
        self.frames = dict()

        container = ttk.Frame(self)
        container.grid(padx=10, pady=10, sticky="EW")

        Registrationframe = Form(container, self)
        Registrationframe.grid(row=0, column=0, sticky="NSEW")

        Loginframe = login(container, self)
        Loginframe.grid(row=0, column=0, sticky="NSEW")

        frame = car(container, self)
        frame.grid(row=0, column=0, sticky="NSEW")

        self.frames[login] = Loginframe
        self.frames[Form] = Registrationframe
        self.frames[car] = frame

        self.show_frame(login)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


class Form(ttk.Frame):

    def __init__(self, container, controller):
        super().__init__(container)

        global name_value , Email_value , city_value , address_value , username_value , password_value
        name_value = tk.StringVar()
        Email_value = tk.StringVar()
        city_value = tk.StringVar()
        address_value = tk.StringVar()
        username_value = tk.StringVar()
        password_value = tk.StringVar()

        name_label = ttk.Label(self, text="Name: ")
        global name_input
        name_input= ttk.Entry(self, width=15, textvariable=name_value)
        name_label.grid(column=0, row=1, sticky="EW", padx=5, pady=5)
        name_input.grid(column=1, row=1, sticky="EW", padx=5, pady=5)
        name_input.focus()

        Email_label = ttk.Label(self, text="Email: ")
        global Email_input
        Email_input= ttk.Entry(self, width=15, textvariable=Email_value)
        Email_label.grid(column=0, row=2, sticky="EW", padx=5, pady=5)
        Email_input.grid(column=1, row=2, sticky="EW", padx=5, pady=5)

        city_label = ttk.Label(self, text="City: ")
        global city_input
        city_input= ttk.Entry(self, width=15, textvariable=city_value)
        city_label.grid(column=0, row=3, sticky="EW", padx=5, pady=5)
        city_input.grid(column=1, row=3, sticky="EW", padx=5, pady=5)

        address_label = ttk.Label(self, text="Address: ")
        global address_input
        address_input= ttk.Entry(self, width=15, textvariable=address_value)
        address_label.grid(column=0, row=4, sticky="EW", padx=5, pady=5)
        address_input.grid(column=1, row=4, sticky="EW", padx=5, pady=5)

        username_label = ttk.Label(self, text="Username: ")
        global username_input
        username_input = ttk.Entry(self, width=15, textvariable=username_value)
        username_label.grid(column=0, row=5, sticky="EW", padx=5, pady=5)
        username_input.grid(column=1, row=5, sticky="EW", padx=5, pady=5)
        username_input.focus()

        password_label = ttk.Label(self, text="Password: ")
        global password_input
        password_input= ttk.Entry(self, width=15, textvariable=password_value)
        password_label.grid(column=0, row=6, sticky="EW", padx=5, pady=5)
        password_input.grid(column=1, row=6, sticky="EW", padx=5, pady=5)

        sign_button = tk.Button(self, text="Sign Up", width=7, bg="#FCDEC0", command=self.insert)
        sign_button.grid(column=0, row=7, sticky="EW", padx=7, pady=7)

        login_button = tk.Button(self, text="Login", width=3, bg="#FCDEC0",
                                 command=lambda: [controller.show_frame(car)])
        login_button.grid(column=1, row=7, sticky="EW", padx=7, pady=7)

        cancel_button = tk.Button(self, text="❌ Cancel", width=10, bg="#FCDEC0",
                                  command=lambda: [controller.show_frame(login)])
        cancel_button.grid(column=2, row=7, sticky="EW", padx=7, pady=7)

    def insert(self):
        name=name_value.get()
        email=Email_value.get()
        city=city_value.get()
        address=address_value.get()
        username=username_value.get()
        password=password_value.get()

        mydb = mysql.connect(host='localhost', user='root', password='', database='signup')
        mycursor = mydb.cursor()
        mycursor.execute("INSERT INTO information values('"+name+"','"+email+"','"+city+"','"+address+"','"+username+"','"+password+"')")
        mycursor.execute("commit");

        name_input.delete(0,'end')
        Email_input.delete(0, 'end')
        city_input.delete(0, 'end')
        address_input.delete(0, 'end')
        username_input.delete(0, 'end')
        password_input.delete(0, 'end')
        messagebox.showinfo("successful", "User registered successfully . Click ok and then login to go further ");
        mydb.close();


class login(ttk.Frame):

    def __init__(self, container, controller):
        super().__init__(container)

        self.userName = tk.StringVar()
        self.password = tk.StringVar()

        username_label = ttk.Label(self, text="Username: ")
        global username_input
        username_input= ttk.Entry(self, width=15, textvariable=self.userName)
        username_label.grid(column=0, row=1, sticky="EW", padx=5, pady=5)
        username_input.grid(column=1, row=1, sticky="EW", padx=5, pady=5)
        username_input.focus()

        password_label = ttk.Label(self, text="Password: ")
        global password_input
        password_input= ttk.Entry(self, width=15, textvariable=self.password)
        password_label.grid(column=0, row=2, sticky="EW", padx=5, pady=5)
        password_input.grid(column=1, row=2, sticky="EW", padx=5, pady=5)

        login_button = tk.Button(self, text="Login", width=5, bg="#FCDEC0", command=self.get)
        login_button.grid(column=0, row=5, sticky="EW", padx=7, pady=7)

        signup_button = tk.Button(self, text="SignUp", width=5, bg="#FCDEC0",
                                  command=lambda: [controller.show_frame(Form)])
        signup_button.grid(column=1, row=5, sticky="EW", padx=7, pady=7)

        cancel_button = tk.Button(self, text="❌ Cancel", width=10, bg="#FCDEC0", command=close)
        cancel_button.grid(column=2, row=5, sticky="EW", padx=7, pady=7)


    def get(self):
        username=username_input.get()
        password=password_input.get()

        mydb = mysql.connect(host='localhost', user='root', password='', database='signup')
        mycursor = mydb.cursor()
        mycursor.execute("select * from information where username=%s and password = %s",(username_input.get(),password_input.get()))
        row = mycursor.fetchone()

        if row == None:
            messagebox.showerror("Error", "Invalid User Name And Password")
            username_input.delete(0, 'end')
            password_input.delete(0, 'end')
        else:
            messagebox.showinfo("Success", "Successfully Login")
            CarPricePrediction().show_frame(car)
            close()

        mydb.close()


class car(ttk.Frame):

    def __init__(self, container, controller):
        super().__init__(container)

        self.Kms_driven = tk.IntVar()
        global var1,var2,var3,var4,var5,var6,var7,var8,var9,presentprice
        var1 = tk.IntVar()
        var2 = tk.IntVar()
        var3 = tk.IntVar()
        var4 = tk.IntVar()
        var5 = tk.IntVar()
        var6 = tk.IntVar()
        var7 = tk.IntVar()
        var8 = tk.IntVar()
        var9 = tk.IntVar()
        presentprice=tk.DoubleVar()

        title = tk.Label(self, text="Details", fg="black", bg="salmon", font="Helvetica 15 bold")
        title.grid(sticky="EW", columnspan=10, padx=10, pady=10)

        Kms_driven_label = ttk.Label(self, text="Kms Driven: ")
        global Kms_driven_input
        Kms_driven_input= ttk.Entry(self, width=15, textvariable=self.Kms_driven)
        Kms_driven_label.grid(column=0, row=1, sticky="W", padx=5, pady=5)
        Kms_driven_input.grid(column=1, row=1, sticky="EW", padx=5, pady=5)
        Kms_driven_input.focus()

        Owner_type_label = ttk.Label(self, text="Owner: ")
        global Owner_type_input_Yes
        Owner_type_input_Yes= ttk.Checkbutton(self, text='Yes', variable=var1, onvalue=1, offvalue=0)
        global Owner_type_input_No
        Owner_type_input_No = ttk.Checkbutton(self, text='No', variable=var2, onvalue=1, offvalue=0)

        Owner_type_label.grid(column=0, row=2, sticky="W", padx=5, pady=5)
        Owner_type_input_Yes.grid(column=1, row=2, sticky="EW", padx=3, pady=3)
        Owner_type_input_No.grid(column=2, row=2, sticky="EW", padx=3, pady=3)

        Fuel_type_label = ttk.Label(self, text="Fuel type: ")
        global Fuel_type_input_CNG
        Fuel_type_input_CNG= ttk.Checkbutton(self, text='CNG', variable=var3, onvalue=1, offvalue=0)
        global Fuel_type_input_Petrol
        Fuel_type_input_Petrol= ttk.Checkbutton(self, text='Petrol', variable=var4, onvalue=1, offvalue=0)
        global Fuel_type_input_Diesel
        Fuel_type_input_Diesel= ttk.Checkbutton(self, text='Diesel', variable=var5, onvalue=1, offvalue=0)

        Fuel_type_label.grid(column=0, row=3, sticky="W", padx=5, pady=5)
        Fuel_type_input_CNG.grid(column=1, row=3, sticky="EW", padx=3, pady=3)
        Fuel_type_input_Petrol.grid(column=2, row=3, sticky="EW", padx=3, pady=3)
        Fuel_type_input_Diesel.grid(column=1, row=4, sticky="EW", padx=3, pady=3)

        Transmission_type_label = ttk.Label(self, text="Transmission-Type: ")
        global Transmission_type_input_Auto
        Transmission_type_input_Auto= ttk.Checkbutton(self, text='Automatic', variable=var6, onvalue=1, offvalue=0)
        global Transmission_type_input_Manual
        Transmission_type_input_Manual= ttk.Checkbutton(self, text='Manual', variable=var7, onvalue=1, offvalue=0)

        Transmission_type_label.grid(column=0, row=5, sticky="W", padx=5, pady=5)
        Transmission_type_input_Auto.grid(column=1, row=5, sticky="EW", padx=3, pady=3)
        Transmission_type_input_Manual.grid(column=2, row=5, sticky="EW", padx=3, pady=3)

        Seller_type_label = ttk.Label(self, text="Seller-Type: ")
        global Seller_type_input_Dealer
        Seller_type_input_Dealer= ttk.Checkbutton(self, text='Dealer', variable=var8, onvalue=1, offvalue=0)
        global Seller_type_input_Individual
        Seller_type_input_Individual= ttk.Checkbutton(self, text='Individual', variable=var9, onvalue=1, offvalue=0)

        Seller_type_label.grid(column=0, row=6, sticky="W", padx=5, pady=5)
        Seller_type_input_Dealer.grid(column=1, row=6, sticky="EW", padx=3, pady=3)
        Seller_type_input_Individual.grid(column=2, row=6, sticky="EW", padx=3, pady=3)

        presentprice_label = ttk.Label(self, text="present price: ")
        global presentprice_input
        presentprice_input = ttk.Entry(self, width=15, textvariable=presentprice)
        presentprice_label.grid(column=0, row=7, sticky="W", padx=5, pady=5)
        presentprice_input.grid(column=1, row=7, sticky="EW", padx=5, pady=5)
        presentprice_input.focus()

        predict_button = tk.Button(self, text="Predict", width=5, bg="#FCDEC0",command=self.values)
        predict_button.grid(column=0, row=8, sticky="EW", padx=7, pady=7)

        Back_button = tk.Button(self, text="↩️ Back", width=5, bg="#FCDEC0",
                                command=lambda: [controller.show_frame(login)])
        Back_button.grid(column=1, row=8, sticky="EW", padx=7, pady=7)

    def values(self):
        global Kms
        global Owner_yes
        global Owner_no
        global Fuel_cng
        global Fuel_petrol
        global Fuel_diesel
        global Trans_auto
        global Trans_manual
        global Seller_ind
        global Seller_dealer
        global Present_Price

        Kms = int(self.Kms_driven.get())

        Owner_yes = int(var1.get())
        Owner_no=int(var2.get())
        if Owner_yes==1:
            Owner=1
        else:
            Owner=0

        Fuel_cng = int(var3.get())
        Fuel_petrol = int(var4.get())
        Fuel_diesel = int(var5.get())


        Trans_auto = int(var6.get())
        Trans_manual = int(var7.get())

        Seller_dealer=int(var8.get())
        Seller_ind=int( var9.get())

        Present_Price=float(presentprice.get())

        global car_price

        car_price = np.array([Present_Price, Kms, Owner, Fuel_cng, Fuel_diesel, Fuel_petrol,
                              Trans_auto, Trans_manual, Seller_dealer, Seller_ind])
        car_price = scaler.transform(car_price.reshape(-1, 10))


        Prediction_result=(model.predict(car_price))
        label_prediction=tk.Label(self,text=Prediction_result)
        label_prediction.grid(column=0, row=10, sticky="W", padx=5, pady=5)


root = CarPricePrediction()
root.mainloop()




