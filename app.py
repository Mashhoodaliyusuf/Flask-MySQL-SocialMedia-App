import os
import sys
import mysql.connector

from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)


app.secret_key = os.urandom(24)


conn = mysql.connector.connect(user='shmplcoi_social', password='bravoechoM1!@#$', host='localhost',
                              database='shmplcoi_social')

cursor = conn.cursor()










@app.route('/')
def login():
    if 'user_id' in session:
        user_name = session['user_name']
        user_img = session['user_img']
        user_email = session['user_email']
        user_pass = session['user_pass']
        cursor.execute("""SELECT posts.post_id, posts.post_title, posts.post_desc, posts.post_date, user.user_name, user.user_img FROM posts INNER JOIN user ON posts.user_id=user.user_id ORDER BY 1 DESC;""")
        posts = cursor.fetchall()
        
        
        return render_template('home.html',name=user_name,uimg=user_img,mail=user_email,upass=user_pass,posts=posts)
    else:    
         return render_template('login.html')
    
    
@app.route('/signup')
def signup():
    name=request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('password')
    
    return render_template('signup.html')
    
    
@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/social')
    
    
    
    
@app.route('/', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    
    cursor.execute("""SELECT * FROM user WHERE user_email LIKE '{}' AND user_pass LIKE '{}' """.format(email,password))
    
    users = cursor.fetchall()
    
    if len(users)>0:
        session['user_id'] = users[0][0]
        session['user_name'] = users[0][1]
        session['user_img'] =  users[0][4]
        session['user_email'] = users[0][2]
        session['user_pass'] = users[0][3]
        return redirect('/social')
    else:
        return redirect('/social')
        
        
        


        
    
    
@app.route('/add', methods=['POST'])
def add_user():
    user_name = request.form.get('user_name')
    user_email = request.form.get('user_email')
    user_password = request.form.get('user_password')
    user_image = 'default.jpg'
    
    cursor.execute("""INSERT INTO user (user_name, user_email, user_pass, user_img)  VALUES('{}', '{}', '{}', '{}') """.format(user_name,user_email,user_password,user_image))
    
    conn.commit()
    
    cursor.execute("""SELECT * FROM user WHERE user_email LIKE '{}' """.format(user_email))
    new_user = cursor.fetchall()
    session['user_id'] = new_user[0][0]
    session['user_name'] = new_user[0][1]
    session['user_img'] =  new_user[0][4]
    session['user_email'] = new_user[0][2]
    session['user_pass'] = new_user[0][3]
    
    return redirect('/social')
    
    
    
    
    
    
    
    

    

        
        
            
    
    
    




@app.route('/myposts')
def myposts():
    if 'user_id' in session:
        user_name = session['user_name']
        user_email = session['user_email']
        user_pass = session['user_pass']
        user_img = session['user_img']
        user_id = session['user_id']
        cursor.execute("""SELECT posts.post_id, posts.post_title, posts.post_desc, posts.post_date, user.user_name, user.user_img FROM posts INNER JOIN user ON posts.user_id=user.user_id WHERE user.user_id LIKE '{}' ORDER BY 1 DESC;""".format(user_id))
        posts = cursor.fetchall()
        
        
        return render_template('mypost.html',user_name=user_name,user_email=user_email,user_pass=user_pass,user_img=user_img,posts=posts)
    else:    
         return redirect('/social')
         
         
         
         
         
      
         
@app.route('/deletepost/<int:id>')
def deletepost(id):
    if 'user_id' in session:
        cursor.execute("""SELECT * FROM posts WHERE post_id LIKE '{}' """.format(id))
        vusers = cursor.fetchall()
        vpostuserid = vusers[0][1]
        vuser_id = session['user_id']
        if vpostuserid == vuser_id:
           cursor.execute("""DELETE FROM posts WHERE post_id LIKE '{}' """.format(id))
           conn.commit() 
           
        else:
            return "<h5>you are not allowed to do this action</h5>"
        
        
         
        
        
        
        return redirect('/social/myposts')
        
    else:    
        return redirect('/social')   



    
    
@app.route('/post', methods=['POST'])
def add_post():
     if 'user_id' in session:
         title = request.form.get('title')
         desc = request.form.get('desc')
         user_id = session['user_id']
    
         cursor.execute("""INSERT INTO posts (user_id, post_title, post_desc, post_date) VALUES ('{}', '{}', '{}', now() ) """.format(user_id, title, desc))
    
         conn.commit()
         return redirect('/social')  
     else:    
         return redirect('/social')  
         
         
         
         
         



@app.route('/upduser', methods=['POST'])
def upd_user():
     if 'user_id' in session:
         upd_id = session['user_id']
         uimage = session['user_img']
         img = request.files['imgfile']
         
         if img:
            uimage = img.filename
            img_path = "static/" + img.filename
            img.save(img_path)
        
         
         
         upd_name = request.form.get('edit_name')
         upd_email = request.form.get('edit_email')
         upd_pass = request.form.get('edit_pass')
         updsql = "update user set user_name='{}', user_email='{}', user_pass='{}', user_img='{}' where user_id={} ".format(upd_name,upd_email,upd_pass,uimage,upd_id)
         cursor.execute(updsql)
         conn.commit()
         
         cursor.execute("""SELECT * FROM user WHERE user_id LIKE {} """.format(upd_id))
         upd_user = cursor.fetchall()
         session['user_id'] = upd_user[0][0]
         session['user_name'] = upd_user[0][1]
         session['user_img'] =  upd_user[0][4]
         session['user_email'] = upd_user[0][2]
         session['user_pass'] = upd_user[0][3]
         
        
         return redirect('/social')  
     else:    
         return redirect('/social')




         
  
  
   





   

@app.route('/singlepost/<int:id>')
def singlepost(id):
    if 'user_id' in session:

        user_id = session['user_id']
        cursor.execute("""SELECT * FROM user WHERE user_id LIKE {} """.format(user_id))
        user = cursor.fetchall()
        
        user_name = user[0][1]
        user_img = user[0][4]
        user_email = user[0][2]
        user_pass = user[0][3]
        
        cursor.execute("""SELECT posts.post_id, posts.post_title, posts.post_desc, posts.post_date, user.user_name, user.user_img FROM posts INNER JOIN user ON posts.user_id=user.user_id WHERE posts.post_id LIKE '{}' """.format(id))
    
        post = cursor.fetchall()
        
        cursor.execute("""SELECT comments.com_id, comments.comment, comments.com_time, user.user_name, user.user_img FROM comments INNER JOIN user ON comments.user_id = user.user_id WHERE post_id LIKE {}""".format(id))
        comm = cursor.fetchall()

        
        
        return render_template('single_post.html', user_id=user_id, user_img=user_img,user_name=user_name,user_email=user_email,user_pass=user_pass,post=post,comm=comm)    
    else:    
        return redirect('/social')
        
        
        
        




@app.route('/edit_post/<int:id>')
def edit_post(id):
    if 'user_id' in session:

        user_id = session['user_id']
        cursor.execute("""SELECT * FROM user WHERE user_id LIKE {} """.format(user_id))
        user = cursor.fetchall()
        
        user_name = user[0][1]
        user_img = user[0][4]
        user_email = user[0][2]
        user_pass = user[0][3]
        
        cursor.execute("""SELECT posts.post_id, posts.post_title, posts.post_desc, posts.post_date, user.user_name, user.user_img FROM posts INNER JOIN user ON posts.user_id=user.user_id WHERE posts.post_id LIKE '{}' """.format(id))
    
        post = cursor.fetchall()
        

        
        
        return render_template('edit_post.html', user_id=user_id, user_img=user_img,user_name=user_name,user_email=user_email,user_pass=user_pass,post=post)    
    else:    
        return redirect('/social')








@app.route('/update_post/<int:id>', methods=['POST'])
def upd_post(id):
     if 'user_id' in session:
         
         upd_title = request.form.get('edit_title')
         upd_desc = request.form.get('edit_desc')
         
         cursor.execute("""SELECT * FROM posts WHERE post_id LIKE '{}' """.format(id))
         vusers = cursor.fetchall()
         vpostuserid = vusers[0][1]
         vuser_id = session['user_id']
         
         if vpostuserid == vuser_id:
             updsql = "update posts set post_title ='{}', post_desc ='{}' where post_id= {} ".format(upd_title,upd_desc,id)
             cursor.execute(updsql)
             conn.commit() 
           
         else:
            return "<h5>you are not allowed to do this action</h5>"
         

         
         
         
        
         return redirect('/social/myposts')  
     else:    
         return redirect('/social')















        
        
        
        
        
        
        
        
        
        
@app.route('/entercomment/<int:id>', methods=['POST'])
def entercomment(id):
    if 'user_id' in session:

        user_id = session['user_id']
        id = id
        
        addcomment = request.form.get('comment')
        
        cursor.execute("""INSERT INTO comments (post_id, user_id, comment, com_time) VALUES({}, {}, '{}', NOW()) """.format(id, user_id, addcomment))
        conn.commit()
        
        cursor.execute("""SELECT * FROM user WHERE user_id LIKE {} """.format(user_id))
        user = cursor.fetchall()
        
        user_name = user[0][1]
        user_img = user[0][4]
        
        cursor.execute("""SELECT posts.post_id, posts.post_title, posts.post_desc, posts.post_date, user.user_name, user.user_img FROM posts INNER JOIN user ON posts.user_id=user.user_id WHERE posts.post_id LIKE '{}' """.format(id))
    
        post = cursor.fetchall()
        
        cursor.execute("""SELECT comments.com_id, comments.comment, comments.com_time, user.user_name, user.user_img FROM comments INNER JOIN user ON comments.user_id = user.user_id WHERE post_id LIKE {}""".format(id))
        comm = cursor.fetchall()

        
        
        return render_template('single_post.html', user_id=user_id, user_img=user_img,user_name=user_name,post=post, comm=comm)   
        
        
    else:    
        return redirect('/social')        
        
        
        
        
        













  
  
  
  
    
    
    
    
         
    
    
 
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/social')
    
    
    
    
    
    
    
if __name__ == '__main__':
    app.run(debug=True)
