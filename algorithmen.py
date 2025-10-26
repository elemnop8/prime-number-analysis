""" Das Programm dient zur Bestimmung aller Primzahlen
    kleiner gleich n (n in den natürlichen Zahlen).
    Hierfür werden drei verschiedene Algorithmen implementiert:
    Ein naiver Algorithmus, Sieb des Eratosthenes und
    Sieb von Atkin.
    von E. Tarielashvili, M. Nguyen
    pylint Version 3.1.0
    pylint score: 10/10
"""
import math
import numpy as np

def naiv_prim(n):
    """
    Naiver Algorithmus zur Berechnung der ersten Primzahlen kleinergleich n.

    Parameters
    ----------
    n : int
        Obergrenze der zu berechnenden Primzahlen

    Returns
    ----------
    np.array
        Array mit den Primzahlen kleinergleich n
    """
    primzahlen = np.array([]) # erstellen leerer Liste zum Speichern der Primzahlen
    for a in range(2, n + 1):
        #Überprüfung, ob a eine Primzahl ist
        #Überprüfung, ob a durch i teilbar
        if all(a % i != 0 for i in range(2, int(math.sqrt(a)) + 1)):
            primzahlen = np.append(primzahlen, a)
    return primzahlen

def sieb_eratosthenes(n):
    """
    Berechnung der ersten Primzahlen kleinergleich n mit Sieb des Eratosthenes.

    Parameters
    ----------
    n : int
        Obergrenze der zu berechnenden Primzahlen

    Returns
    ----------
    np.array
        Array mit den Primzahlen kleinergleich n
    """
    # Liste mit Wahrheitswerten
    primzahlen = np.ones(n + 1, dtype=bool)
    primzahlen[0:2] = False  # 0 und 1 sind keine Primzahlen
    # Startwert für die Primzahlprüfung
    p = 2
    while p * p <= n:
        # Wenn p eine Primzahl ist dann alle Vielfachen von p nicht prim
        if primzahlen[p]:
            primzahlen[p * p:n + 1:p] = False
        p += 1

    # Rückgabe der Indizes, die True sind, also primzahlen
    return np.nonzero(primzahlen)[0]

def sieb_von_atkin(n):
    """
    Berechnung der ersten Primzahlen kleiner gleich n mit Sieb von Atkin.

    Parameters
    ----------
    n : int
        Obergrenze der zu berechnenden Primzahlen

    Returns
    ----------
    prim : np.array
        Array mit den Primzahlen kleinergleich n
    """
    if n < 2:
        return np.array([])

    if n == 2:
        return np.array([2])

    # Initialisierung des Sieb-Arrays mit False-Werten
    sieb = np.zeros(n + 1, dtype=bool)

    limit = int(math.sqrt(n)) + 1

    # Hauptteil des Sieb von Atkin2
    for x in range(1, limit):
        for y in range(1, limit):
            x2 = x * x
            y2 = y * y

            # Hauptformel 1: n = 4x^2 + y^2
            m = 4 * x2 + y2
            if m <= n and (m % 12 == 1 or m % 12 == 5):
                sieb[m] = not sieb[m]

            # Hauptformel 2: n = 3x^2 + y^2
            m = 3 * x2 + y2
            if m <= n and m % 12 == 7:
                sieb[m] =not sieb[m]

            # Hauptformel 3: n = 3x^2 - y^2 (x > y)
            if x > y:
                m = 3 * x2 - y2
                if m <= n and m % 12 == 11:
                    sieb[m] =not sieb[m]

    # Markiere alle Vielfachen von Quadraten als nicht prim
    for a in range(5, limit):
        if sieb[a]:
            a2 = a * a
            sieb[a2:n + 1:a2] = False

    # Rückgabe der Indizes, die True sind, also Primzahlen
    prim = np.concatenate(([2, 3], np.nonzero(sieb[5:])[0] + 5))

    return prim

def main():
    """ Hauptprogramm des Experiementierskripts
    """
    # Informationen an den Nutzer
    print("Dieses Modul beinhaltet 3 Algorithmen zur",
          "Berechnung aller Primzahlen bis zu einer gewählten Obergrenze.\n")

    # Nutzereingabe
    a = True
    while a:
        try:
            n = int(input("Wählen Sie eine Obergrenze "+
                          "(eine natürliche Zahl): "))
            if n<0:
                raise ValueError
            a = False
        except ValueError:
            print("Ungültige Eingabe. Bitte geben Sie eine natürliche Zahl ein.")

    # Ausgabe der Primzahlen
    print(f"\nMit dem naiven Algorithmus bestimmten Primzahlen bis {n}:\n",
          naiv_prim(n))
    print(f"\nMit dem Sieb des Eratosthenes bestimmten Primzahlen bis {n}:\n",
          sieb_eratosthenes(n))
    print(f"\nMit dem Sieb von Atkin bestimmten Primzahlen bis {n}:\n",
          sieb_von_atkin(n))

    print("\nWie erwartet geben alle 3 Algorithmen das gleichen Werte aus.")

if __name__ == "__main__":
    main()
