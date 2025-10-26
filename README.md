# Prime Number Analysis 🔢

This project was created as part of the *Project Practicum I* (2024).  
It investigates algorithms for generating and analyzing prime numbers efficiently.

---

## 📘 Contents
- **Report:** `Bericht_Primzahlen.pdf`  
- **Code:**
  - `prime_check.py` – implements basic primality testing  
  - `sieve_eratosthenes.py` – computes all primes ≤ n using the Sieve of Eratosthenes  
  - `prime_analysis.py` – compares runtime and performance of different algorithms  

---

## ⚙️ Methods
- Naive prime number testing  
- Sieve of Eratosthenes  
- Asymptotic runtime comparison \( O(n \log \log n) \) vs. \( O(n^2) \)  
- Visualization of prime distribution  

---

## 📊 Results
The numerical experiments confirm:
- The Sieve of Eratosthenes is significantly faster for large \( n \).  
- The distribution of primes roughly follows the Prime Number Theorem \( \pi(n) \sim \frac{n}{\log n} \).  
- Naive methods become inefficient beyond \( n \approx 10^5 \).  

---

## 🧠 Requirements
Python ≥ 3.9  
Packages: `numpy`, `matplotlib`, `time`
