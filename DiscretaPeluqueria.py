#programa una simulacion de linea de espera
#una peluqueria tiene un peluquero que se demora entre 15 y 30 minutos por corte. La peluqueria recibe en promedio 3 clientes por hora (es decir, uno cada 20 minutos). Se desea simular las llegadas y servicios de los 5 clientes

import random
from re import escape
import simpy
import math

class Peluqueria:
  semilla = 30
  num_peluqueros = 1
  tiempo_corte_min = 15
  tiempo_corte_max= 30
  t_llegadas = 20
  tot_clientes=5
  
  te=0.0 #tiempo de espera total
  dt=0.0#duracion del servicio
  fin=0.0#minuto en que finaliza
  
  #procedimientos
  def cortar(self, cliente):
    R = random.random()
    tiempo = self.tiempo_corte_max - self.tiempo_corte_min
    tiempo_corte = self.tiempo_corte_min + (tiempo*R) #dist Uniforme
    yield env.timeout(tiempo_corte) #dejar correr el tiempo n minutos
    print("Corte listo a %s en %.2f minutos" % (cliente, tiempo_corte))
    self.dt = self.dt + tiempo_corte #acumular tiempo de uso de la instalacion

  def cliente(self, env, name, personal):
    llega = env.now # guarda el minuto de llegada del cliente 
    print("--> %s llegó a la peluqueria en el minuto %.2f" % (name, llega))
    with personal.request() as request: # espera turno
        yield request # obtener turno
        pasa = env.now
        espera = pasa - llega # acumulo tiempo de espera
        self.te = self.te + espera # acumulo tiempo de espera
        print("%s Pasa y espera en la peluqueria en el minuto %.2f habiendo esperado %.2f" % (name, pasa, espera))
        yield env.process(self.cortar(name)) # llamar al proceso cortar
        deja = env.now # momento en que el cliente deja la peluquería
        print("<--%s deja la peluqueria en minuto %.2f" % (name, deja))
        self.fin = deja # guardo el minuto en que termina


  def principal(self, env, personal):
    llegada = 0
    i = 0
    for i in range(self.tot_clientes):
      R = random.random()
      llegada = -self.t_llegadas* math.log(R)
      yield env.timeout(llegada) #dejo transcurrir un tiempo entre un cliente y otro
      i=i+1
      env.process(self.cliente(env, 'cliente %d' % i, personal))
      
  def run(self):
    #programa principal
    print("---Simulacion Peluqueria---")
    self.semilla = int(input("Ingrese la semilla: "))
    self.num_peluqueros = int(input("Ingrese el numero de peluqueros: "))
    self.tiempo_corte_min = int(input("Ingrese el tiempo de corte minimo: "))
    self.tiempo_corte_max= int(input("Ingrese el tiempo de corte maximo: "))
    self.t_llegadas =  int(input("Ingrese el tiempo de llegada: "))
    self.tot_clientes= int(input("Ingrese el total de clientes: "))
    
    random.seed(self.semilla)
    
    global env, personal

    env = simpy.Environment() #creo el entorno de simulacion
    personal = simpy.Resource(env, self.num_peluqueros) #crea los recursos peluqueros
    env.process(self.principal(env, personal))
    env.run()

    #salidas
    print("Indicadores optenidos")
    print("")
    lpc = self.te/self.fin
    print("Longitud promedio de la cola: %.2f" % lpc)
    tep = self.te/self.tot_clientes
    print("Tiempo de espera promedio: %.2f" % tep)
    upi = (self.dt/self.fin)/self.num_peluqueros
    print("Uso promedio de la instalacion: %.2f" % upi)
