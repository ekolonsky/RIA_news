# Euegen Kolonsky 2022
# scrip for news headlines data scrapping from RIA Novosti web site
# data collected from pages with url  https//:ria.ru/YYYYMMDD/?page=N

import urllib, urllib.request, time, datetime
from bs4 import BeautifulSoup
from datetime import date, timedelta


site = 'https://ria.ru/'

# set here start date, final date and filename for data saving

start_day = '20151231'
fin_day   = '20130101'
filename = 'corpus-15-13.txt'

def get_page(day, page_num):
  url = site + day
  url_page = url + '/?page=' + str(page_num)
  print('.', end='')
  #print(url_page)
  try:
    req = urllib.request.Request(url_page)
    resp = urllib.request.urlopen(req, timeout=2)
    respData = resp.read().decode('utf-8')
  except Exception as e:
    respData = ''
  return respData

def get_links(html_page, day):
  links = {}
  soup = BeautifulSoup(html_page)
  for link in soup.find_all('a'):
      href = str(link.get('href'))
      title = str(link.string)
      if  day in href and 'html' in href and len(title) > 10:
        #print(href, title)
        links[href] = title
  return links  

def get_day(day):
  links = {}
  for page_num in range(1,100):
    p = get_page(day, page_num)
    more_links = get_links(p, day)
    if any(link in links.keys() for link in more_links.keys()) or len(more_links)==0:
        break
    else:
        links.update(more_links)
  return links

def save(filename, dict):
  file = open(filename, 'a')
  for key in dict:
    file.write(key +'\t' + dict[key] +  '\n')
  file.close()
  return 
  
counter = 0
day = datetime.datetime.strptime(start_day, '%Y%m%d')
strday = day.strftime('%Y%m%d') 

while strday > fin_day:
  strday = day.strftime('%Y%m%d') 
  print(strday, end='')
  headers = get_day(strday)
  save(filename, headers)
  counter += 1
  day = day - timedelta(days=1)
  print(len(headers))
  
  
