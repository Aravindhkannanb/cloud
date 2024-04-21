from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate("account.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "fir-curd-90710.appspot.com"
})
app = Flask(__name__)
db = firestore.client()
user = db.collection("Users")
bucket = storage.bucket()

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        id = request.form.get("id")
        user.document(email).set(
            {
                "name": name,
                "email": email,
                "id": id
            }
        )
        return redirect(url_for("home"))
    docs = user.get()
    lists = []
    for i in docs:
        lists.append(i.to_dict())
    return render_template("index.html", data=lists)

@app.route("/update/<email>", methods=["POST", "GET"])
def update(email):
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        id = request.form.get("id")
        user.document(email).update(
            {
                "name": name,
                "email": email,
                "id": id
            }
        )
        return redirect(url_for("home"))
    doc = user.document(email).get()
    return render_template("update.html", data=doc.to_dict())

@app.route("/delete/<email>")
def delete(email):
    user.document(email).delete()
    return redirect(url_for("home"))

@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        file = request.files["myfile"]
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
