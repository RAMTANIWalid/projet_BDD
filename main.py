import random
from flask import Flask, flash, render_template, request, session, redirect, url_for, session
from datetime import datetime
import db
from passlib.context import CryptContext

app = Flask(__name__)
# create route to login
@app.route("/login")
def login():
    return render_template("index.html")

@app.route("/create_new_account", methods=["POST"])
def create_acount():
    if request.method == 'POST':
        firstname = request.form['Firstname']
        name = request.form['Name']
        mail = request.form['Email']
        tel = request.form['Phone']
        mdp = request.form['Password']
        sexe = request.form['Sexe']
        country = request.form["Country"]
        role = request.form["Role"]
        if firstname and name and mail and tel and mdp and sexe and country and role:
            if len(tel) >= 9:
                conn = db.connect()
                password_ctx = CryptContext(schemes=['bcrypt'])
                hash_pw = password_ctx.hash(mdp)
                if role == "Manager":       
                    with conn.cursor() as cur:
                        # Check if the email already exists in the 'gerant' table
                        cur.execute('SELECT * FROM gerant WHERE mailGer = %s;', (mail,))
                        existing_manager = cur.fetchone()  # Use fetchone to get the result

                        if existing_manager is None:  # No manager found with the same email
                            # Insert new manager into the 'gerant' table
                            with conn.cursor() as inser:
                                tel = country + tel
                                print(tel)
                                inser.execute(
                                    "INSERT INTO gerant(nomGer, prenomGer, mailGer, telGer, mdpGer, sexe) VALUES (%s, %s, %s, %s, %s, %s);",
                                    (name, firstname, mail, tel, hash_pw, sexe)
                                )
                            conn.close()
                            return redirect(url_for("login"))
                        else:
                            conn.close()
                            flash("An account with this email already exists.", "Error")
                            return redirect("error")
                elif role == "Employe":
                    with conn.cursor() as cur:
                        # Check if the email already exists in the 'gerant' table
                        cur.execute('SELECT * FROM employe WHERE mailEmp = %s;', (mail,))
                        existing_manager = cur.fetchone()  # Use fetchone to get the result

                        if existing_manager is None:  # No manager found with the same email
                            with conn.cursor() as inser:
                                tel = country + tel
                                inser.execute(
                                    "INSERT INTO employe (nomEmp, prenomEmp, mailEmp, telEmp, mdpEmp, sexe) VALUES (%s, %s, %s, %s, %s, %s);",
                                    (name, firstname, mail, tel, hash_pw, sexe)
                                )
                            conn.close()
                            return redirect(url_for("login"))
                        else:
                            conn.close()
                            flash("An account with this email already exists.", "Error")
                            return redirect("error")
                elif role == "Client":
                    with conn.cursor() as cur:
                        # Check if the email already exists in the 'gerant' table
                        cur.execute('SELECT * FROM client WHERE mailCli = %s;', (mail,))
                        existing_manager = cur.fetchone()  

                        if existing_manager is None:  # No manager found with the same email
                            with conn.cursor() as inser:
                                tel = country + tel
                                inser.execute(
                                    "INSERT INTO client (nomCli, prenomCli, mailCli, telCli, mdpCli, sexe) VALUES (%s, %s, %s, %s, %s, %s);",
                                    (name, firstname, mail, tel, hash_pw, sexe)
                                )
                            conn.close()
                            return redirect(url_for("login"))
                        else:
                            conn.close()
                            flash("An account with this email already exists.", "Error")
                            return redirect("error")
    conn.close()
    return redirect(url_for("manager"))
             
# create route to login_info
@app.route("/login_account", methods=["POST"])
def login_account():
    if request.method == 'POST':
        mail = request.form['Email']
        mdp = request.form['Password']
        role = request.form["Role"]
        if role and mdp and mail:
            conn = db.connect()
            password_ctx = CryptContext(schemes=['bcrypt'])
            with conn.cursor() as cur:
                if role == "Manager":
                    cur.execute("SELECT * FROM gerant WHERE mailGer = %s", (mail,))
                    existing_manager = cur.fetchone()
                    if existing_manager is None:
                        flash("This account doest not exist.", "Error")
                        conn.close()
                        return redirect("error")               
                    if password_ctx.verify(mdp, existing_manager.mdpger):
                        session.user = existing_manager
                        conn.close()
                        return redirect(url_for("manager"))
                elif role == "Employe":
                    cur.execute("SELECT * FROM employe WHERE mailEmp = %s", (mail,))
                    existing_manager = cur.fetchone()
                    if existing_manager is None:
                        flash("This account doest not exist.", "Error")
                        conn.close()
                        return redirect("error")              
                    if password_ctx.verify(mdp, existing_manager.mdpemp):
                        session.user = existing_manager
                        conn.close()
                        return redirect(url_for("manager"))
                elif role == "Client":
                    cur.execute("SELECT * FROM client WHERE mailCli = %s", (mail,))
                    existing_manager = cur.fetchone()
                    if existing_manager is None:
                        flash("This account doest not exist.", "Error")
                        conn.close()
                        return redirect("error")               
                    if password_ctx.verify(mdp, existing_manager.mdpcli):
                        session.user = existing_manager
                        conn.close()
                        return redirect(url_for("manager"))
    flash("This account doest not exist.", "Error")
    return redirect("error") 
# create route to register
@app.route("/register")
def register():
    return render_template("register.html")
# create route manager main page
@app.route("/manager")
def manager():
    composant = ["Mouse", "heyrizhfuiahh hfhehhzudhe hfuhehf zhfhzuur hzurghd hzyyhz hzhyhge","gohan.jpeg"]
    return render_template("profile.html", composants = [composant for i in range(10)])
# create route product main page
@app.route("/product")
def product():
    return render_template("produit.html")

# create route product main page
@app.route("/shop")
def shop():
    return render_template("magasin.html")


@app.route("/employeshifts")
def employeshifts():
    return render_template("shiftemployee.html")


#error route
@app.route("/error")
def show_error_page():
    return render_template("error.html")

if __name__ == '__main__':
    app.secret_key = 'asta'
    app.run()