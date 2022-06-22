import pyodbc
con = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:/Users/DIASSANA/Desktop/LIEEMA/lieema.accdb;')
c= con.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS Etudiants(task_name TEXT Not Null,task_fname TEXT Not Null,numeroEtu Number,task_date DATE,niveau Number,task_cp Number,sexe TEXT Not Null,contact Number,secti TEXT Not Null,nomComite TEXT Not Null,task_info TEXT Not Null,CONSTRAINT pk_numeroEtu PRIMARY KEY (numeroEtu))')
    

def add_data(task_name,task_fname,numeroEtu,task_date,niveau,task_cp,sexe,contact,secti,nomComite,task_info):
	c.execute('INSERT INTO Etudiants(task_name,task_fname,numeroEtu,task_date,niveau,task_cp,sexe,contact,secti,nomComite,task_info) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',task_name,task_fname,numeroEtu,task_date,niveau,task_cp,sexe,contact,secti,nomComite,task_info)
	con.commit()

def view_all_data():
	c.execute('SELECT * FROM Etudiants')
	data = c.fetchall()
	return data
