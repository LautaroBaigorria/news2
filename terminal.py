#!/usr/bin/python

import news2
import argparse

class Terminal(object):
    """docstring for Terminal"""
    def __init__(self):
        self.news=news2.News()
        # print("Funcion init")
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", type=str, help="link para agregar a lista de feeds")
        args = parser.parse_args()
        if args.i:
            entrada=str(args)
            entrada=entrada[13:-2]
            self.news.agregarfeedcmdline(entrada)
        self.mostrar_menu()
        
    def mostrar_menu(self):
        menu2 = ['Ver feeds', 'Agregar feed','Borrar feed' ,'Salir', 'Convertir a archivo yaml']
        self.print_list(menu2)
        entrada_usuario=int(input("Seleccione una opcion: "))
        if (entrada_usuario==1):
            self.news.ver_feeds()
            self.mostrar_menu()
        elif (entrada_usuario==2):
            self.news.agregarfeed()
            self.mostrar_menu()
        elif (entrada_usuario==3):
            self.news.borrarfeed()
            self.mostrar_menu()
        elif (entrada_usuario==4):
            quit()
        elif (entrada_usuario==5):
            print  ("5")
        else:
            print("Opcion no valida")

    def print_list(self, array):
        if type(array)==list:
            for x in array:
                print (str(array.index(x)+1) +' - ' + x)

terminal=Terminal()
