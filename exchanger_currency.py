import tkinter as tk
import sys
import requests
import json
import pandas as pd
import tkinter.messagebox
from tkinter import ttk


class Exchange:
    '''class for exchange currencies app'''

    def __init__(self, master):
        '''
        Create window of aplication
        :param master: (Tk) main aplication window
        '''
        self.data()

        self.currency1 = tk.StringVar(master)
        self.currency2 = tk.StringVar(master)
        self.currency1.set("waluta")
        self.currency2.set("waluta")

        self.f_currency = tk.LabelFrame(master, text="Wybierz pierwszą waltuę", bg="#FAF0E6", labelanchor="n")
        self.f_currency_opt = ttk.Combobox(self.f_currency, textvariable=self.currency1)

        self.s_currency = tk.LabelFrame(master, text="Wybierz drugą walutę", bg="#FAF0E6", labelanchor="n")
        self.s_currency_opt = ttk.Combobox(self.s_currency, textvariable=self.currency2)

        self.switch = tk.Button(master, text="<->", command=self.switch_currencies, bg="#FFFAFA", height=1, width=5)

        self.value = tk.Label(master, text="Wartość:", bg="#FAF0E6")
        self.value_num = tk.Entry(master, font=("Helvetica", "10"))

        self.count = tk.Button(master, text="Przelicz", command=self.new_value, height=2, width=10, bg="#FFFAFA")
        self.result = tk.Label(master, text="Wynik:", bg="#FAF0E6")
        self.text = tk.Label(master, text="", bg="white", font=("Helvetica", "12"), width=27)

        self.exit = tk.Button(master, text="Wyjście", command=self.quit, height=2, width=10, fg="red", bg="#FFFAFA")

        self.cleaning = tk.Button(master, text="Wyczyść", command=self.clean, height=2, width=10, bg="#FFFAFA")

        self.frames()
        self.grid()

    def frames(self):
        '''
        Give Combobox values
        '''
        data = self.value_list()
        for i in [self.f_currency_opt, self.s_currency_opt]:
            i["values"] = data
            i['state'] = 'readonly'

    def grid(self):
        '''
        Order widgets on the windows
        '''
        self.f_currency.grid(row=0, column=0, padx=20, pady=10)
        self.f_currency_opt.grid(padx=20, pady=10)
        self.s_currency.grid(row=0, column=2, padx=20, pady=10)
        self.s_currency_opt.grid(padx=20, pady=10)
        self.switch.grid(row=0, column=1)
        self.value.grid(row=1, column=1)
        self.value_num.grid(row=2, column=1)
        self.count.grid(row=3, column=1, pady=15)
        self.result.grid(row=4, column=1)
        self.text.grid(row=5, column=1)
        self.exit.grid(row=6, column=2, pady=15)
        self.cleaning.grid(row=6, column=0, pady=15)

    @staticmethod
    def quit():
        '''
        Exit the window with aplication
        '''
        sys.exit()

    def courencys_list(self):
        json_str = self.data_reading()
        json_to_pd = pd.read_json(json_str).set_index("currency")
        frame = pd.DataFrame(json_to_pd)
        frame.loc["złoty polski"] = ['PLN', 1]
        return frame

    def value_list(self):
        '''
        Create list of value to choice
        :return: (list) list of currencies
        '''
        frame = self.courencys_list()
        return frame.index.values.tolist()

    def is_number(self):
        '''
        Check if value entered value is number
        :return: (bool) True - yes, False - no
        '''
        try:
            float(self.value_num.get())
            return True
        except ValueError:
            return False

    def new_value(self):
        '''
        Counts value of new currency
        '''
        if self.currency1.get() == self.currency2.get():
            tkinter.messagebox.showwarning("Ostrzeżenie", "Waluty nie mogą być takie same.")
        elif self.currency1.get() == "waluta" or self.currency2.get() == "waluta":
            tkinter.messagebox.showwarning("Ostrzeżenie", "Wybierz obie waluty.")
        elif not self.is_number():
            tkinter.messagebox.showwarning("Ostrzeżenie",
                                        "Nie można przekonwertować tekstu.\nJeśli użyłeś przecinka, użyj kropki.")
        else:
            frame = self.courencys_list()
            value = round((float(self.value_num.get()) * frame.loc[self.currency1.get()]["mid"]) /
                          frame.loc[self.currency2.get()]["mid"], 4)
            v_code = frame.loc[self.currency2.get()]["code"]
            self.text["text"] = f"{value} {v_code}"

    def switch_currencies(self):
        '''
        Switch one currency to another one
        '''
        first, second = self.currency1.get(), self.currency2.get()
        self.currency1.set(second)
        self.currency2.set(first)

    @staticmethod
    def data_reading():
        '''
        Reading data from file with currencies rates
        '''
        with open("currencies_data.txt", "r") as c_data:
            data = c_data.read()
        return data

    def data(self):
        '''
        Load data frome nbp page or form file
        '''
        try:
            response = requests.get('http://api.nbp.pl/api/exchangerates/tables/A').json()[0]["rates"]
            data = json.dumps(response)
        except:
            tkinter.messagebox.showerror(title="Problem z połączeniem", message="Najnowsze dane są niedostępne")
            answer = tkinter.messagebox.askokcancel(title="Dane z pliku",
                                                    message="Czy załadować dane z pliku?")
            if answer:
                try:
                    self.data_reading()
                except FileNotFoundError:
                    tkinter.messagebox.showerror(title="Błąd", message="Plik z danymi nie został znaleziony")
                    self.quit()
            else:
                self.quit()
        else:
            with open("currencies_data.txt", "w") as c_data:
                c_data.write(data)

    def clean(self):
        '''
        Returns the window to its original state
        '''
        self.currency1.set("waluta")
        self.currency2.set("waluta")
        self.value_num.delete(0, 'end')
        self.text["text"] = ""


def main():
    '''
    Main function with exchanger currencies app
    '''
    root = tk.Tk()
    root.configure(background='#FAF0E6')
    root.title("Konwenter walut")
    root.geometry('701x330')
    root.resizable(False, False)
    Exchange(root)
    root.mainloop()


if __name__ == "__main__":
    main()