from datetime import datetime

def registrar_respuesta(usuario):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("respuesta.log", "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha}, USUARIO_BLOQUEADO, {usuario}\n")
    return fecha

intentos = {}

try:
    with open("eventos.log", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split(",")
            if len(partes) == 3:
                fecha = partes[0].strip()
                tipo = partes[1].strip()
                usuario = partes[2].strip()

                if tipo == "LOGIN_FALLIDO":
                    if usuario not in intentos:
                        intentos[usuario] = []
                    intentos[usuario].append(fecha)
except FileNotFoundError:
    print("Aún no existe el archivo eventos.log. Genera algunos eventos primero.")

for usuario, registros in intentos.items():
    if len(registros) >= 3:
        print("----------------------------------------")
        print("ALERTA DE SEGURIDAD")
        print("Usuario:", usuario)
        print("Intentos fallidos:", len(registros))
        print("Primer intento:", registros[0])
        print("Detección:", registros[2])

        # Registro de respuesta / bloqueo
        fecha_respuesta = registrar_respuesta(usuario)
        print("Acción aplicada: bloqueo de usuario")
        print("Respuesta:", fecha_respuesta)

        # Cálculo de Fechas
        inicio = datetime.strptime(registros[0], "%Y-%m-%d %H:%M:%S")
        deteccion = datetime.strptime(registros[2], "%Y-%m-%d %H:%M:%S")
        respuesta = datetime.strptime(fecha_respuesta, "%Y-%m-%d %H:%M:%S")

        # Métricas en segundos
        mttd = (deteccion - inicio).total_seconds()
        mttr = (respuesta - deteccion).total_seconds()

        print(f"MTTD: {mttd} segundos")
        print(f"MTTR: {mttr} segundos")
        print("----------------------------------------")