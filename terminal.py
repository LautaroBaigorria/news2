#!/usr/bin/python

import news2
import argparse

class Terminal(object):
    """para ejecutar desde la terminal"""
    def __init__(self):
        self.news=news2.News()
        
    def execute(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", type=str, help="link para agregar a lista de feeds")
        args = parser.parse_args()
        if args.i:
            self.news.agregarfeedcmdline(args.i)
        self.mostrar_menu()  
    
    def mostrar_menu(self):
        menu = [{'opcion':'Ver feeds','funcion': self.news.ver_feeds},{'opcion':'Agregar feed','funcion': self.news.agregarfeed},{'opcion':'Borrar feed','funcion': self.news.borrarfeed},{'opcion':'Noticias recientes','funcion': self.news.showRecentHeadlines},{'opcion':'Salir','funcion': quit}]
        self.printMenu(menu)
        entradaUsuario=int(input("Seleccione una opcion: "))
        if ((entradaUsuario-1) in range(-1,len(menu))):
            menu[entradaUsuario-1]['funcion']();self.mostrar_menu()
        else:
            print('Opcion no valida!')
            self.mostrar_menu()

    def printMenu(self, menu):
        for element in menu:
            print(f"{menu.index(element)+1} - {element['opcion']}")

if __name__ == "__main__":
   terminal = Terminal()
   terminal.execute()