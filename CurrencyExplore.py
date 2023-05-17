# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import font
import requests
import json

class CurrencyExplorer(tk.Tk):
    
    def __init__(self):
        super().__init__()

        self.title("Currency Explorer")
        self.geometry("400x150")
        self.title_label = ttk.Label(self, text="Currency Explorer", font= "Calibri 12 bold")
        self.from_currency_combo = ttk.Combobox(self, font= "Calibri 10 bold")
        self.to_currency_combo = ttk.Combobox(self, font= "Calibri 10 bold")
        self.amount_entry = tk.Entry(self, font= "Calibri 10 bold")
        self.result_label = tk.Label(self, font= "Calibri 15 bold")
        self.convert_button = tk.Button(self, text="Convert", command=self.convert)
                                        
        currencies = self.get_currencies()
        self.from_currency_combo['values'] = currencies
        self.to_currency_combo['values'] = currencies

        self.title_label.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(10, 10))
        self.from_currency_combo.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))
        self.to_currency_combo.grid(row=1, column=1, padx=(10, 0), pady=(10, 0))
        self.amount_entry.grid(row=2, column=0, padx=(10, 0), pady=(10, 0))
        self.convert_button.grid(row=2, column=1, padx=(10, 0), pady=(10, 0))
        self.result_label.grid(row=3, column=0, columnspan=2, padx=(10, 0), pady=(10, 0))
        

    def get_currencies(self):        
        response = requests.get("https://api.exchangerate.host/symbols")
        data = response.json()
        return list(data["symbols"].keys())
       
    def convert(self):
        from_currency = self.from_currency_combo.get()
        to_currency = self.to_currency_combo.get()
        amount = self.amount_entry.get()

       
        if not from_currency or not to_currency or not amount:
            self.result_label['text'] = 'Please select both currencies and enter an amount.'
            return

        try:
            amount = float(amount)
        except ValueError:
            self.result_label['text'] = 'Please enter a valid amount.'
            return

        response = requests.get(f'https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}')
        data = response.json()

        self.result_label['text'] = f'{amount} {from_currency} = {data["result"]} {to_currency}'


app = CurrencyExplorer()
app.mainloop()