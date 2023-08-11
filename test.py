# Python program to demonstrate
# selenium
 
# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
 
# create webdriver object
driver = webdriver.Chrome()
 
# enter keyword to search
keyword = "geeksforgeeks"
 
# get geeksforgeeks.org
driver.get("https://www.geeksforgeeks.org/")
 
# get element
element = driver.find_element(By.NAME, "search")
 
# print complete element
print(element)