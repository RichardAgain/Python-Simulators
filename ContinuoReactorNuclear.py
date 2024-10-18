


import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class ReactorNuclear:

    # Parámetros del sistema
    Q_gen = 5000  # Tasa de generación de calor en vatios (W)
    k = 0.1  # Coeficiente de enfriamiento en W/°C
    T_cool = 25  # Temperatura del sistema de enfriamiento en grados Celsius (°C)
    C = 10000  # Capacidad térmica del reactor (J/°C)

    # Tiempo de simulación (0 a 200 minutos, con 1000 puntos)
    tiempo = np.linspace(0, 200, 1000)  # Tiempo en minutos

    # Temperatura inicial del reactor
    T0 = 150  # °C

    # Ecuación diferencial para la variación de la temperatura
    def modelo(self, T, t):
        dT_dt = (self.Q_gen / self.C) - self.k * (T - self.T_cool)
        return dT_dt

    # Graficar los resultados
    def run (self):
        self.Q_gen = float(input("Ingrese Tasa de generación de calor en vatios (W): "))
        self.k = float(input("Ingrese Coeficiente de enfriamiento en W/°C: "))
        self.T_cool = float(input("Ingrese Temperatura del sistema de enfriamiento en grados Celsius (°C): "))
        self.C = float(input("Ingrese Capacidad térmica del reactor (J/°C): "))
        self.T0 = float(input("Ingrese Temperatura inicial del reactor: "))
        
        self.solucion = odeint(self.modelo, self.T0, self.tiempo)
        
        plt.figure(figsize=(10, 5))
        plt.plot(self.tiempo, self.solucion, label='Temperatura del Reactor')
        plt.xlabel('Tiempo (minutos)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Enfriamiento del Reactor Nuclear')
        plt.axhline(self.T_cool, color='red', linestyle='--', label='Temperatura del Sistema de Enfriamiento')
        plt.grid(True)
        plt.legend()
        plt.show()
