from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from multiprocessing import Pool, Manager

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无头模式
    return webdriver.Chrome(options=options)

def fetch_data():
    driver = init_driver()
    driver.get("https://www.toolify.ai/category")
    
    father = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div[2]/div/div[2]/div[2]')
    child_elements = father.find_elements(By.XPATH, './div')
    
    data_list = []
    for target in child_elements:
        title = target.find_element(By.XPATH, './h3').text
        target_elements = target.find_elements(By.XPATH, './div/a')
        for i in target_elements:
            subtitle = i.find_element(By.XPATH, './span').text
            num = i.find_element(By.XPATH, './div').text
            links = i.get_attribute('href')
            data_list.append((title, subtitle, num, links))
    
    driver.quit()
    return data_list

def process_data(item, data):
    title, subtitle, num, links = item
    if title not in data:
        data[title] = []
    data[title].append({subtitle: {'num': num, 'links': links}})

def main():
    data_list = fetch_data()
    
    manager = Manager()
    data = manager.dict()
    
    with Pool(processes=4) as pool:
        pool.starmap(process_data, [(item, data) for item in data_list])
    
    result = {"category": dict(data)}
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()