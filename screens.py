import curses
import service

def mainScreen(stdscr):
    #Pantalla de bienvenida
    stdscr.clear()
    curses.curs_set(0)
    welcomeMsg = "Bienvenido. Presiona cualquier tecla para ingresar."
    height, width = stdscr.getmaxyx()
    stdscr.addstr(height // 2, (width - len(welcomeMsg)) // 2, welcomeMsg)
    stdscr.refresh()
    #Bloqueamos el programa hasta que se presione la tecla
    stdscr.getch()
    #Entramos al menu inicial
    menuScreen(stdscr)

def menuScreen(stdscr):
    #Pantalla del menú principal.
    stdscr.clear()
    curses.curs_set(0)
    mainOpt = [
        "Agregar una nueva cédula.",
        "Ver todas las cédulas.",
        "Buscar una cédula.",
        "Actualizar una cédula.",
        "Eliminar una cédula.",
        "Reportes",
        "Salir"
    ]
    currentOpt = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        titulo = "Seleccione una opción:"
        stdscr.addstr(1, (width - len(titulo)) // 2, titulo, curses.A_BOLD)

        for i, opcion in enumerate(mainOpt):
            indicador = "<-" if i == currentOpt else "  "
            opcionText = f"{indicador} {opcion}"
            x = (width - len(opcionText)) // 2
            y = 3 + i
            stdscr.addstr(y, x, opcionText)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and currentOpt > 0:
            currentOpt -= 1
        elif key == curses.KEY_DOWN and currentOpt < len(mainOpt) - 1:
            currentOpt += 1
        elif key in [curses.KEY_ENTER, ord('\n'), ord('\r')]:
            #Salir opt
            if currentOpt == len(mainOpt) - 1:
                stdscr.clear()
                mensaje = "Gracias por usar el sistema. ¡Hasta luego!"
                stdscr.addstr(stdscr.getmaxyx()[0] // 2, (stdscr.getmaxyx()[1] - len(mensaje)) // 2, mensaje)
                stdscr.refresh()
                stdscr.getch()
                break
            #Agregar una cedula
            elif currentOpt == 0:
                stdscr.clear()
                cedula = service.get_input(stdscr, "Ingrese una nueva cedula: ")
                service.addCedula(cedula, stdscr)
            #Ver todas las cedulas
            elif currentOpt == 1:
                service.showCedulas(stdscr, height, width)
            #Buscar una cedula
            elif currentOpt == 2:
                cedula = service.search_with_suggestions(stdscr, "Ingrese la cedula a buscar: ")
                if cedula in service.cedulas:
                    mensaje = f"La cédula {cedula} fue encontrada."
                else:
                    mensaje = f"La cédula {cedula} no se encuentra en la lista."
                stdscr.clear()
                stdscr.addstr(stdscr.getmaxyx()[0] // 2, (stdscr.getmaxyx()[1] - len(mensaje)) // 2, mensaje)
                stdscr.refresh()
                stdscr.getch()
            #Actualizar una cedula
            elif currentOpt == 3:
                service.updateCedula(stdscr)
            #Eliminar una cedula
            elif currentOpt == 4:
                service.deleteCedula(stdscr)
            #Reportes
            elif currentOpt == 5:
                service.reportes(stdscr)

if __name__ == "__main__":
    curses.wrapper(mainScreen)