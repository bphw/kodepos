import sqlite3

conn = sqlite3.connect('koposindo.db')
c = conn.cursor()
# Create table
c.execute('''CREATE TABLE IF NOT EXISTS provinsi
             (id integer PRIMARY KEY, provinsi text, slug text)''')

# Insert a row of data
c.execute("INSERT INTO provinsi VALUES (NULL,'Nanggroe Aceh Darussalam','nanggroe-aceh-darussalam')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Sumatera Utara','sumatera-utara')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Sumatera Barat','sumatera-barat')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Riau','riau')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Jambi','jambi')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Sumatera Selatan','sumatera-selatan')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Bengkulu','bengkulu')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Lampung','lampung')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Kepulauan Bangka Belitung','kepulauan-bangka-belitung')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Kepulauan Riau','kepulauan-riau')")
c.execute("INSERT INTO provinsi VALUES (NULL,'DKI Jakarta','dki-jakarta')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Jawa Barat','jawa-barat')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Jawa Tengah','jawa-tengah')")
c.execute("INSERT INTO provinsi VALUES (NULL,'DI Yogyakarta','di-yogyakarta')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Jawa Timur','jawa-timur')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Banten','banten')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Bali','bali')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Nusa Tenggara Barat','nusa-tenggara-barat')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Nusa Tenggara Timur','nusa-tenggara-timur')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Kalimantan Barat','kalimantan-barat')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Kalimantan Tengah','kalimantan-tengah')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Kalimantan Selatan','kalimantan-selatan')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Kalimantan Timur','kalimantan-timur')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Kalimantan Utara','kalimantan-utara')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Sulawesi Utara','sulawesi-utara')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Sulawesi Tengah','sulawesi-tengah')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Sulawesi Selatan','sulawesi-selatan')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Sulawesi Tenggara','sulawesi-tenggara')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Gorontalo','gorontalo')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Sulawesi Barat','sulawesi-barat')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Maluku','maluku')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Maluku Utara','maluku-utara')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Papua','papua')")
c.execute("INSERT INTO provinsi VALUES (NULL,'Papua Barat','papua-barat')")


# Save (commit) the changes
conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS kota
             (id integer PRIMARY KEY, provinsi_id integer, kota text, slug text)''')
c.execute('''CREATE TABLE IF NOT EXISTS kecamatan
             (id integer PRIMARY KEY, provinsi_id integer, kota_id integer, kecamatan text, slug text)''')
c.execute('''CREATE TABLE IF NOT EXISTS kelurahan
             (id integer PRIMARY KEY, provinsi_id integer, kota_id integer, kecamatan_id integer, kelurahan text, slug text, kodepos integer)''')

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()