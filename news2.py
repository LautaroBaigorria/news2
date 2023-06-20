#!/usr/bin/python
import feedparser
# import soupsieve
import yaml 
from bs4 import BeautifulSoup
import os.path


class News(object):
    """docstring for News"""
    def __init__(self):
        pass
    def ver_feeds(self):
        #  listaPorDefecto = ['http://rss.slashdot.org/Slashdot/slashdot','http://www.digg.com/rss/index.xml','https://www.tecmint.com/feed/','https://www.reddit.com/r/Python/.rss']
         lista=self.loadyaml()
         self.niltotitle(lista)
         self.print_dictlist(lista)      
         select_feed=input('Seleccione la Fuente deseada o presione \'M\' para volver al menu principal ')
         if select_feed.lower()=='m':
            pass
            #self.mostrar_menu()
         else:
            # self.print_feedlist(lista)
            d=feedparser.parse(lista[int(select_feed)-1]["link"])
            i=0
            while i <len(d.entries):
                print (str(i+1)+ ' - '  + d.entries[i].title)
                i+=1
            select_item=input('Seleccione articulo: ')
            article = d.entries[int(select_item)-1].title
            article += '\n'
            article += d.entries[int(select_item)-1].link
            article += '\n'
            article += d.entries[int(select_item)-1].description
            esHtml = bool(BeautifulSoup(article, "html.parser").find())

            if (esHtml):
                print ("HTML Detectado.")
                print (self.htmlTotext(article))
            else:
                print(article)

    def agregarfeed(self):
        nuevo_feed=input('Escriba link de nuevo feed: ')
        # nuevo_feed=self.checkIfUrlHasHttp(nuevo_feed)
        nuevo_feed=self.checkIfUrlHasSlash(nuevo_feed)
        if (self.checkIfUrlHasEntries(nuevo_feed)):
            lsita=self.loadyaml()
            el={"titulo":"","link":nuevo_feed}
            lsita.append(el)
            self.feed2yaml(lsita)
            #self.mostrar_menu()
        else:
            print ("se ejecuta wrapperCheck")
            nuevo_feed=self.wrapperCheck(nuevo_feed)
            if (self.checkIfUrlHasEntries(nuevo_feed)):
                lsita=self.loadyaml()
                el={"titulo":"","link":nuevo_feed}
                lsita.append(el)
                self.feed2yaml(lsita)
            else:
                print ("no se encontro feed valido")    

    def borrarfeed(self):
        lista=self.loadyaml()
        self.print_dictlist(lista)
        feed_a_borrar=input('Seleccione feed a borrar: ')
        del lista[int(feed_a_borrar)-1]
        self.feed2yaml(lista)
        #self.mostrar_menu()
        
    def feed2yaml(self,lsita):
        with open(".newsrc",'w') as my_file:
            yaml.dump(lsita,my_file)

    def loadyaml(self):
        lsita=[]
        if os.path.isfile(".newsrc"):
            with open(".newsrc",'r') as my_file:
                lsita=yaml.load(my_file, Loader=yaml.FullLoader)
        else: 
            lsita = [{"titulo":"","link":'http://rss.slashdot.org/Slashdot/slashdot'},{"titulo":"","link":'http://www.digg.com/rss/index.xml'}] 
        return lsita
        
    def agregarfeedcmdline(self,nuevo_feed):
        # nuevo_feed=self.checkIfUrlHasHttp(nuevo_feed)
        nuevo_feed=self.checkIfUrlHasSlash(nuevo_feed)
        if (self.checkIfUrlHasEntries(nuevo_feed)):
            lsita=self.loadyaml()
            el={"titulo":"","link":nuevo_feed}
            lsita.append(el)
            self.feed2yaml(lsita)
            # self.mostrar_menu()
        else:
            print ("se ejecuta wrapperCheck")
            nuevo_feed=self.wrapperCheck(nuevo_feed)
            if (self.checkIfUrlHasEntries(nuevo_feed)):
                lsita=self.loadyaml()
                el={"titulo":"","link":nuevo_feed}
                lsita.append(el)
                self.feed2yaml(lsita)
            else:
                print ("no se encontro feed valido") 

    def print_dictlist(self, array):
        if type(array)==list:
            for x in array:
                # print (str(array.index(x)+1) +' - ' + x)
                if x["titulo"]=='':
                    print (str(array.index(x)+1) + ' - ' + x["link"])
                else:
                    print (str(array.index(x)+1) + ' - ' + x["titulo"])
    def dicttoyaml(self):
        lsita=[]
        lista=[]
        lista=self.loadyaml()
        for i in lista:
            el={"titulo":"","link":i} 
            lsita.append(el)
        with open(".newsrc2",'w') as my_file:
            yaml.dump(lsita,my_file)

    def niltotitle(self,array):
                for x in array:
                    if x["titulo"]=='':
                        self.fetch_title(x)
                        self.feed2yaml(array)        

    def fetch_title(self,dict1):
        if dict1["titulo"]=='':
            d=feedparser.parse(dict1["link"])
            dict1["titulo"]=d.feed.title
        return dict1

    def parselink(self,link):
        d=feedparser.parse(link)
        return d
    
    def htmlTotext(self,html):
        soup = BeautifulSoup(html,features="lxml")
        text = soup.get_text()
        return text
    
    '''no funciona'''
    def mostrarNoticiasrecientes(self): 
        lista = self.loadyaml()
        table_titles = []
        table_article_titles = []
        table_data = [table_titles,table_article_titles]
        for element in lista:
            table_titles.append(element["titulo"])
            feed = feedparser.parse(element["link"])
            table_article_titles.append(feed.entries[0].title)
            print(feed.entries[0].title)
        for row in table_data:
            print("{: ^20} {: ^20} {: ^20} {: ^20}".format(*row))    

    def checkIfUrlHasEntries(self,url):
        posibleFeed = feedparser.parse(url)
        if not (posibleFeed.entries):
            print ("posibleFeed.entries esta vacio")
            return False
        else: 
            return True

    def checkIfUrlHasHttp(self,url):
        if not "http://" or "https://" in url:
            print("no contiene http")
            url = "http://{0}".format(url)
            return url
        else: 
            return url
        
    def checkIfUrlHasSlash(self,url):
        if url[-1] != "/":
            url = "{0}/".format(url)
        return url

    def checkForWordpressFormat(self,url):
        url = "{0}feed".format(url)
        posibleFeed = feedparser.parse(url)
        if not posibleFeed.entries:
            print("posibleFeed.entries esta vacio / no es un sitio wordpress")
        else:
            print("se encontraron feeds en sitio tipo wordpress")
            print(url)
            return url

    def checkForTumblrFormat(self,url):
        url = "{0}rss".format(url)
        posibleFeed = feedparser.parse(url)
        if not posibleFeed.entries:
            print("posibleFeed.entries esta vacio / no es un sitio tumblr")
            return False
        else:
            print("se encontraron feeds en sitio tipo tumblr")
            print(url)
            return True
        
    def checkForBloggerFormat(self,url):
        url = "{0}feeds/posts/default".format(url)
        posibleFeed = feedparser.parse(url)
        if not posibleFeed.entries:
            print("posibleFeed.entries esta vacio / no es un sitio blogger")
            return False
        else:
            print("se encontraron feeds en sitio tipo blogger")
            print(url)
            return True

    def checkForMediumFormat(self,url):
        url = url[:19] + 'feed/' + url[19:]
        # https://medium.com/feed/example-site
        posibleFeed = feedparser.parse(url)
        if not posibleFeed.entries:
            print("posibleFeed.entries esta vacio / no es un sitio medium")
            return False
        else:
            print("se encontraron feeds en sitio tipo medium")
            print(url)
            return True
        
    def checkForFeedInSourceCode(self,url):
        pass

    def wrapperCheck(self,url):
        if (self.checkForWordpressFormat(url)):
            url = "{0}feed".format(url)
        if (self.checkForTumblrFormat(url)):
            url = "{0}rss".format(url)
        if (self.checkForBloggerFormat(url)):
            url = "{0}feeds/posts/default".format(url)
        if (self.checkForMediumFormat(url)):
            url = url[:19] + 'feed/' + url[19:]
        return url