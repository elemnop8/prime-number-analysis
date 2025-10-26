""" experimente.py ist ein Experimentierskript, welches dem Nutzer ermöglicht
    verschiedene Algorithmen zur Bestimmung von Primzahlen kleiner gleich n,
    zu untersuchen.
    Die Verfahren werden hinsichtlich Speicherbedarf, Laufzeitverhalten,
    und Anzahl der Operationen verglichen.
    Die Ergebnisse werden grafisch dargestellt.
    Dies geschieht mithilfe der Funktionen naiv_prim_sieb(), 
    sieb_eratosthenes(), sieb_von_atkin(), measure_time(),
    read_number(), measure_memory_usage().
    von E. Tarielashvili, M. Nguyen
    pylint Version 3.1.0
    pylint score:  9.69/10
"""

# Die pylint Meldung zu Zeile 21 erscheint zu aufwendig zu beheben,
# da wahrscheinlich extra Funktionen notwenig wären

import sys
import numpy as np
from algorithmen import naiv_prim, sieb_eratosthenes, sieb_von_atkin
from hilfsmittel import measure_time, measure_memory_usage, reference_n, plot_vergleich, read_number
from hilfsmittel import referenzlinie, reference_n_logn, reference_n_log, reference_n_wurzel

def main():
    """ Hauptprogramm des Experiementierskripts
    """
    # Informationen an den Nutzer
    print("Ihnen stehen 3 verschiedene Algorithmen zur Verfügung für die "
          "Bestimmung \naller Primzahlen bis zur gewählten Obergrenze n."
          "\nUnd zwar ein naiver Algorithmus, der Sieb von Eratosthenes und \n"
          "der Sieb von Atkin.\nDieses Programm dient zur Untersuchung dieser "
          + "Algorithmen.\nWas wollen sie zunächst untersuchen?")
    print("1. Die Algorithmen hinsichtlich ihrer Laufzeitern \n"
          "2. Die Algorithmen hinsichtlich ihrem Speicherbedarf")
    choice = read_number("\nIhre Wahl (1 oder 2): ", 1, 2, int)

    if choice == 1 :
        print("\nWollen Sie...\n"+
              "1. Die Laufzeiten für eine gewählte Obergrenze bestimmen \n"
              "2. Die Laufzeiten grafisch vergleichen")
        wahl = read_number("\nIhre Wahl (1 oder 2): ", 1, 2, int)
        # read_number für die Nutzereingabe
        try:
            n =read_number("Wählen Sie eine Obergrenze (zwischen 1 und 10^6): ", 1, 10**6, int)
        except ValueError as e:
            if str(e) == "Leere Eingabe. Das Programm wurde abgebrochen.":
                print(str(e))
                sys.exit()  # Beendet das Programm ohne Fehlermeldung
        # Wenn die Liste der erzeugten Primzahlen max 30 Elemente hat, wird sie ausgegeben
        if n<127:
            print(f"Primzahlen kleiner gleich {n}:\n", sieb_eratosthenes(n))

        if wahl == 1 :
            # gibt die Laufzeiten für gewähltes n an
            print(f"\nNaiver Algorithmus: \nLaufzeit (ms): {measure_time(naiv_prim, n)}")
            print(f"\nSieb von Eratosthenes: \nLaufzeit (ms): {measure_time(sieb_eratosthenes, n)}")
            print(f"\nSieb von Atkin: \nLaufzeit (ms): {measure_time(sieb_von_atkin, n)}")

        if wahl == 2 :
            x = np.geomspace(2,n,100,endpoint=True, dtype=np.int64)
            m = 10000

            # Messwerte, die geplotted werden
            naive_times = [measure_time(naiv_prim, n) for n in x]
            sieve_times = [measure_time(sieb_eratosthenes, n) for n in x]
            atkin_times = [measure_time(sieb_von_atkin, n) for n in x]

            # Werte der Referenzlinien
            scaling_atkin = referenzlinie(measure_time, sieb_von_atkin, reference_n, m, x)
            scaling_era = referenzlinie(measure_time, sieb_eratosthenes, reference_n_log, m, x)
            scaling_naive =  referenzlinie(measure_time, naiv_prim, reference_n_wurzel, m, x)

            # Label der Referenzlinien
            labels_scaling_times = [
                    "Eratosthenes $O(n(log(log(n)))$",
                    "Atkin $O(n)$",
                    "Naives $O(n\\sqrt{n})$",
                ]

            # Label der Messwerte
            labels_actual_times = [
                    "Sieb von Eratosthenes",
                    "Sieb von Atkin",
                    "Naiver Algorithmus"
                ]

            # Plot Vergleich der Laufzeiten
            plot_vergleich(
                    x,
                    [sieve_times, atkin_times, naive_times],
                    labels_actual_times,
                    'Laufzeitvergleich der Primzahl-Algorithmen',
                    'Laufzeit (ms)',
                    [scaling_era, scaling_atkin, scaling_naive],
                    labels_scaling_times,
                    filename = 'laufzeit_plot.png'
                    )

    if choice == 2 :
        print("Wollen Sie...\n"+
              "1. Den Speicherbedarf für eine gewählte Obergrenze bestimmen \n"
              "2. Den Speicherbedarf grafisch vergleichen")
        wahl = read_number("Ihre Wahl (1 oder 2): ", 1, 2, int)
        try:
            n =read_number("Wählen Sie eine Obergrenze (zwischen 1 und 10^5): ", 1, 10**5, int)
        except ValueError as e:
            if str(e) == "Leere Eingabe. Das Programm wurde abgebrochen.":
                print(str(e))
                sys.exit()  # Beendet das Programm ohne Fehlermeldung
        # Wenn die Liste der erzeugten Primzahlen max 30 Elemente hat, wird sie ausgegeben
        if n<127:
            print(f"Primzahlen kleiner gleich {n}:\n", sieb_eratosthenes(n))

        if wahl == 1 :
            print("\nNaiver Algorithmus: \nSpeicherverbrauch (MiB):"+
                  f" {measure_memory_usage(naiv_prim, n)}")
            print("\nSieb von Eratosthenes: \nSpeicherverbrauch (MiB):"+
                  f" {measure_memory_usage(sieb_eratosthenes, n)}")
            print("\nSieb von Atkin: \nSpeicherverbrauch (MiB):"+
                  f" {measure_memory_usage(sieb_von_atkin, n)}")

        if wahl == 2 :
            x = np.geomspace(2,n,100,endpoint=True, dtype=np.int64)
            m = 10000

            # Messwerte, die geplotted werden
            naive_memory = [measure_memory_usage(naiv_prim, n) for n in x]
            sieve_memory = [measure_memory_usage(sieb_eratosthenes, n) for n in x]
            atkin_memory = [measure_memory_usage(sieb_von_atkin, n) for n in x]

            # Werte der Referenzlinien
            scaling_atkin = referenzlinie(measure_memory_usage, sieb_von_atkin, reference_n, m, x)
            scaling_era = referenzlinie(measure_memory_usage, sieb_eratosthenes, reference_n, m, x)
            scaling_naive =  referenzlinie(measure_memory_usage, naiv_prim, reference_n_logn, m, x)

            # Label der Referenzlinien
            labels_scaling_memory = [
                    "Eratosthenes $O(n)$",
                    "Atkin $O(n)$",
                    "Naiv $O(\\frac{n}{\\log(n)})$"
                ]

            # Label der Messwerte
            labels_actual_memory = [
                    "Sieb von Eratosthenes",
                    "Sieb von Atkin",
                    "Naiver Algorithmus"
                ]

            # Plot Vergleich der Laufzeiten
            plot_vergleich(
                    x,
                    [sieve_memory, atkin_memory, naive_memory],
                    labels_actual_memory,
                    'Speicherbedarf der Primzahl-Algorithmen',
                    'Speicherbedarf (MiB)',
                    [scaling_era, scaling_atkin, scaling_naive],
                    labels_scaling_memory,
                    filename = 'speicherbedarf_plot.png')

if __name__ == "__main__":
    main()
