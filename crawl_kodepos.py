import requests
from bs4 import BeautifulSoup
import re
import sqlite3
from tqdm import tqdm

from slugify import slugify


def pages(soup_city):
	pages_to_exec = []
	for ul in soup_city.find_all('ul',class_='pagination'):
		for li in ul.find_all('li'):
			if unicode(li) != b' ' or unicode(li) != b'\n':
				# class has multiple value
				if li.get('class') not in [[u'disabled'],[u'active']] and li.string != 'NEXT':
					# last_page = li.string
					pages_to_exec.append(li.a.get('href'))
	return pages_to_exec

def crawl(soup_city):
	conn = sqlite3.connect('koposindo.db')
	c = conn.cursor()
	table = soup_city.find_all('tr')

	for city_table in table:
		if unicode(city_table) != b' ' or unicode(city_table) != b'\n':
			counter = 0
			for td_data in tqdm(city_table.find_all('td')):
				# provinsi
				if counter == 0:
					print('executing provinsi==>',td_data.a.get('href'))
					province_slug = td_data.a.get('href').split(url+'/provinsi/')
					data = (province_slug[1],)

					c.execute('SELECT * FROM provinsi WHERE slug=?', data)
					prov_id = c.fetchone()[0]
				# kotamadya
				if counter == 1:
					print('executing kota/kotamadya==>',td_data.a.get('href'))
					city_slug = td_data.a.get('href').split(url+'/daerah/'+province_slug[1]+'/')
					city_name = td_data.a.string
					data = (prov_id,city_slug[1],)

					c.execute('SELECT * FROM kota WHERE provinsi_id=? AND slug=?', data)
					result_city = c.fetchone()
					if result_city is None:

						insert_data = (None,prov_id,city_name,city_slug[1],)
						c.execute('INSERT INTO kota VALUES (?,?,?,?)',insert_data)
						conn.commit()

					c.execute('SELECT * FROM kota WHERE provinsi_id=? AND slug=?', data)
					result_city = c.fetchone()
					kota_id = result_city[0]

				# kecamatan
				if counter == 2:
					print('executing kecamatan==>',td_data.a.get('href'))
					kecamatan_slug = td_data.a.get('href').split(url+'/daerah/'+province_slug[1]+'/'+city_slug[1]+'/')
					kecamatan_name = td_data.a.string
					data = (prov_id,kota_id,kecamatan_slug[1],)

					c.execute('SELECT * FROM kecamatan WHERE provinsi_id=? AND kota_id=? AND slug=?', data)
					result_kecamatan = c.fetchone()
					if result_kecamatan is None:

						insert_data = (None,prov_id,kota_id,kecamatan_name,kecamatan_slug[1],)
						c.execute('INSERT INTO kecamatan VALUES (?,?,?,?,?)',insert_data)
						conn.commit()

					c.execute('SELECT * FROM kecamatan WHERE provinsi_id=? AND kota_id=? AND slug=?', data)
					result_kecamatan = c.fetchone()
					kecamatan_id = result_kecamatan[0]

				# kelurahan
				if counter == 3:
					print('executing kelurahan==>',td_data.a.get('href'))
					kelurahan_slug = td_data.a.get('href').split(url+'/daerah/'+province_slug[1]+'/'+city_slug[1]+'/'+kecamatan_slug[1]+'/')
					kelurahan_name = td_data.a.string
					data = (prov_id,kota_id,kecamatan_id,kelurahan_name,kelurahan_slug[1],)

					c.execute('SELECT * FROM kelurahan WHERE provinsi_id=? AND kota_id=? AND kecamatan_id=? AND kelurahan=? AND slug=?', data)
					result_kelurahan = c.fetchone()
					print(type(result_kelurahan))
					if result_kelurahan is None:

						insert_data = (None,prov_id,kota_id,kecamatan_id,kelurahan_name,kelurahan_slug[1],None,)
						c.execute('INSERT INTO kelurahan VALUES (?,?,?,?,?,?,?)',insert_data)
						conn.commit()

					c.execute('SELECT * FROM kelurahan WHERE provinsi_id=? AND kota_id=? AND kecamatan_id=? AND kelurahan=? AND slug=?', data)
					result_kelurahan = c.fetchone()
					kelurahan_id = result_kelurahan[0]

				# kodepos
				if counter == 4:
					print('executing kodepos==>',td_data.a.get('href'))
					kodepos_slug = td_data.a.get('href').split(url+'/kodepos/')
					data = (kodepos_slug[1],prov_id,kota_id,kecamatan_id,kelurahan_name,kelurahan_slug[1],)

					c.execute('UPDATE kelurahan SET kodepos=? WHERE provinsi_id=? AND kota_id=? AND kecamatan_id=? AND kelurahan=? AND slug=?', data)
					conn.commit()
				
				counter += 1

	c.close()
	conn.close()





url = 'https://www.koposindo.com'
r = requests.get(url)
soup = BeautifulSoup(r.text,'html.parser')

for province_label in soup.find_all('a',href=re.compile('^provinsi/')):	
	# if 'dki-jakarta' in province_label.get('href'):
	print('execute %s/%s' % (url,province_label.get('href')))
	r_city = requests.get('%s/%s' % (url,province_label.get('href')))

	soup_city = BeautifulSoup(r_city.text,'html.parser')

# using file
# with open('koposindo.html') as fp:
# 	soup_city = BeautifulSoup(fp,'html.parser')

	# first page/current
	crawl(soup_city)

	# remain pages
	remain_pages = pages(soup_city)
	for p in remain_pages:
		r = requests.get(p)
		soup = BeautifulSoup(r.text,'html.parser')
		crawl(soup)
