import os,sys
import bib2ref,resource_rc
from PyQt5.QtWidgets import QApplication, QMainWindow
from functools import partial
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
mode_num = 1
def input_file(ui):
    try:
        input_path = ui.input_bib()
        ui.lineEdit.setText(str(input_path))
    except:
        pass
def output_file(ui):
    try:
        output_path = ui.output_txt()
        ui.lineEdit_2.setText(str(output_path))
    except:
        pass
def doimode(ui):
    global mode_num
    mode_num = 2
def batchmode(ui):
    global mode_num
    mode_num = 1
def exitgui(ui):
    qapp = QApplication.instance()
    qapp.quit()
def baidu(ui):
    global mode_num
    xpath = "//a[@class='paper_q']"
    try:
        if mode_num == 1:
            input_path = ui.lineEdit.text()
            f = open(input_path, 'r', encoding='UTF-8')
            doi = []
            cite = []
            num = 0
            line = f.readline()
            while line:
                if "doi =" in line:
                    doi.append(line.split('{')[-1].split('}')[0])
                line = f.readline()
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chromeDriverPath = 'chromedriver.exe'
            driver = webdriver.Chrome(options=chrome_options, executable_path=chromeDriverPath)
            driver.get('http://xueshu.baidu.com/')
            for i in doi:
                num = num + 1
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "kw")))
                    driver.find_element_by_id("kw").send_keys(i)
                    driver.find_element_by_id("su").click()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sc_quote_bg")))
                    driver.find_element_by_xpath(xpath).click()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sc_cit0")))
                    dr = driver.find_element_by_id('sc_cit0')
                    dr.get_attribute('data-original-title')
                    text = "[" + str(num) + "]" + ' ' + dr.text
                except:
                    text = "[" + num +" ] Timeout or There is no data matching with this doi:" + i
                cite.append(text)
                driver.back()
            driver.quit()
            output_path = ui.lineEdit_2.text()
            file_write = open(output_path, 'a', encoding='utf8')
            ui.textBrowser.append("*****Baidu Academic*****")
            for i in cite:
                file_write.writelines(i + '\n')
                ui.textBrowser.append(i)
            file_write.close()
        elif mode_num == 2:
            doi_num = ui.lineEdit_3.text()
            if doi_num == '':
                pass
            else:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-gpu")
                chromeDriverPath = 'chromedriver.exe'
                driver = webdriver.Chrome(options=chrome_options,executable_path=chromeDriverPath)
                driver.get('http://xueshu.baidu.com/')
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "kw")))
                    driver.find_element_by_id("kw").send_keys(doi_num)
                    driver.find_element_by_id("su").click()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sc_quote_bg")))
                    driver.find_element_by_xpath(xpath).click()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sc_cit0")))
                    dr = driver.find_element_by_id('sc_cit0')
                    dr.get_attribute('data-original-title')
                    text = "[DOI MODE]" + ' ' + dr.text
                except:
                    text =  "[DOI MODE] Timeout or There is no data matching with this doi:" + doi_num
                driver.quit()
                ui.textBrowser.append("*****Baidu Academic*****")
                ui.textBrowser.append(text)
    except:
        pass
def bing(ui):
    global mode_num
    xpath = "//div[@class='aca_citeStr']"
    locator = ("xpath", "//span[@class='b_floatR']")
    until_text = "GBT7714"
    try:
        if mode_num == 1:
            input_path = ui.lineEdit.text()
            f = open(input_path, 'r', encoding='UTF-8')
            doi = []
            cite = []
            num = 0
            line = f.readline()
            while line:
                if "doi =" in line:
                    doi.append(line.split('{')[-1].split('}')[0])
                line = f.readline()
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chromeDriverPath = 'chromedriver.exe'
            driver = webdriver.Chrome(options=chrome_options, executable_path=chromeDriverPath)
            driver.get('https://cn.bing.com/academic')
            for i in doi:
                num = num + 1
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sb_form_q")))
                    driver.find_element_by_id("sb_form_q").send_keys(i)
                    driver.find_element_by_id("sb_form_go").click()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "aca_cref")))
                    driver.find_element_by_id("aca_cref").click()
                    WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element(locator,until_text))
                    dr = driver.find_element_by_xpath(xpath)
                    dr.get_attribute('data-original-title')
                    text = "[" + str(num) + "]" + ' ' + dr.text
                except:
                    text = "[" + num +" ] Timeout or There is no data matching with this doi:" + i
                cite.append(text)
                driver.back()
            driver.quit()
            output_path = ui.lineEdit_2.text()
            file_write = open(output_path, 'a', encoding='utf8')
            ui.textBrowser.append("*****Bing Academic*****")
            for i in cite:
                file_write.writelines(i + '\n')
                ui.textBrowser.append(i)
            file_write.close()
        elif mode_num == 2:
            doi_num = ui.lineEdit_3.text()
            if doi_num == '':
                pass
            else:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-gpu")
                chromeDriverPath = 'chromedriver.exe'
                driver = webdriver.Chrome(options=chrome_options,executable_path=chromeDriverPath)
                driver.get('https://cn.bing.com/academic')
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sb_form_q")))
                    driver.find_element_by_id("sb_form_q").send_keys(doi_num)
                    driver.find_element_by_id("sb_form_go").click()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "aca_cref")))
                    driver.find_element_by_id("aca_cref").click()
                    WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element(locator, until_text))
                    dr = driver.find_element_by_xpath(xpath)
                    dr.get_attribute('data-original-title')
                    text = "[DOI MODE]" + ' ' + dr.text
                except:
                    text =  "[DOI MODE] Timeout or There is no data matching with this doi:" + doi_num
                driver.quit()
                ui.textBrowser.append("*****Bing Academic*****")
                ui.textBrowser.append(text)
    except:
        pass
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = bib2ref.Ui_mainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.pushButton.clicked.connect(partial(input_file,ui))
    ui.pushButton_2.clicked.connect(partial(output_file,ui))
    ui.pushButton_4.clicked.connect(partial(exitgui,ui))
    ui.pushButton_3.clicked.connect(partial(bing,ui))
    ui.pushButton_5.clicked.connect(partial(baidu,ui))
    ui.pushButton_6.clicked.connect(partial(doimode,ui))
    ui.pushButton_7.clicked.connect(partial(batchmode,ui))
    sys.exit(app.exec_())
