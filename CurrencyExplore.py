# -*- coding: utf-8 -*-
from cgitb import text
import tkinter as tk
from tkinter import font
from turtle import width
import ttkbootstrap as ttk
from tkinter import messagebox
import requests
import json
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
from ttkwidgets.autocomplete import AutocompleteCombobox



class CurrencyExplorer(tk.Tk):
    
    def __init__(self):
        super().__init__()
        currencies = self.get_currencies()
        self.style = ttk.Style(theme="journal")
        self.title("Currency Explorer")
        self.geometry("280x230")
        self.show_plot = tk.BooleanVar()
        self.show_plot.trace_add("write", self.toggle_date_entry)
        self.title_label = ttk.Label(self, text="Currency Explorer", font= "Calibri 12 bold")
        self.from_currency_combo = AutocompleteCombobox(self, font= "Calibri 10 bold", width=5, completevalues=currencies)
        self.to_currency_combo = AutocompleteCombobox(self, font= "Calibri 10 bold", width=5, completevalues=currencies)
        self.amount_label = tk.Label(self, text="Amount:", font= "Calibri 10 bold")
        self.amount_entry = tk.Entry(self, font= "Calibri 10 bold",width=15)
        self.result_label = tk.Label(self, font= "Calibri 15 bold")
        self.switch_button = tk.Button(self, text="Switch", command=self.switch_currencies)
        self.convert_button = tk.Button(self, text="Convert", command=self.convert, width=15)
        self.start_date_label = tk.Label(self, text="Start Date (YYYY-MM-DD):", font= "Calibri 10 bold")
        self.start_date_entry = tk.Entry(self, font= "Calibri 10 bold")
        self.plot_checkbox = tk.Checkbutton(self, text="Show Timeseries", variable=self.show_plot)                 
        
        self.from_currency_combo['values'] = currencies
        self.to_currency_combo['values'] = currencies


        self.title_label.grid(row=0, column=0, columnspan=3, padx=(10, 10), pady=(10, 10)) 
        self.from_currency_combo.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))
        self.switch_button.grid(row=1, column=1, padx=(10, 0), pady=(10, 0))
        self.to_currency_combo.grid(row=1, column=2, padx=(10, 0), pady=(10, 0))
        self.amount_label.grid(row=2, column=0, padx=(10, 0), pady=(10, 0), sticky="E")
        self.amount_entry.grid(row=2, column=1, padx=(10, 0), pady=(10, 0)) 
        self.convert_button.grid(row=3, column=0, columnspan=3, padx=(10, 0), pady=(10, 0)) 
        self.result_label.grid(row=4, column=0, columnspan=3, padx=(10, 0), pady=(10, 0))
        self.start_date_label.grid(row=5, column=0, columnspan=3,padx=(10, 0), pady=(10, 0))
        self.start_date_entry.grid(row=6, column=0, columnspan=3,padx=(10, 0), pady=(10, 0))
        self.plot_checkbox.grid(row=7, column=0, columnspan=3, padx=(10, 0), pady=(10, 0))
        self.start_date_label.grid_remove()
        self.start_date_entry.grid_remove()
    
    def toggle_date_entry(self, *args):
        if self.show_plot.get():
            self.start_date_label.grid()
            self.start_date_entry.grid()
            self.geometry("280x300")
            self.convert_button.config(text="Convert and Plot")
        else:
            self.start_date_label.grid_remove()
            self.start_date_entry.grid_remove()
            self.geometry("280x230")
            self.convert_button.config(text="Convert")

    def get_currencies(self):        
        response = requests.get("https://api.exchangerate.host/symbols")
        data = response.json()
        return list(data["symbols"].keys())
       
    def convert(self):
        from_currency = self.from_currency_combo.get().upper()
        to_currency = self.to_currency_combo.get().upper()
        amount = self.amount_entry.get()
        self.from_currency_combo.set(from_currency.upper())
        self.to_currency_combo.set(to_currency.upper())

        if not from_currency or not to_currency or not amount:
            messagebox.showerror("Error", "Please select both currencies and enter an amount.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return

        response = requests.get(f'https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}')
        data = response.json()

        self.result_label['text'] = f'{amount} {from_currency} = {data["result"]} {to_currency}'

        if self.show_plot.get():  
            start_date = self.start_date_entry.get()
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
            timeseries_data = self.get_timeseries_data(from_currency, to_currency, start_date, end_date)
            self.plot_timeseries(timeseries_data, to_currency)

    def switch_currencies(self):

        from_currency = self.from_currency_combo.get()
        to_currency = self.to_currency_combo.get()

        self.from_currency_combo.set(to_currency.upper())
        self.to_currency_combo.set(from_currency.upper())
        
    def get_timeseries_data(self, from_currency, to_currency, start_date, end_date):
        url = f'https://api.exchangerate.host/timeseries?start_date={start_date}&end_date={end_date}&base={from_currency}&symbols={to_currency}'
        response = requests.get(url)
        data = response.json()
        return data

    def plot_timeseries(self, data, to_currency):
        dates = []
        rates = []

        for date, rate in data['rates'].items():
            dates.append(datetime.datetime.strptime(date, "%Y-%m-%d"))
            rates.append(rate[to_currency])

        fig, ax = plt.subplots()
        ax.plot(dates, rates)
        from_currency = self.from_currency_combo.get()
        to_currency = self.to_currency_combo.get()

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        fig.set_figwidth(11)
        fig.canvas.manager.set_window_title(f"Exchange rate over time {to_currency} - {from_currency}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Rate")
        ax.set_title("Exchange rate over time")
        
        plt.show()

app = CurrencyExplorer()
app.mainloop()
