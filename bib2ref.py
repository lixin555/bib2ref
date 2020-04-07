#!/usr/bin/env python
# bib2ref
# Anaconda3 is recommended for users, and selenium is needed.
# The script is used to extract doi form bibtex file to generate a reference list which can be used in markdown.
# GNU General Public License v3.0
# Author: Li Xin, a graduate student studying Materials Science & Engineering in USTB
# Email: lixin@xs.ustb.edu.cn  Homepage: https://www.yuhualixin.com/714.html
# Github: https://github.com/lixin555/bib2ref 
import os
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def select_inputfile():
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename(title=u'Input File',filetypes=[('bibtex file', '.bib')])
    print('input path:',filepath)
    return filepath
def select_savefile():
    root = tk.Tk()
    root.withdraw()
    save_path = filedialog.asksaveasfilename(title=u'Save File',filetypes=[('txt file', '.txt')])+".txt"
    print('save path:',save_path)
    return save_path
path = select_inputfile()
f = open(path,'r', encoding='UTF-8')
doi   = []
cite  = []
num   = 0
xpath = "//a[@class='paper_q']"
line = f.readline()
while line:
    if "doi =" in line:
        doi.append(line.split('{')[-1].split('}')[0])
    line = f.readline()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)
driver.get('http://xueshu.baidu.com/')
for i in doi:
    num = num +1
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "kw")))
    except:
        print("error1")
    driver.find_element_by_id("kw").send_keys(i)
    driver.find_element_by_id("su").click()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "head_wr")))
    except:
        print("error2")
    driver.find_element_by_xpath(xpath).click()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sc_cit0")))
    except:
        print("error3")
    dr = driver.find_element_by_id('sc_cit0')
    dr.get_attribute('data-original-title')
    text = "["+str(num)+"]"+' '+dr.text
    cite.append(text)
    driver.back()
driver.quit()
print(cite)
save_path = select_savefile()
file_write = open(save_path, 'a', encoding='utf8')
for i in cite:
    file_write.writelines(i+'\n')
file_write.close()
print("Work done")
os.system('pause')
