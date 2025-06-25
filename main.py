from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

# Listy danych
pralnie = []
pracownicy = []
klienci = []
wszystkie_markery = []

class ObiektMapy:
    def __init__(self, nazwa, miejscowosc):
        self.nazwa = nazwa
        self.miejscowosc = miejscowosc
        self.coordinates = self.get_coordinates()
        self.marker = None

    def get_coordinates(self):
        url = f"https://pl.wikipedia.org/wiki/{self.miejscowosc}"
        try:
            response = requests.get(url).text
            soup = BeautifulSoup(response, "html.parser")
            longitude = float(soup.select(".longitude")[1].text.replace(",", "."))
            latitude = float(soup.select(".latitude")[1].text.replace(",", "."))
            return [latitude, longitude]
        except:
            return [52.23, 21.0]  # domyślna lokalizacja (Warszawa)

class Pralnia(ObiektMapy):
    pass

class Pracownik(ObiektMapy):
    def __init__(self, nazwa, miejscowosc, pralnia):
        self.pralnia = pralnia
        super().__init__(nazwa, miejscowosc)

class Klient(ObiektMapy):
    def __init__(self, nazwa, miejscowosc, pralnia):
        self.pralnia = pralnia
        super().__init__(nazwa, miejscowosc)

def dodaj_pralnie():
    nazwa = entry_name.get()
    miejscowosc = entry_location.get()
    if nazwa and miejscowosc:
        pralnia = Pralnia(nazwa, miejscowosc)
        pralnie.append(pralnia)
        listbox_pralnie.insert(END, pralnia.nazwa)
    clear_entries()

def dodaj_pracownika():
    nazwa = entry_name.get()
    miejscowosc = entry_location.get()
    pralnia = entry_extra.get()
    if nazwa and miejscowosc and pralnia:
        pracownik = Pracownik(nazwa, miejscowosc, pralnia)
        pracownicy.append(pracownik)
        listbox_pracownicy.insert(END, pracownik.nazwa)
    clear_entries()

def dodaj_klienta():
    nazwa = entry_name.get()
    miejscowosc = entry_location.get()
    pralnia = entry_extra.get()
    if nazwa and miejscowosc and pralnia:
        klient = Klient(nazwa, miejscowosc, pralnia)
        klienci.append(klient)
        listbox_klienci.insert(END, klient.nazwa)
    clear_entries()

def clear_entries():
    entry_name.delete(0, END)
    entry_location.delete(0, END)
    if entry_extra:
        entry_extra.delete(0, END)

def usun_wszystkie_markery():
    global wszystkie_markery
    for marker in wszystkie_markery:
        marker.delete()
    wszystkie_markery = []

def pokaz_wszystkie_pralnie():
    usun_wszystkie_markery()
    map_widget.set_zoom(6)
    for p in pralnie:
        p.marker = map_widget.set_marker(p.coordinates[0], p.coordinates[1], text=p.nazwa)
        wszystkie_markery.append(p.marker)

def pokaz_wszystkich_pracownikow():
    usun_wszystkie_markery()
    map_widget.set_zoom(6)
    for p in pracownicy:
        p.marker = map_widget.set_marker(p.coordinates[0], p.coordinates[1], text=p.nazwa)
        wszystkie_markery.append(p.marker)

def pokaz_klientow_pralni():
    usun_wszystkie_markery()
    nazwa_pralni = entry_pralnia_klient.get()
    if nazwa_pralni:
        for k in klienci:
            if k.pralnia == nazwa_pralni:
                k.marker = map_widget.set_marker(k.coordinates[0], k.coordinates[1], text=k.nazwa)
                wszystkie_markery.append(k.marker)


def pokaz_formularz(typ):
    for widget in frame_formularz.winfo_children():
        widget.destroy()

    Label(frame_formularz, text="Nazwa").grid(row=0, column=0)
    global entry_name
    entry_name = Entry(frame_formularz)
    entry_name.grid(row=0, column=1)

    Label(frame_formularz, text="Miejscowość").grid(row=1, column=0)
    global entry_location
    entry_location = Entry(frame_formularz)
    entry_location.grid(row=1, column=1)

    global entry_extra
    entry_extra = None

    if typ != "pralnia":
        Label(frame_formularz, text="Pralnia").grid(row=2, column=0)
        entry_extra = Entry(frame_formularz)
        entry_extra.grid(row=2, column=1)

def edytuj_pralnie():
    selected_index = listbox_pralnie.curselection()
    if selected_index:
        pralnia = pralnie[selected_index[0]]
        entry_name.delete(0, END)
        entry_name.insert(0, pralnia.nazwa)
        entry_location.delete(0, END)
        entry_location.insert(0, pralnia.miejscowosc)

        def zapisz():
            pralnia.nazwa = entry_name.get()
            pralnia.miejscowosc = entry_location.get()
            pralnia.coordinates = pralnia.get_coordinates()
            listbox_pralnie.delete(selected_index[0])
            listbox_pralnie.insert(selected_index[0], pralnia.nazwa)
            clear_entries()
            btn_zapisz.destroy()

        btn_zapisz = Button(frame_formularz, text="Zapisz zmiany", command=zapisz)
        btn_zapisz.grid(row=6, column=0, columnspan=2)

def edytuj_pracownika():
    selected_index = listbox_pracownicy.curselection()
    if selected_index:
        pracownik = pracownicy[selected_index[0]]
        entry_name.delete(0, END)
        entry_name.insert(0, pracownik.nazwa)
        entry_location.delete(0, END)
        entry_location.insert(0, pracownik.miejscowosc)
        entry_extra.delete(0, END)
        entry_extra.insert(0, pracownik.pralnia)

        def zapisz():
            pracownik.nazwa = entry_name.get()
            pracownik.miejscowosc = entry_location.get()
            pracownik.pralnia = entry_extra.get()
            pracownik.coordinates = pracownik.get_coordinates()
            listbox_pracownicy.delete(selected_index[0])
            listbox_pracownicy.insert(selected_index[0], pracownik.nazwa)
            clear_entries()
            btn_zapisz.destroy()

        btn_zapisz = Button(frame_formularz, text="Zapisz zmiany", command=zapisz)
        btn_zapisz.grid(row=6, column=0, columnspan=2)

def edytuj_klienta():
    selected_index = listbox_klienci.curselection()
    if selected_index:
        klient = klienci[selected_index[0]]
        entry_name.delete(0, END)
        entry_name.insert(0, klient.nazwa)
        entry_location.delete(0, END)
        entry_location.insert(0, klient.miejscowosc)
        entry_extra.delete(0, END)
        entry_extra.insert(0, klient.pralnia)

        def zapisz():
            klient.nazwa = entry_name.get()
            klient.miejscowosc = entry_location.get()
            klient.pralnia = entry_extra.get()
            klient.coordinates = klient.get_coordinates()
            listbox_klienci.delete(selected_index[0])
            listbox_klienci.insert(selected_index[0], klient.nazwa)
            clear_entries()
            btn_zapisz.destroy()

        btn_zapisz = Button(frame_formularz, text="Zapisz zmiany", command=zapisz)
        btn_zapisz.grid(row=6, column=0, columnspan=2)


root = Tk()
root.geometry("1200x800")
root.title("Mapa Pralni i Klientów")

frame_left = Frame(root)
frame_left.grid(row=0, column=0, sticky=N)

frame_formularz = Frame(frame_left)
frame_formularz.grid(row=3, column=0, columnspan=2, pady=10)

Label(frame_left, text="Pralnia dla klientów:").grid(row=6, column=0, columnspan=2)
entry_pralnia_klient = Entry(frame_left)
entry_pralnia_klient.grid(row=7, column=0, columnspan=2)
Button(frame_left, text="Pokaż klientów pralni", command=pokaz_klientow_pralni).grid(row=8, column=0, columnspan=2)

Label(frame_left, text="Pralnia dla pracowników:").grid(row=9, column=0, columnspan=2)
entry_pralnia_pracownik = Entry(frame_left)
entry_pralnia_pracownik.grid(row=10, column=0, columnspan=2)

Label(frame_left, text="Pralnie").grid(row=12, column=0)
listbox_pralnie = Listbox(frame_left, height=5)
listbox_pralnie.grid(row=13, column=0, columnspan=2)

Label(frame_left, text="Pracownicy").grid(row=14, column=0)
listbox_pracownicy = Listbox(frame_left, height=5)
listbox_pracownicy.grid(row=15, column=0, columnspan=2)

Label(frame_left, text="Klienci").grid(row=16, column=0)
listbox_klienci = Listbox(frame_left, height=5)
listbox_klienci.grid(row=17, column=0, columnspan=2)

map_widget = tkintermapview.TkinterMapView(root, width=900, height=700, corner_radius=0)
map_widget.grid(row=0, column=1)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)

root.mainloop()
