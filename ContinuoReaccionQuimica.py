import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class ReaccionQuimica:
    # Parámetros del sistema
    k = 0.1  # Constante de velocidad de la reacción (1/min)
    A0 = 1.0  # Concentración inicial de A (mol/L)

    # Tiempo de simulación (0 a 50 minutos, con 1000 puntos)
    tiempo = np.linspace(0, 50, 1000)  # Tiempo en minutos

    # Ecuación diferencial para la concentración de A
    def modelo(self, A, t):
        dA_dt = -self.k * A
        return dA_dt

    def run (self):
        self.k = float(input("Ingrese Constante de velocidad de reaccion (1/min): "))
        self.A0 = float(input("Ingrese Concentracion inicial de A (mol/L): ")) 
        
        # Resolver la ecuación diferencial        
        self.solucion = odeint(self.modelo, self.A0, self.tiempo)
        
        # Graficar los resultados
        plt.figure(figsize=(10, 5))
        plt.plot(self.tiempo, self.solucion, label='Concentración de [A]')
        plt.xlabel('Tiempo (minutos)')
        plt.ylabel('Concentración (mol/L)')
        plt.title('Descomposición de un Reactivo de Primer Orden')
        plt.grid(True)
        plt.legend()
        plt.show()
