from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import unittest
import var

class TesteDeRegistroFIEF(unittest.TestCase):
    def insere_valores_pagina_1(self, valor_curso = "131"):
        self.driver = webdriver.Chrome(var.driver_path)
        driver = self.driver
        driver.maximize_window()
        driver.get(var.url_pagina)
        elemento = driver.find_element_by_name("ctl00$ContentPlaceHolder1$pageControl$txtCPF")
        elemento.clear()
        elemento.send_keys(var.cpf_valido)
        action = ActionChains(driver)
        action.move_to_element_with_offset(elemento, 300, 300)
        action.click()
        action.perform()
        Select(driver.find_element_by_name("ctl00$ContentPlaceHolder1$pageControl$ddlAnoSemestre")).select_by_value("20193")
        Select(driver.find_element_by_name("ctl00$ContentPlaceHolder1$pageControl$ddlCurso")).select_by_value(valor_curso)
        driver.find_element_by_xpath("//*[@id=\"ctl00_ContentPlaceHolder1_pageControl_btnProxGeral\"]").click()

    def insere_valores_pagina_2(self):
        driver = self.driver
        for i in range(len(var.elementos_pagina_2)):
            driver.find_element_by_name(var.elementos_pagina_2[i]).send_keys(var.chaves_pagina_2[i])
    
    def checa_se_passou(self):
        self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_pageControl_ASPxButton1_CD").click()
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$pageControl$rdbList")

    def insere_dados_texto(self, elemento, chave):
        self.driver.find_element_by_name(elemento).send_keys(chave)
        self.checa_se_passou()

    def insere_dados_select(self, elemento):
        driver = self.driver
        Select(driver.find_element_by_name(elemento)).select_by_value("SE")
        self.checa_se_passou()
    
    def clica_botoes(self):
        self.driver.find_element_by_name(var.botoes[0]).click()
        self.driver.find_element_by_id(var.botoes[1]).click()

    #Assegura que o cadastro de todos os cursos estão funcionando corretamente
    def test_registro_primeira_pagina(self):    
        for i in range (len(var.valores_curso_parcial)):
            self.insere_valores_pagina_1(var.valores_curso_parcial[i])
            try:
                self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$pageControl$txtNome")
            except NoSuchElementException:
                self.fail()
                self.driver.quit()
            else:
                self.driver.quit()

    
    #Assegura que usuário não passará para a próxima página se algum dos campos requeridos estiver vazio
    def test_registro_segunda_pagina_requeridos(self):
        self.insere_valores_pagina_1()
        for i in range (len(var.elementos_pagina_2)):
            self.insere_dados_texto(var.elementos_pagina_2[i], var.chaves_pagina_2[i])
        for i in range (len(var.selecionaveis_pagina_2)):
            self.insere_dados_select(var.selecionaveis_pagina_2[i])
        self.clica_botoes()
        try:
            self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$pageControl$rdbList")
        except NoSuchElementException:
            self.fail()
            self.driver.quit()
        else:
            self.driver.quit()


    #Assegura que o cadastro a partir de todas as UFs estão funcionando corretamente
    def test_segunda_pagina_uf(self):
        for i in range(len(var.valores_uf_parcial)):
            try:
                self.insere_valores_pagina_1()
                self.insere_valores_pagina_2()
                Select(self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$pageControl$ufsRG")).select_by_value("SE")
                Select(self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$pageControl$ufsPessoal")).select_by_value(var.valores_uf_parcial[i])
                self.clica_botoes()
                self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$pageControl$rdbList")
            except NoSuchElementException:
                self.fail()
                self.driver.quit()
            else:
                self.driver.quit()

if __name__ == '__main__':
    unittest.main()