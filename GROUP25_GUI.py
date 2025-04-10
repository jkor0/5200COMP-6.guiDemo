#Inconsistent code due to learning Tkinter;

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf
import pandas as pd

import tkinter as tk
from tkinter import *
from tkinter import ttk

def display_stock_graph(frame, ticker):
    # Fetch stock data
    stock_data = yf.download(ticker, period="1y")  # Get 1 year of data

    if stock_data.empty:
        ttk.Label(frame, text=f"Could not retrieve data for {ticker}").pack()
        return

    # Create a matplotlib figure and axes
    fig, ax = plt.subplots(figsize=(6, 4))  # Adjust figure size as needed
    ax.plot(stock_data['Close'])
    ax.set_title(f"{ticker} Stock Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.grid(True)

    # Embed the plot into the Tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def clear_page():
    #Destroys all widgets in root window not children of navbar
    for widget in root.winfo_children():
        if widget != nav_frame:
            widget.destroy()

def home_page():
    clear_page()

    content_label = ttk.Label(root, text="Select a stock", font=("Arial", 14))
    content_label.grid(pady=20)

    search_label = ttk.Label(root, text="Search")
    search_label.grid(column=0)
    search_entry = ttk.Entry(root)
    search_entry.grid(column=0)

    table = ttk.Treeview(root, columns=('ticker'))
    table.heading('#0', text='Stock')
    table.heading('ticker', text='Ticker')

    table.insert("",'end', text='Apple Inc', values=('AAPL'))
    table.insert("",'end', text='Microsoft Corporation', values=('MSFT'))
    table.insert("",'end', text='NVIDIA Corp', values=('NVDA'))
    table.insert("",'end', text='Amazon.com, Inc', values=('AMZN'))
    table.insert("",'end', text='Alphabet Inc', values=('GOOGL'))
    table.insert("",'end', text='Meta Platforms, Inc', values=('META'))
    table.insert("",'end', text='Tesla, Inc', values=('TSLA'))

    table.bind("<ButtonRelease-1>", item_clicked)

    table.grid(padx=10, pady=10)

    nav_frame.grid(column=0, columnspan=4, sticky=EW)

def history_page():
    clear_page()
    content_label = ttk.Label(root, text="Content for Past History Page", font=("Arial", 14))
    content_label.grid(pady=20)

def display_stock(name, ticker):
    clear_page()

    #Frame for anything not navbar
    ttk.Style().configure("stock.TFrame", background="grey")
    f = ttk.Frame(root, style="stock.TFrame")
    f.grid(row=1, column=0, columnspan=4, pady=20, sticky=NSEW)
    f.grid_rowconfigure(1, weight=1)
    f.grid_columnconfigure(1, weight=1)

    #Stock Table
    ttk.Style().configure("minor.Treeview")
    table = ttk.Treeview(f, columns=('ticker'), style="minor.Treeview")
    table.heading('#0', text='Stock')
    table.heading('ticker', text='Ticker')

    table.insert("",'end', text='Apple Inc', values=('AAPL'))
    table.insert("",'end', text='Microsoft Corporation', values=('MSFT'))
    table.insert("",'end', text='NVIDIA Corp', values=('NVDA'))
    table.insert("",'end', text='Amazon.com, Inc', values=('AMZN'))
    table.insert("",'end', text='Alphabet Inc', values=('GOOGL'))
    table.insert("",'end', text='Meta Platforms, Inc', values=('META'))
    table.insert("",'end', text='Tesla, Inc', values=('TSLA'))

    table.bind("<ButtonRelease-1>", item_clicked)
    table.grid(row=1, column=3, pady=10, padx=10, sticky=NSEW)
    
    #Content taking up ~2/3 leftside space
    content_frame = ttk.Frame(f)
    content_frame.grid(row=1, column=1, sticky=NSEW)
    content_frame.grid_columnconfigure(0, weight=1)
    
    stock_label = ttk.Label(content_frame, text=name, font=("Arial", 14))
    stock_label.grid(row=1, column=0, pady=20)

    #Stock graph
    ttk.Style().configure("graphCol.TFrame", background="black")
    graph_frame = ttk.Frame(content_frame, style="graphCol.TFrame")
    graph_frame.grid(row=2, column=0, padx=20, pady=20, rowspan=2, columnspan=2, sticky=NSEW) 
    display_stock_graph(graph_frame, ticker)
    
    #Forecasting
    forecast_frame = ttk.Frame(content_frame, width=50)
    forecast_frame.grid(row=4, column=0, columnspan=2, rowspan=3)
    forecast_label = ttk.Label(forecast_frame, text="Enter a date for forecasting:")
    forecast_label.grid(row=0, column=0,padx=20, pady=10, columnspan=1)

    forecast_entry = ttk.Entry(forecast_frame)
    forecast_entry.grid(row=1, column=0, padx=20, columnspan=1)

    def get_input(): # Not necessary for GUI demo, but would be used in implementation
        user_input = forecast_entry.get()
        print("User input:", user_input)
    
    button = ttk.Button(forecast_frame, text="Get Forecast", command=get_input)
    button.grid(row=2,column=0,pady=10, rowspan=1)

    text_box = tk.Text(forecast_frame, height=5, width=40)
    text_box.insert('1.0', 'Forecasting details and risk analysis: \n...')
    text_box.grid(row=0, column=1, rowspan=2, padx=50, pady=10)

    #News analysis
    news_box = tk.Text(content_frame, height=5, width=80)
    news_box.insert('1.0', 'News analysis of the most relevant stories to this stock: \n...')
    news_box.grid(row=7, column=0, padx=20, pady=20, columnspan=2)
    

    nav_frame.grid(column=0, columnspan=4, sticky=EW)
    
def item_clicked(event):
    tree = event.widget
    selected_item = tree.selection()

    if selected_item:
        item_text = tree.item(selected_item, "text")
        item_ticker = tree.item(selected_item, "values")
        print(f"You clicked on: {item_text}")
        display_stock(item_text, item_ticker)


## Create the main window ##
root = Tk()
root.title("Home")

root.grid_columnconfigure(0, weight=1)

# Nav bar
ttk.Style().configure("navbar.TFrame", background="lightblue")
nav_frame = ttk.Frame(root, style="navbar.TFrame", height=50)
nav_frame.grid(column=0, sticky=EW)
nav_frame.grid_columnconfigure(2, weight=1)
nav_frame.grid_columnconfigure(3, weight=0)
nav_frame.grid_rowconfigure(0, pad=40)

# Nav bar buttons
ttk.Style().configure("TButton", background="lightblue")

home_button = ttk.Button(nav_frame, text="Home", command=lambda: home_page())
home_button.grid(column=1, row=0, padx=20, sticky=E)

history_button = ttk.Button(nav_frame, text="History", command=lambda: history_page())
history_button.grid(column=3, row=0, padx=20, sticky=W)

home_page()

root.mainloop()
