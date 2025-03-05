import curses

# Colores
def init_colors():
    #Configuramos colores
    curses.start_color()

    #Color regular
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    #Color sugerencia Cyan
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

# Lista inicial
cedulas = ["1234", "5678", "9012"]

#Solo numeros
def is_valid_cedula(cedula):
    return cedula.isdigit()

#Agregar una cedula
def addCedula(cedula, stdscr):
    #Confirmamos si es valida
    if not is_valid_cedula(cedula):
        mensaje = "La cedula debe contener solo numeros. Presiona Enter para continuar."
    elif cedula in cedulas:
        mensaje = "La cedula ya existe. Presiona Enter para continuar."
    else:
        cedulas.append(cedula)
        mensaje = f"Cedula {cedula} agregada. Presiona Enter para continuar."

    stdscr.clear()
    stdscr.addstr(stdscr.getmaxyx()[0] // 2, (stdscr.getmaxyx()[1] - len(mensaje)) // 2, mensaje)
    stdscr.refresh()
    stdscr.getch()

def showCedulas(stdscr, height, width):
    """Muestra todas las cedulas en la pantalla."""
    titulo = "Lista de cedulas"
    stdscr.clear()
    stdscr.addstr(1, (width - len(titulo)) // 2, titulo, curses.A_BOLD)

    #No hay cedulas
    if not cedulas:
        mensaje = "No hay cedulas registradas."
        stdscr.addstr(height // 2, (width - len(mensaje)) // 2, mensaje)
    else:
        #Mostrar cedulas
        for i, cedula in enumerate(cedulas, start=1):
            stdscr.addstr(3 + i, (width - len(str(cedula))) // 2, f"{i}. {cedula}")

    stdscr.refresh()
    mensaje = "Presiona Enter para continuar."
    stdscr.addstr(height - 1, (width - len(mensaje)) // 2, mensaje)
    stdscr.getch()

def search_with_suggestions(stdscr, prompt):
    init_colors()
    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    stdscr.refresh()

    input_str = ""  # Variable para almacenar la entrada del usuario
    cursor_x = len(prompt)  # Posición inicial del cursor

    while True:
        key = stdscr.getch()

        if key == curses.KEY_ENTER or key in [10, 13]:  #10 y 13 = Enter
            break  #Salir del bucle y devolver el texto ingresado
        elif key == 9:  # 9 = Tab
            #Confirmar la sugerencia
            matches = [cedula for cedula in cedulas if cedula.startswith(input_str)]
            if matches:
                input_str = matches[0]
                cursor_x = len(prompt) + len(input_str)

                stdscr.clear()
                stdscr.addstr(0, 0, prompt + input_str, curses.color_pair(1))
                stdscr.move(0, cursor_x)
                stdscr.refresh()
            continue
        elif key in [curses.KEY_BACKSPACE, 127, 8]:  # 127 y 8 = Backspace
            if input_str:
                input_str = input_str[:-1]
                cursor_x -= 1
        elif 32 <= key <= 126: #Solo caracteres
            input_str += chr(key)
            cursor_x += 1

        suggestion = ""
        if input_str:
            matches = [cedula for cedula in cedulas if cedula.startswith(input_str)]
            if matches:
                suggestion = matches[0][len(input_str):]  # Parte restante de la primera coincidencia

        # Limpiar la línea actual y redibujar el texto
        stdscr.clear()
        stdscr.addstr(0, 0, prompt + input_str, curses.color_pair(1))  # Texto ingresado por el usuario (gris)
        if suggestion:
            stdscr.addstr(0, cursor_x, suggestion, curses.color_pair(2))  # Sugerencia en cian
        stdscr.move(0, cursor_x)  # Mover el cursor a la posición correcta
        stdscr.refresh()

    return input_str.strip()  # Eliminar espacios en blanco al inicio y final

def get_input(stdscr, prompt):
    """Captura la entrada del usuario en tiempo real sin sugerencias."""
    stdscr.clear()
    stdscr.addstr(0, 0, prompt)  # Mostrar el mensaje de solicitud
    stdscr.refresh()

    input_str = ""  # Variable para almacenar la entrada del usuario
    cursor_x = len(prompt)  # Posición inicial del cursor

    while True:
        key = stdscr.getch()

        if key == curses.KEY_ENTER or key in [10, 13]:  # Si se presiona Enter
            break
        elif key in [curses.KEY_BACKSPACE, 127, 8]:  # Si se presiona Retroceso
            if input_str:  # Solo borrar si hay algo que borrar
                input_str = input_str[:-1]
                cursor_x -= 1
        elif 32 <= key <= 126:  # Solo aceptar caracteres imprimibles
            input_str += chr(key)
            cursor_x += 1

        # Limpiar la línea actual y redibujar el texto
        stdscr.clear()
        stdscr.addstr(0, 0, prompt + input_str)
        stdscr.move(0, cursor_x)  # Mover el cursor a la posición correcta
        stdscr.refresh()

    return input_str.strip()  # Eliminar espacios en blanco al inicio y final

def updateCedula(stdscr):
    """Actualiza una cedula existente."""
    cedula_vieja = search_with_suggestions(stdscr, "Ingrese la cedula que desea actualizar: ")
    if cedula_vieja not in cedulas:
        mensaje = f"La cedula {cedula_vieja} no existe. Presiona Enter para continuar."
    else:
        cedula_nueva = search_with_suggestions(stdscr, "Ingrese la nueva cedula: ")
        if not is_valid_cedula(cedula_nueva):
            mensaje = "La nueva cedula debe contener solo números. Presiona Enter para continuar."
        elif cedula_nueva in cedulas:
            mensaje = "La nueva cedula ya existe. Presiona Enter para continuar."
        else:
            cedulas[cedulas.index(cedula_vieja)] = cedula_nueva
            mensaje = f"Cedula actualizada: {cedula_vieja} -> {cedula_nueva}. Presiona Enter para continuar."

    stdscr.clear()
    stdscr.addstr(stdscr.getmaxyx()[0] // 2, (stdscr.getmaxyx()[1] - len(mensaje)) // 2, mensaje)
    stdscr.refresh()
    stdscr.getch()

def deleteCedula(stdscr):
    """Elimina una cedula de la lista."""
    cedula = search_with_suggestions(stdscr, "Ingrese la cedula a eliminar: ")
    if cedula in cedulas:
        cedulas.remove(cedula)
        mensaje = f"La cedula {cedula} fue eliminada."
    else:
        mensaje = f"La cedula {cedula} no se encuentra en la lista."

    stdscr.clear()
    stdscr.addstr(stdscr.getmaxyx()[0] // 2, (stdscr.getmaxyx()[1] - len(mensaje)) // 2, mensaje)
    stdscr.refresh()
    stdscr.getch()

def reportes(stdscr):
    """Muestra el menú de reportes."""
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        titulo = "Menú de Reportes"
        stdscr.addstr(1, (width - len(titulo)) // 2, titulo, curses.A_BOLD)
        opciones = [
            "Total de cedulas registradas.",
            "Cedula con el mayor valor.",
            "Cedula con el menor valor.",
            "Listado ordenado de cedulas.",
            "Volver al menú principal."
        ]
        currentOpt = 0
        while True:
            stdscr.clear()
            stdscr.addstr(1, (width - len(titulo)) // 2, titulo, curses.A_BOLD)
            for i, opcion in enumerate(opciones):
                indicador = "<-" if i == currentOpt else "  "
                opcionText = f"{indicador} {opcion}"
                x = (width - len(opcionText)) // 2
                y = 3 + i
                stdscr.addstr(y, x, opcionText)
            stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_UP and currentOpt > 0:
                currentOpt -= 1
            elif key == curses.KEY_DOWN and currentOpt < len(opciones) - 1:
                currentOpt += 1
            elif key in [curses.KEY_ENTER, ord('\n'), ord('\r')]:
                if currentOpt == len(opciones) - 1:  # Volver al menú principal
                    return
                elif currentOpt == 0:  # Total de cedulas registradas
                    total_cedulas = len(cedulas)
                    mensaje = f"Hay {total_cedulas} cedulas registradas."
                elif currentOpt == 1:  # Cedula con el mayor valor
                    if cedulas:
                        max_cedula = max(cedulas, key=lambda x: int(x))
                        mensaje = f"Cedula con el mayor valor: {max_cedula}."
                    else:
                        mensaje = "No hay cedulas registradas."
                elif currentOpt == 2:  # Cedula con el menor valor
                    if cedulas:
                        min_cedula = min(cedulas, key=lambda x: int(x))
                        mensaje = f"Cedula con el menor valor: {min_cedula}."
                    else:
                        mensaje = "No hay cedulas registradas."
                elif currentOpt == 3:  # Listado ordenado de cedulas
                    if cedulas:
                        sorted_cedulas = sorted(cedulas, key=lambda x: int(x))
                        mensaje = "Listado ordenado de cedulas:\n" + "\n".join(sorted_cedulas)
                    else:
                        mensaje = "No hay cedulas registradas."

                    # Mostrar el listado centrado
                    stdscr.clear()
                    titulo_listado = "Listado Ordenado de Cedulas"
                    stdscr.addstr(1, (width - len(titulo_listado)) // 2, titulo_listado, curses.A_BOLD)

                    if cedulas:
                        # Calcular la posición inicial para centrar el listado
                        inicio_y = (height - len(sorted_cedulas)) // 2
                        for i, cedula in enumerate(sorted_cedulas):
                            x = (width - len(cedula)) // 2
                            stdscr.addstr(inicio_y + i, x, cedula)
                    else:
                        mensaje = "No hay cedulas registradas."
                        stdscr.addstr(height // 2, (width - len(mensaje)) // 2, mensaje)

                    stdscr.refresh()
                    stdscr.getch()
                    continue

                # Mostrar el mensaje del reporte
                stdscr.clear()
                stdscr.addstr(height // 2, (width - len(mensaje)) // 2, mensaje)
                stdscr.refresh()
                stdscr.getch()