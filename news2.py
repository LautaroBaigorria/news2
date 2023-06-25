#!/usr/bin/python
import feedparser
# import soupsieve
import yaml 
from bs4 import BeautifulSoup
import os.path
import findfeed
import findfeed2


class News(object):
    """docstring for News"""
    def __init__(self):
        pass
    def ver_feeds(self):
        #  listaPorDefecto = ['http://rss.slashdot.org/Slashdot/slashdot','http://www.digg.com/rss/index.xml','https://www.tecmint.com/feed/','https://www.reddit.com/r/Python/.rss']
        lista=self.loadyaml()
        self.niltotitle(lista)
        self.printFeedList(lista)      
        selectedFeed=input('Seleccione la Fuente deseada o presione \'M\' para volver al menu principal ')
        if selectedFeed.lower()=='m':
            pass
            #self.mostrar_menu()
        else:
            siteFeed=feedparser.parse(lista[int(selectedFeed)-1]["link"])
            self.printArticleList(siteFeed)
            articleIndex = input('Seleccione articulo: ')
            self.printArticle(siteFeed,articleIndex) #desde aqui para abajo 
            
    def agregarfeed(self):
        nuevo_feed=input('Escriba link de nuevo feed: ')
        self.addFeed(nuevo_feed)

    def borrarfeed(self):
        lista=self.loadyaml()
        self.printFeedList(lista)
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
        self.addFeed(nuevo_feed)

    def printFeedList(self, array):
        '''imprime lista de sitios en ver_feeds'''
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
    
    def mostrarNoticiasrecientes(self): 
        '''no funciona arreglar'''
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
        try:
            posibleFeed = feedparser.parse(url)
        except:
            print("e")
        if not (posibleFeed.entries):
            print ("posibleFeed.entries esta vacio")
            return False
        else: 
            return True

    def checkIfUrlHasHttp(self,url):
        if not "http://" in url or "https://" in url:
            print("no contiene http")
            url = "http://{0}".format(url)
            return url
        else: 
            return url
        
    def checkIfUrlHasSlash(self,url):
        if url[-1] != "/":
            url = "{0}/".format(url)
        return url

    
    def wrapperCheck(self,url):
        feed_url = url + "feed"
        try:
            feed = feedparser.parse(feed_url)
            if feed.entries:
                return feed_url
        except Exception:
            pass

        feed_url = url + "rss"
        try:
            feed = feedparser.parse(feed_url)
            if feed.entries:
                return feed_url
        except Exception:
            pass

        feed_url = url + "feeds/posts/default"
        try:
            feed = feedparser.parse(feed_url)
            if feed.entries:
                return feed_url
        except Exception:
            pass    

        feed_url = url[:19] + 'feed/' + url[19:]
        try:
            feed = feedparser.parse(feed_url)
            if feed.entries:
                return feed_url
        except Exception:
            pass  

        feed_url = url + "blog/feed"
        try:
            feed = feedparser.parse(feed_url)
            if feed.entries:
                return feed_url
        except Exception:
            pass

        feed_url = url + "blog/rss"
        try:
            feed = feedparser.parse(feed_url)
            if feed.entries:
                return feed_url
        except Exception:
            pass

        feed_url = url + ".xml"
        try:
            feed = feedparser.parse(feed_url)
            if feed.entries:
                return feed_url
        except Exception:
            pass

        feed_url = url + "rss.xml"
        try:
            feed = feedparser.parse(feed_url)
            if feed.entries:
                return feed_url
        except Exception:
            pass

        feed_url = url + "blog/rss.xml"
        try:
            feed = feedparser.parse(feed_url)
            if feed.entries:
                return feed_url
        except Exception:
            pass

        try:
            print ("probando metodos externos")
            url = self.checkForFeedInSourceCode(url)
            return url
        except Exception:
            pass

        return False


    def addFeed(self,nuevo_feed):
        # nuevo_feed = self.checkIfUrlHasHttp(nuevo_feed)
        nuevo_feed = self.checkIfUrlHasSlash(nuevo_feed)
        if (self.checkIfUrlHasEntries(nuevo_feed)):
            self.addFeed2(nuevo_feed)
        else:
            print ("se ejecuta wrapperCheck")
            nuevo_feed=self.wrapperCheck(nuevo_feed)
            try:
                if (self.checkIfUrlHasEntries(nuevo_feed)):
                    self.addFeed2(nuevo_feed)
                else:
                    print ("no se encontro feed valido")    
            except Exception:
                pass

    def addFeed2(self,nuevo_feed):
        lsita=self.loadyaml()
        el={"titulo":"","link":nuevo_feed}
        el = self.fetch_title(el)
        if self.checkIfAlreadyOnFeedList(nuevo_feed,lsita):
            print("La Url {0} ya existe en la lista".format(nuevo_feed))
        elif self.checkIfTitleExists(el["titulo"], lsita):
            print("Hay un feed con titulo {0} en la lista".format(el["titulo"]))
        else:
            lsita.append(el)
            self.feed2yaml(lsita)
        
    def checkIfAlreadyOnFeedList(self,link,feedlist):
        if any(
            element.get('link') == link
            for element in feedlist 
        ):
            return True
        if not any(
            element.get('link') == link
            for element in feedlist 
        ):
            return False
        
    def checkIfTitleExists(self,title,feedlist):
        if any(
            element.get('titulo') == title
            for element in feedlist 
        ):
            return True
        if not any(
            element.get('titulo') == title
            for element in feedlist 
        ):
            return False

        
    def printArticleList(self,siteFeed):
        '''imprime lista de articulos en ver_feeds'''
        i=0
        while i <len(siteFeed.entries):
            print (str(i+1)+ ' - '  + siteFeed.entries[i].title)
            i+=1

    def printArticle(self,siteFeed,articleIndex):
        '''imprime articulo seleccionado'''
        article = siteFeed.entries[int(articleIndex)-1].title + '\n' + siteFeed.entries[int(articleIndex)-1].link + '\n' + siteFeed.entries[int(articleIndex)-1].description
        esHtml = bool(BeautifulSoup(article, "html.parser").find())
        if (esHtml):
            print ("HTML Detectado.")
            print (self.htmlTotext(article))
        else:
            print(article)

    def checkForFeedInSourceCode(self,url):
        '''metodos adicionales para busqueda de feeds validos en codigo fuente de pagina'''
        urlList = findfeed.findfeed(url)
        if urlList:
            print (urlList[0])
            return urlList[0]
        else:
            urlList = findfeed2.find_rss_links(url)
            if urlList:
                print (urlList[0])
                return urlList[0]
            else: 
                print("No se encontraron feeds")

    