import ContinuoReaccionQuimica as crq
import ContinuoReactorNuclear as crn
import DiscretaPeluqueria as dp
import DiscretaRestaurante as dr
import DiscretaRestaurante2 as dr2
import DiscretaSistemaRedes as dsr

while True:
    print('''
        Simuladores de Ejemplos
        =======================''')

    try:
        option = int(input(('''
            1. ContinuoReaccionQuimica
            2. ContinuoReaccionNuclear
            3. DiscretaPeluqueria
            4. DiscretaRestaurante
            5. DiscretaRestaurante2
            6. DiscretaSistemaRedes
                            
            > ''')))
        
        match option:
            case 1:
                print('''
                ContinuoReaccionQuimica
                =======================
                ''')
                crq.ReaccionQuimica().run()
                input('(Presione ENTER para continuar) ')
            case 2:
                print('''
                ContinuoReaccionNuclear
                =======================
                ''')
                crn.ReactorNuclear().run()
                input('(Presione ENTER para continuar) ')
            case 3:
                print('''
                DiscretaPeluqueria
                ==================
                ''')
                dp.Peluqueria().run()
                input('(Presione ENTER para continuar) ')
            case 4:
                print('''
                DiscretaRestaurante
                ==================
                ''')
                dr.Restaurante().run()
                input('(Presione ENTER para continuar) ')
            case 5:
                print('''
                DiscretaRestaurante2
                ==================
                ''')
                dr2.Restauerante().run()
                input('(Presione ENTER para continuar) ')
            case 6:
                print('''
                DiscretaSistemaRedes
                ==================
                ''')
                dsr.SistemaRedes().run()
                input('(Presione ENTER para continuar) ')
                
            case default:
                input('Opcion no valida(Presione ENTER para continuar) ')
                continue
    except ValueError as err:
        input('Opcion no valida (Presione ENTER para continuar) ')
        continue
