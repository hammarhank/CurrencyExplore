# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import requests
import json

class CurrencyExplorer(tk.Tk):
    
    def __init__(self):
        super().__init__()

        self.title("Currency Explorer")
        self.geometry("400x600")
        #TODO: rita upp guit med tkinter
        self.from_currency_combo = ttk.Combobox(self)
        self.to_currency_combo = ttk.Combobox(self)
        self.amount_entry = tk.Entry(self)
        self.result_label = tk.Label(self)
        self.convert_button = tk.Button(self, text="Convert", command=self.convert)

        
        currencies = self.get_currencies()
        self.from_currency_combo['values'] = currencies
        self.to_currency_combo['values'] = currencies

        self.from_currency_combo.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))
        self.to_currency_combo.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))
        self.amount_entry.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))
        self.convert_button.grid(row=1, column=1, padx=(10, 0), pady=(10, 0))
        self.result_label.grid(row=2, column=0, columnspan=2, padx=(10, 0), pady=(10, 0))
        

    def get_currencies(self):
        #TODO: hämta valutavärden från exchangerate.host
        response = requests.get("https://api.exchangerate.host/symbols")
        data = response.json()
        return list(data["symbols"].keys())
        
    def convert(self):
        #Konvertera mellan olika valutor.
        0
app = CurrencyExplorer()
app.mainloop()