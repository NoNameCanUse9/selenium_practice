from selenium import webdriver
from selenium.webdriver.common.by import By
import json
data={}
driver = webdriver.Chrome()
driver.get("https://www.toolify.ai/category")
father = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div[2]/div/div[2]/div[2]')
child=father.find_elements(By.XPATH, './div')
for target in child:
    title=target.find_element(By.XPATH, './h3').text
    target=target.find_elements(By.XPATH, './div/a')
    data[title]=[]
    for i in target:
        subtitle=i.find_element(By.XPATH, './span').text
        num=i.find_element(By.XPATH, './div').text
        links=i.get_attribute('href')
        data[title].append({subtitle:{'resources_num':num,'links':links}})
        
result={}
result["category"]=data
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)