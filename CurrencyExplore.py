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

    def get_currencies(self):
        #TODO: h�mta valutav�rden fr�n exchangerate.host
        0
    def convert(self):
        #Konvertera mellan olika valutor.
        0

CurrencyExplorer.mainloop()