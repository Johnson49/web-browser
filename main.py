from PyQt5.QtCore import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtWebEngineWidgets import * 
from PyQt5.QtPrintSupport import * 
import sys 


class Window(QMainWindow): 
    def __init__(self, *args, **kwargs): 
        super(Window, self).__init__(*args, **kwargs) 

        self.abas = QTabWidget() 
        self.abas.setDocumentMode(True) 
        self.abas.tabBarDoubleClicked.connect(self.abrir_aba_com_duplo_click) 

        self.abas.currentChanged.connect(self.alternar_entre_as_guias) 
        self.abas.setTabsClosable(True) 
        self.abas.tabCloseRequested.connect(self.fechar_aba) 

        #-----------------------------------
        self.setMinimumSize(600,700)
        self.showMaximized()
        self.setWindowIcon(QIcon("./icones/web-search-engine.png"))
        #---------------------------

        self.setCentralWidget(self.abas) 
        #------------------------

        barra_de_navegacao = QToolBar() 
        barra_de_navegacao.setMovable(False)
        barra_de_navegacao.setIconSize(QSize(20,20))
        self.addToolBar(barra_de_navegacao) 

        #-----------------------------

        botao_de_voltar_pagina = QAction(QIcon('./icones/seta-esquerda.png'), "Voltar - Ctrl+w", self) 
        botao_de_voltar_pagina.setShortcut('Ctrl+w')
        botao_de_voltar_pagina.triggered.connect(lambda: self.abas.currentWidget().back()) 
        barra_de_navegacao.addAction(botao_de_voltar_pagina) 
        #-------------------------------------------------------

        botao_avancar_pagina = QAction(QIcon('./icones/seta-direita.png'),"Avançar - Ctrl+e", self) 
        botao_avancar_pagina.setShortcut('Ctrl+e')
        botao_avancar_pagina.triggered.connect(lambda: self.abas.currentWidget().forward()) 
        barra_de_navegacao.addAction(botao_avancar_pagina) 
        #-----------------------------------------------

        botao_de_atualizar_pagina = QAction(QIcon('./icones/atualizar.png'),"Atualizar - Ctrl+r", self) 
        botao_de_atualizar_pagina.setShortcut('Ctrl+r')
        botao_de_atualizar_pagina.triggered.connect(lambda: self.abas.currentWidget().reload()) 
        barra_de_navegacao.addAction(botao_de_atualizar_pagina) 
        #-------------------------------------------------------

        botao_da_pagina_inicial = QAction(QIcon('./icones/pagina-inicial.png'),"Home - Ctrl+h", self) 
        botao_da_pagina_inicial.setShortcut('Ctrl+h')
        botao_da_pagina_inicial.triggered.connect(self.pagina_inicial) 
        barra_de_navegacao.addAction(botao_da_pagina_inicial) 

         #-------------------------------------------------------------
        self.barra_de_pesquisa = QLineEdit()
        self.barra_de_pesquisa.setStyleSheet("QLineEdit""{" "border-radius:0px; padding: 4px;""}") 
        font = QFont()
        font.setPointSize(11)
        self.barra_de_pesquisa.setFont(font)
        self.barra_de_pesquisa.returnPressed.connect(self.carregar_url) 
        barra_de_navegacao.addWidget(self.barra_de_pesquisa) 
        self.adicionar_nova_aba(QUrl('https://duckduckgo.com'), 'Página inicial') 
        self.show() 
        
    def adicionar_nova_aba(self, qurl = None, label ="Nova guia"): 
        if qurl is None: 
              qurl = QUrl('https://duckduckgo.com') 
        browser = QWebEngineView() 
          #download--------------------------
        browser.page().profile().downloadRequested.connect(self.download)
        browser.setUrl(qurl) 
        i = self.abas.addTab(browser, label) 
        self.abas.setCurrentIndex(i) 
        browser.urlChanged.connect(lambda qurl, browser = browser:self.atualizar_barra_de_pesquisa(qurl, browser)) 
        browser.loadFinished.connect(lambda _, i = i, browser = browser: self.abas.setTabText(i, browser.page().title())) 
  
    def abrir_aba_com_duplo_click(self, i): 
      if i == -1: 
        self.adicionar_nova_aba() 
  
    def alternar_entre_as_guias(self, i): 
        qurl = self.abas.currentWidget().url() 
        self.atualizar_barra_de_pesquisa(qurl, self.abas.currentWidget()) 
        # self.update_title(self.abas.currentWidget()) 

    def fechar_aba(self, i): 
        if self.abas.count() < 2: 
              return
        self.abas.removeTab(i) 
  
    def pagina_inicial(self): 
        self.abas.currentWidget().setUrl(QUrl("https://duckduckgo.com")) 
  
    
    def carregar_url(self): 
        url = QUrl(self.barra_de_pesquisa.text()) 
        if url.scheme() == "": 
              url.setScheme("https") 
        self.abas.currentWidget().setUrl(url) 
  
    
    def atualizar_barra_de_pesquisa(self, url, browser = None): 
        if browser != self.abas.currentWidget(): 
            return
        self.barra_de_pesquisa.setText(url.toString()) 
    
    def download(self, object):
        object.accept()
        msg = QMessageBox()
        msg.setWindowTitle('Download')
        msg.setText('O seu download foi inicializado')
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

        
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    app.setApplicationName('Web Browser') 
    window = Window() 
    app.exec_()  