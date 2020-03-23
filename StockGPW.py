from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
import requests
import pandas as pd
from tkinter import *
import lxml.html as lh
import tkinter as tk

def CurSelect(event):
    listbox2.configure(state=tk.NORMAL)
    listbox2.delete(0,END)
    values = [listbox.get(idx) for idx in listbox.curselection()]
    for a in values:
        listbox2.insert(END,a)
    listbox2.configure(state=tk.DISABLED)

def find_share_prices():
    list_of_companies = []
    values = [listbox.get(idx) for idx in listbox.curselection()]
    for i in values:
        list_of_companies.append(i[1])
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(chrome_options=chrome_options,
                               executable_path='C:\\Users\\PC\\python_IE_broswer\\chromedriver')
    list_of_shareprices = []
    current_time = datetime.datetime.now()
    curr_time = str(current_time)[0:-7]
    label2 = Label(window, text=f"Kurs z {curr_time}")
    label2.place(x=540, y=320, width = 240, height = 40)
    textbox_with_shareprices = Text(window)
    textbox_with_shareprices.place(x=540, y=350, width=220, height=230)
    for s in list_of_companies:
        browser.get('https://www.stooq.pl/q/?s={}'.format(s))
        actual_prices = browser.find_elements_by_id("f18")[2]
        price = actual_prices.text
        list_of_shareprices.append(price)
        textbox_with_shareprices.insert(END,f"{list_of_companies[list_of_companies.index(s)]}      {list_of_shareprices[list_of_companies.index(s)]}\n")

#'MAIN'

#main window
window = tk.Tk()
window.title("Spółki giełdowe")
window.geometry("800x600")

#1 label
title = Label(window,text = "Wybierz spółki")
title.pack(side="left")

#2 label
label2 = Label(window,text = "Wybrane spółki")
label2.place(x = 595, y = 14, width = 120, height = 20)

#listbox
url = 'http://infostrefa.com/infostrefa/pl/spolki'
html = requests.get(url).content
df_list = pd.read_html(html)
df = df_list[-1]
df = df[['Nazwa giełdowa','Ticker']]
lst = df.values.tolist()
listbox = Listbox(window,width=70,height=90,selectmode='multiple')
for item in lst:
    listbox.insert(END,item)
listbox.bind('<<ListboxSelect>>',CurSelect)
listbox.pack(side ="left")

#listbox2
listbox2 = Listbox(window)
listbox2.place(x = 540, y = 40, width = 220, height = 230)

#Button
button = tk.Button(window, text = "Wyszukaj kursy", command=find_share_prices)
button.place(x = 595, y = 275, width = 120, height = 30)

window.mainloop()