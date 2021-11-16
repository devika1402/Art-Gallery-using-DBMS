from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os
from datetime import date
app = Flask(__name__)

UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# HOME PAGE
@app.route("/")
def home():
       return render_template("index.html", content="Testing")
    
# CREATING A DATABASE CONSISTING OF Art and Genre TABLES
# CREATING THE Art TABLE
@app.route('/createdb',methods=['POST'])
def createArtdb():
   print("Making a connection")
   connection = sqlite3.connect('db.db')

   print ("Getting a cursor")
   cursor = connection.cursor()
   
   print ("Executing the DML")
   cursor.execute('''CREATE TABLE IF NOT EXISTS Art 
                  (pk INTEGER PRIMARY KEY, Title TEXT, 
                  Artist TEXT, Genre TEXT, Year INT, Photo TEXT, Appr INTEGER)''')

   print("Committing the changes")
   connection.commit()
   
   print("Closing the database")
   connection.close()
   
   return('Art table created successfully')

# CREATING THE Genre TABLE
@app.route('/creategdb',methods=['POST'])
def creategdb():
   print("Making a connection")
   connection = sqlite3.connect('db.db')

   print ("Getting a cursor")
   cursor1 = connection.cursor()
   
   print ("Executing the DML")
   cursor1.execute('''CREATE TABLE IF NOT EXISTS Genre
                  (id INTEGER PRIMARY KEY, Name TEXT, 
                  About TEXT, Date_modified DATE)''')
   
   print("Committing the changes")
   connection.commit()
   
   print("Closing the database")
   connection.close()
   
   return('Genre Table and Database created successfully')


# CREATION OF GENRES
@app.route('/creategenre', methods = ['GET','POST'])
def creategenre():
   
   if request.method == 'POST':
      name = request.form['name']
      about = request.form['about']
      datemodified = date.today()

      try:
         print ("making a connection")
         connection = sqlite3.connect('db.db')

         print ("Getting a Cursor")
         cursor = connection.cursor()
         
         print ("Executing the DML")
         # Entry of data into genre table
         cursor.execute("INSERT into Genre (Name, About, Date_modified) values (?,?,?)",
                        (name,about,datemodified))  
      
         print ("Commiting the changes")
         connection.commit()

         print ("Closing the database")
         connection.close()

         return redirect(url_for('genrelist'))
   
      except Exception as error:
         return_message = str(error)
         return(return_message)

   else:
      return render_template("creategenre.html")
   
# DISPLAYING THE LIST OF GENRES (READING DATABASE)
@app.route('/genrelist', methods=['GET']) 
def genrelist():
   print("Making a connection")
   connection = sqlite3.connect('db.db')

   print ("Getting a cursor")
   cursor = connection.cursor()
   
   print ("Executing the DML")
   cursor.execute("select * from Genre") #accessing all genre data (name,about,date modified)

   print("Get the Rows from cursor")
   g_rows = cursor.fetchall()
   
   print("Closing the database")
   connection.close()

   print(g_rows)
   return render_template("genrelist.html", g_rows = g_rows)

# GETTING INPUT FOR GENRE NAMES FOR THE DROP DOWN LIST DISPLAYING THE LIST OF GENRES (READING DATABASE) FOR CREATING ARTWORK
@app.route('/artworkcreate') 
def genrenames():
   print("Making a connection")
   connection = sqlite3.connect('db.db')

   print ("Getting a cursor")
   cursor = connection.cursor()
   
   print ("Executing the DML")
   cursor.execute("select * from Genre order by Name") #accessing genre names

   print("Get the Rows from cursor")
   gname = cursor.fetchall()
   
   print("Closing the database")
   connection.close()

   print(gname)
   return render_template("artworkcreate.html", gname = gname)

# GETTING INPUT FOR GENRE NAMES FOR THE DROP DOWN LIST DISPLAYING THE LIST OF GENRES (READING DATABASE) FOR UPDATING ARTWORK
@app.route('/artworkupdate') 
def genrenames():
   print("Making a connection")
   connection = sqlite3.connect('db.db')

   print ("Getting a cursor")
   cursor = connection.cursor()
   
   print ("Executing the DML")
   cursor.execute("select * from Genre order by Name") #accessing genre data names

   print("Get the Rows from cursor")
   gname = cursor.fetchall()
   
   print("Closing the database")
   connection.close()

   print(gname)
   return render_template("artworkupdate.html", gname = gname)

# UPDATION OF GENRE DETAILS
@app.route("/genreupdate/<int:pk>", methods=['GET','POST'])
def genreupdate(id):
   
   if request.method == 'POST':
      name = request.form['name']
      about = request.form['about']
      datemodified = date.today()
         
      try:
         print ("Making a connection", id)
         connection = sqlite3.connect('db.db')
      
         print ("Getting a Cursor")
         cursor = connection.cursor()
         
         print ("Executing the DML")
         cursor.execute("UPDATE Genre SET Name=?, About=?, Date_modified=? WHERE id=?",(name,about,datemodified,id))  
         
         print ("Committing the changes")
         connection.commit()
         return redirect(url_for('genrelist'))

      except Exception as error:
         return_message = str(error)
         return(return_message)
 
   else:
         
      print ("Making a connection")
      connection = sqlite3.connect('db.db')
   
      print ("Getting a Cursor")
      cursor = connection.cursor()
      
      print ("Executing the DML")
      cursor.execute("select * from Genre where id=(?)",(id,))

      print ("Get the Rows from cursor")
      show_data = cursor.fetchall()
      
      print ("Closing the database")
      connection.close()

      return render_template("genreupdate.html", show_data = show_data)

# CREATION OF ARTWORKS' DETAILS' ENTRIES
@app.route('/artworkcreate', methods = ['GET','POST'])
def artworkcreate():
   
   if request.method == 'POST':
      title = request.form['title']
      artist = request.form['artist']
      genre = request.form['genre']
      year = request.form['year']
      image = request.files['file']  
      appr = 0

      try:
         # file url is used for storing images at an absolute location on the os file folder.
         file_url = os.path.join(os.getcwd() + UPLOAD_FOLDER, image.filename)

         # static url is required for serving images from a static folder. store this on SQL DB
         staic_url = os.path.join(UPLOAD_FOLDER, image.filename)

         image.save(file_url)

         print ("Making a connection")
         connection = sqlite3.connect('db.db')

         print ("Getting a Cursor")
         cursor = connection.cursor()
         
         print ("Executing the DML")
         cursor.execute("INSERT into Art (Title, Artist, Genre, Year, Photo, Appr) values (?,?,?,?,?,?)",
                        (title,artist,genre,year,staic_url,appr))  
         
         print ("Committing the changes")
         connection.commit()

         print ("Closing the database")
         connection.close()

         return redirect(url_for('artlist'))
   
      except Exception as error:
         return_message = str(error)
         return(return_message)

   else:
      return render_template("artworkcreate.html")
   
# DISPLAYING THE LIST OF ARTWORKS (READING DATABASE)
@app.route('/artlist', methods=['GET']) 
def artlist():
   print("Making a connection")
   connection = sqlite3.connect('db.db')

   print ("Getting a cursor")
   cursor = connection.cursor()
   
   print ("Executing the DML")
   cursor.execute("select * from Art")

   print("Get the Rows from cursor")
   rows = cursor.fetchall()
   
   print("Closing the database")
   connection.close()

   print(rows)
   return render_template("artlist.html", art = rows)

# UPDATION OF ARTWORK DETAILS
@app.route("/artworkupdate/<int:pk>", methods=['GET','POST'])
def artworkupdate(pk):
   
   if request.method == 'POST':
      title = request.form['title']
      artist = request.form['artist']
      genre = request.form['genre']
      year = request.form['year']
      image = request.files['file']

      if(len(image.filename)!=0): #if no image is selected (in case of updating artwork details)
         old_image = request.form['image_file']
         current_dir = os.getcwd()

         old_image_url = current_dir + old_image
         print(old_image_url)
         
         try:
            # file url is used for storing images at an absolute location on the os file folder.
            file_url = os.path.join(os.getcwd()+ UPLOAD_FOLDER, image.filename)

            # static url is required for serving images from a static folder. store this on SQL DB
            static_url = os.path.join(UPLOAD_FOLDER, image.filename)

            image.save(file_url)

            # Let's delete old image
            os.remove(old_image_url)

            print ("Making a connection", pk)
            connection = sqlite3.connect('db.db')
         
            print ("Getting a Cursor")
            cursor = connection.cursor()
            
            print ("Executing the DML")
            cursor.execute("UPDATE Art SET Title=?, Artist=?, Genre=?, Year=?, Photo=? WHERE pk=?",(title,artist,genre,year,static_url,pk))  
            
            print ("Committing the changes")
            connection.commit()
            return redirect(url_for('artlist'))
   
         except Exception as error:
            return_message = str(error)
            return(return_message)
   
      else:
         
         print ("Making a connection",pk)
         connection = sqlite3.connect('db.db')
      
         print ("Getting a Cursor")
         cursor = connection.cursor()
         
         print ("Executing the DML")
         cursor.execute("UPDATE Art SET Title=?, Artist=?, Genre=? Year=? WHERE pk=?",(title,artist,genre,year,pk))

         print ("Committing the changes")
         connection.commit()
         
         return redirect(url_for('artlist'))
         
   
   else:
         
      print ("Making a connection")
      connection = sqlite3.connect('db.db')
   
      print ("Getting a Cursor")
      cursor = connection.cursor()
      
      print ("Executing the DML")
      cursor.execute("select * from Art where pk=(?)",(pk,))

      print ("Get the Rows from cursor")
      show_data = cursor.fetchall()
      
      print ("Closing the database")
      connection.close()

      return render_template("artworkupdate.html", show_data = show_data)

# DELETION OF ARTWORKS
@app.route("/artworkdelete/<int:pk>", methods=['GET','POST'])
def artworkdelete(pk):
      
   try:

      print ("making a connection")
      connection = sqlite3.connect('db.db')

      print ("Getting a Cursor")
      cursor = connection.cursor()
      
      print ("Executing the DML")
      cursor.execute("DELETE from Art where pk=(?)", (pk,))
      
      print ("Commiting the changes")
      connection.commit()

      print ("Closing the database")
      connection.close()
      
      return redirect(url_for('artlist'))
   
   
   except Exception as error:
      return_message = str(error)
      return(return_message)

# LIKING ARTWORK
@app.route("/like/<int:pk>",methods=['GET','POST'])
def like(pk):
   print ("Making a connection")
   connection = sqlite3.connect('db.db')

   print ("Getting a Cursor")
   cursor = connection.cursor()
      
   print ("Executing the DML")
   cursor.execute("UPDATE Art SET Appr=Appr+1 WHERE pk=(?)",(pk,))

   print ("Committing the changes")
   connection.commit()

   print ("Closing the database")
   connection.close()

   print ("Making a connection")
   connection = sqlite3.connect('db.db')

   print ("Getting a Cursor")
   cursor = connection.cursor()

   print ("Executing the DML")
   cursor.execute("SELECT * from Art where pk=(?)",(pk,))

   print ("Get the Rows from cursor")
   data = cursor.fetchall() 

   print ("Closing the database")
   connection.close()

   return render_template("like.html", item = data)

if __name__ == '__main__':
   app.run()
   app.debug = True