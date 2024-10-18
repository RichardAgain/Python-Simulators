import simpy
import random

class Restauerante:
    
    # Parámetros de la simulación
    SEMILLA = 42  # Semilla para reproducibilidad
    NUM_MESAS = 5  # Número de mesas disponibles en el restaurante
    TIEMPO_COMER_MIN = 20  # Tiempo mínimo que un cliente pasa comiendo (minutos)
    TIEMPO_COMER_MAX = 40  # Tiempo máximo que un cliente pasa comiendo (minutos)
    TIEMPO_LLEGADAS = 10  # Tiempo promedio entre la llegada de clientes (minutos)
    TOTAL_CLIENTES = 10  # Total de clientes a simular


    # Función para simular el proceso de un cliente
    def cliente(self, env, nombre, restaurante):
        """Simula el proceso de un cliente que llega, espera una mesa, come y luego se va."""
        print(f'{nombre} llega al restaurante en el minuto {env.now:.2f}')

        # El cliente solicita una mesa en el restaurante (espera si no hay mesas disponibles)
        with restaurante.request() as mesa:
            yield mesa  # Espera a que una mesa esté disponible
            print(f'{nombre} toma una mesa en el minuto {env.now:.2f}')

            # Simula el tiempo que el cliente pasa comiendo
            tiempo_comer = random.randint(self.TIEMPO_COMER_MIN, self.TIEMPO_COMER_MAX)
            yield env.timeout(tiempo_comer)
            print(
                f'{nombre} termina de comer y deja la mesa en el minuto {env.now:.2f}'
            )


    # Función para la llegada de clientes
    def llegada_clientes(self, env, restaurante):
        """Genera la llegada de clientes al restaurante."""
        for i in range(self.TOTAL_CLIENTES):
            # Cada cliente llega al restaurante
            yield env.timeout(
                random.expovariate(1.0 / self.TIEMPO_LLEGADAS)
            )  # Distribución exponencial para el tiempo entre llegadas
            env.process(self.cliente(env, f'Cliente {i+1}', restaurante))


    # Configuración y ejecución de la simulación
    def run (self):
        print('--- Simulación del Restaurante ---')
        self.SEMILLA = int(input("Ingrese Semilla para reproducibilidad: "))
        self.NUM_MESAS = int(input("Ingrese Número de mesas disponibles en el restaurante: "))
        self.TIEMPO_COMER_MIN = int(input("Ingrese Tiempo mínimo que un cliente pasa comiendo (minutos): "))
        self.TIEMPO_COMER_MAX = int(input("Ingrese Tiempo máximo que un cliente pasa comiendo (minutos): "))
        self.TIEMPO_LLEGADAS = int(input("Ingrese Tiempo promedio entre la llegada de clientes (minutos): "))
        self.TOTAL_CLIENTES = int(input("Ingrese Total de clientes a simular: "))
        
        random.seed(self.SEMILLA)  # Establece la semilla para reproducir resultados
        env = simpy.Environment()  # Crea el entorno de simulación
        restaurante = simpy.Resource(
            env, self.NUM_MESAS)  # Crea el recurso de mesas en el restaurante
        env.process(self.llegada_clientes(
            env, restaurante))  # Inicia el proceso de llegada de clientes
        env.run()  # Ejecuta la simulación
        print('--- Fin de la simulación ---')
