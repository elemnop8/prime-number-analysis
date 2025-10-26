""" Das Programm dient zur Untersuchung von Algorithmen
    hinsichtlich Speicherbedarf und Laufzeitverhalten.
    Dafür werden 3 verschiedene Hilfsfunktionen definiert:
    measure_time() misst die Laufzeit eines Algorithmus.
    measure_memory_usage() misst den Spitzen-Speicherbedarf
    während der Ausführung des Algorithmus.
    read_number() erleichtert das Einlesen von Nutzereingaben.
    plot_vergleich() erzeugt einen Log-Log-Plot für den Vergleich.
    referenzlinie() Berechnet eine Referenzlinie durch
    Skalierung eines Referenzwertes
    Von M. Nguyen, E. Tarielashvili
    pylint Version 3.1.0
    pylint score: 9.81/10
"""
# Die pylint Meldung zu Zeile 163 erscheint zu aufwendig zu beheben,
# da wahrscheinlich extra Funktionen notwenig wären

import math
import time
import sys
import tracemalloc
import matplotlib.pyplot as plt
import numpy as np
from algorithmen import naiv_prim, sieb_eratosthenes, sieb_von_atkin

def measure_time(algorithm, n, runs=1):
    """ 
    Funktion zum Messen der Laufzeit eines Algorithmus.

    Parameters
    ----------
    algorithm : function
        Algorithmus, dessen Laufzeit gemessen werden soll
    n : int
        Parameter, der an den Algorithmus übergeben wird
    runs : int
        Anzahl der Messungen für genauere Schätzungen

    Returns
    ----------
    float
        Die gemessene Laufzeit des Algorithmus in Millisekunden
    """
    total_time = 0
    for _ in range(runs):
        # Startzeit messen
        start_time = time.perf_counter_ns()
        # Algorithmus mit Parameter n ausführen
        algorithm(n)
        # Endzeit messen
        end_time = time.perf_counter_ns()
        # Zeit in Millisekunden
        total_time += (end_time - start_time) / 1000000
    return total_time / runs

def measure_memory_usage(algorithm, n, runs=1):
    """
    Misst den Spitzen-Speicherbedarf während der Ausführung des Algorithmus.

    Parameters
    ----------
    algorithm : function 
        Algorithmus, dessen Speicherbedarf gemessen werden soll
    n : int 
        Parameter, der an den Algorithmus übergeben wird
    runs : int
        Anzahl der Messungen für genauere Schätzungen

    Returns
    ---------
    float
        Der gemessene Spitzen-Speicherbedarf des Algorithmus in Mebibyte
    """
    max_memory = 0  # Variable zur Speicherung des höchsten gemessenen Speicherverbrauchs
    # Mehrfaches Ausführen des Algorithmus
    for _ in range(runs):
        # Starten der Speicherverfolgung
        tracemalloc.start()
        # Ausführen des Algorithmus mit Parameter n
        algorithm(n)
        # Abrufen des aktuellen und Spitzen-Speicherverbrauchs
        peak = tracemalloc.get_traced_memory()[-1]
        # Stoppen der Speicherverfolgung
        tracemalloc.stop()
        # Aktualisieren des maximalen Speicherverbrauchs
        max_memory = max(max_memory, peak)
    # Konvertieren in Mebibyte (1 MiB = 1024 KiB)
    return max_memory / (1024*1024)  # Rückgabe in Mebibyte

def read_number(question: str,
                lower_limit: float = -math.inf,
                upper_limit: float = math.inf,
                data_type: type = float
                ):
    """
    Überprüfung der Nutzeingabe auf ihre Gültigkeit.

    Parameter
    ----------
    question : str 
        Frage, die der Nutzer beantworten soll
    lower_limit : float, standard: -math.inf
        Der Nutzer soll keinen kleineren Wert als diesen angeben können
    upper_limit : float, standard: math.inf
        Der Nutzer soll keinen größeren Wert als diesen angeben können
    data_type : type (<class 'float'> oder <class 'int'>)
        Eingabe des Nutzers soll als dieser Datentyp eingelesen werden können
    
    Returns
    -------
    nutzereingabe : data_type
        Eingegebene Zahl wird im Datentyp data_type zurückgegeben
    """
    wert = True
    while wert:
        try:
            # Nutzereingabe abfragen
            x = input(question)
            # Programmabbruch bei einer leeren Eingabe
            if x == "":
                raise ValueError("Leere Eingabe. Das Programm wurde abgebrochen.")
            nutzereingabe = data_type(x)
            # Überprüfen, ob die Eingabe im gültigen Bereich liegt
            if nutzereingabe > upper_limit:
                print("Ungültige Eingabe. Bitte geben Sie eine Zahl kleinergleich "
                      f"{upper_limit} ein. Zum Abbrechen Eingabe leer lassen.")
            elif nutzereingabe < lower_limit:
                print("Ungültige Eingabe. Bitte geben Sie eine Zahl größergleich"
                      f" {lower_limit} ein. Zum Abbrechen Eingabe leer lassen.")
            else:
                wert = False
                return nutzereingabe
        except ValueError as e:
            if str(e) == "Leere Eingabe. Das Programm wurde abgebrochen.":
                raise
            print("Ungültige Eingabe. Bitte geben Sie eine Zahl mit" +
                      f" dem Datentyp {data_type} ein. Zum Abbrechen Eingabe leer lassen.")
    return None

def referenzlinie(untersuchungsfunktion, algorithmus, referenz,  m, x):
    """
    Berechnet die Referenzlinie durch Skalierung eines Referenzwertes.

    Parameters
    ----------
    untersuchungsfunktion : function
        Funktion, die abhängig von `algorithmus` und `m` einen Wert berechnet
    algorithmus: function
        Algorithmus, der untersucht wird
    referenz : function
        berechnet Referenzwert in Abhängigkeit von `m`
    m : int
        Parameter, anhand welchem der Referenzwert gebildet wird
    x : array
        x-Werte, der Messungen

    Returns
    ---------
    numpy.ndarray: 
        y-Werte der Referenzlinie
    """
    wert = untersuchungsfunktion(algorithmus, m)
    # Berechnung des Skalierungsfaktors
    scaling =  wert/ referenz(m)
    return referenz(x) * scaling

def plot_vergleich(x,
                   y,
                   labels,
                   title,
                   ylabel,
                   y_scaling = None,
                   labels_scaling = None,
                   xlabel="Obergrenze n",
                   filename=None):
    """
    Erzeugt einen Log-Log-Plot für den Vergleich von Daten mit optionalen Skalierungslinien.

    Parameters
    ----------
    x : numpy.ndarray
        Die zu plottenden Daten x-Werte
    y : list of lists
        Liste von y-Werten für die darzustellenden Funktionen
    labels : list of str
        Liste von Labels
    title : str 
        Titel des Plots
    ylabel : str 
        Bezeichnung der y-Achse
    y_scaling : list of lists, optional
        Liste von y-Werten für die Referenzlinien
    labels_scaling : list of str, optional
        Liste von Labels für die Referenzlinien
    xlabel : str 
        Bezeichnung der x-Achse
    filename : str, optional
        Dateiname zum Speichern des Plots

    Returns
    ---------
    None
    """
    # Standardfarben und -stile
    colors = ['#d62728', '#2ca02c', '#1f77b4']
    linestyles = [':', '--', '-.']
    markers = ['', '', '']

    plt.figure(figsize=(10, 6))
    # Skalierungslinien plotten
    if y_scaling is not None and labels_scaling is not None:
        for ys, label, color, linestyle in zip(y_scaling, labels_scaling, colors, linestyles):
            plt.loglog(x, ys, color=color, alpha=0.6, marker="", ls=linestyle, label=label)
    # Tatsächliche Daten plotten
    for ya, label, color, marker in zip(y, labels, colors, markers):
        plt.loglog(x, ya, color=color, marker=marker, label=label)

    plt.xlabel(xlabel, fontsize=15)
    plt.ylabel(ylabel, fontsize=15)
    plt.title(title, fontsize=16, pad=20)
    plt.legend(fontsize=12)
    plt.grid(True, ls="-")
    # Plot speichern, falls ein Dateiname angegeben ist
    if filename:
        speichern = read_number(f"Wollen Sie den Plot unter dem Namen {filename} speichern?\n"
                                "Es sollte keine Datei mit dem gleichen Dateiname im Ordner "+
                                "des Programms vorliegen"+", da diese sonst überschrieben wird."
                                "\n(1 für ja, 2 für nein): ", 1, 2, int)
        if speichern ==1:
            plt.savefig(filename, dpi=500)
            print(f"Plot gespeichert als {filename}.")
    plt.show()

def reference_n(x):
    """
    Berechnet Werte für die Komplexität O(n).

    Parameters
    ----------
    x : array
        Eingabewerte

    Returns
    -------
    array
        Referenzwerte
    """
    return x

def reference_n_log(x):
    """
    Berechnet Werte für die Komplexität O(n log(log(n))).

    Parameters
    ----------
    x : array
        Eingabewerte

    Returns
    -------
    array
        Referenzwerte
    """
    return x * np.log(np.log(x))

def reference_n_wurzel(x):
    """
    Berechnet Werte für die Komplexität O(n sqrt(n)).

    Parameters
    ----------
    x : array
        Eingabewerte

    Returns
    -------
    array
        Referenzwerte
    """
    return x * np.sqrt(x)

def reference_n_logn(x):
    """
    Berechnet Werte für die Komplexität O(frac{n}{log(n)}).

    Parameters
    ----------
    x : array
        Eingabewerte

    Returns
    -------
    array
        Referenzwerte
    """
    return x/ np.log(x)

def main():
    """ Hauptprogramm: Funktionalität und Verwendung der oben implementierten Funktionen, 
        Aufruf von 'measure_time()', 'measure_memory_usage()', read_number(),
        referenzlinie(), plot_vergleich()
        und als Beispielalgorithmen:
        'naiv_prim_sieb()', 'sieb_erastosthenes()', 'sieb_von_atkin()'
    """
    # Informationen an den Nutzer
    print("Dieses Modul beinhaltet Hilfsfunktionen zur Untersuchung von "
          "Algorithmen \nhinsichtlich Speicherbedarf und Laufzeitverhalten.\n"+
          "Dabei vergleichen wir hier 3 Algorithmen, welche alle "+
          "\nPrimzahlen bis zu einer Obergrenze bestimmen.\n"+
          "Die read_numbers Funktion überprüft, ob die Nutzereingabe"+
          " im gewählten Intervall liegt.\n")
    # read_number für die Nutzereingabe
    try:
        # limit für die read_number funktion kann selber eingestellt werden
        n =read_number("Wählen Sie eine Obergrenze (größer gleich 0): ", 0, 10**6, int)
    except ValueError as e:
        if str(e) == "Leere Eingabe. Das Programm wurde abgebrochen.":
            print(e)
            sys.exit()  # Beendet das Programm ohne Fehlermeldung
    # Wenn die Liste der erzeugten Primzahlen max 30 Elemente hat, wird sie ausgegeben
    # die 31. Primzahl ist 127
    if n<127:
        print(f"Primzahlen kleiner gleich {n}:", sieb_eratosthenes(n))

    print(f"\nNaiver Algorithmus: \nLaufzeit (ms): {measure_time(naiv_prim, n)} \n"
          + f"Speicherverbrauch (MiB): {measure_memory_usage(naiv_prim, n)}")
    print(f"\nSieb von Eratosthenes: \nLaufzeit (ms): {measure_time(sieb_eratosthenes, n)} \n"
          + f"Speicherverbrauch (MiB): {measure_memory_usage(sieb_eratosthenes, n)}")
    print(f"\nSieb von Atkin: \nLaufzeit (ms): {measure_time(sieb_von_atkin, n)} \n"
          + f"Speicherverbrauch (MiB): {measure_memory_usage(sieb_von_atkin, n)}")

    print("\nMit den Funktionen referenzlinie() und plot_vergleich() lässt sich ein\n"
          +"doppelt logarithmisch skalierter Plot zum Vergleich von Daten mit\n"
          +"Referenzlinien erstellen.\n")

    print("Wir plotten nun als Beispiel das Laufzeitverhalten der obigen Algorithmen.")

    # x-Achse
    x = np.geomspace(2, n ,100,endpoint=True, dtype=np.int64)

    m = 10000
    naive_times = [measure_time(naiv_prim, n) for n in x]
    sieve_times = [measure_time(sieb_eratosthenes, n) for n in x]
    atkin_times = [measure_time(sieb_von_atkin, n) for n in x]

    # Referenzlinien
    scaling_atkin = referenzlinie(measure_time, sieb_von_atkin, reference_n, m, x)
    scaling_era = referenzlinie(measure_time, sieb_eratosthenes, reference_n_log, m, x)
    scaling_naive =  referenzlinie(measure_time, naiv_prim, reference_n_wurzel, m, x)

    labels_scaling_times = [
            "Eratosthenes $O(n(log(log(n)))$",
            "Atkin $O(n)$",
            "Naives $O(n\\sqrt{n})$"
        ]

    labels_actual_times = [
            "Sieb von Eratosthenes",
            "Sieb von Atkin",
            "Naiver Algorithmus"
        ]
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

if __name__ == '__main__':
    main()
