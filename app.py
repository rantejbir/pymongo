from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work
from bson.errors import InvalidId # For catching InvalidId exception for ObjectId
import os

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)    #Configure the connection to the database
db = client.camp2016    #Select the database
allList = db.todo #Select the collection

app = Flask(__name__)



def redirect_url():
	return request.args.get('next') or \
		request.referrer or \
		url_for('index')
		
@app.route("/")
@app.route("/list")
def lists ():
	#Display the all things
	todos_l = list(allList.find({"category": False}))
	todos_ls = list(allList.find({"category": True}))
	a1="active"
	return render_template('index.html',a1=a1,todos=todos_l,todos2=todos_ls)


@app.route("/page2")
def second_page():
	a1="active"
	return render_template('Add.html',a1=a1)

@app.route("/action", methods=['POST'])
def action ():
	#Adding a Name
	name=request.values.get("name")
	desc=request.values.get("desc")
	gender=request.values.get("gender")
	allList.insert_one({ "name":name, "desc":desc,"gender":gender,"category":False})
	return redirect("/list")


@app.route("/action2", methods=['POST'])
def action2 ():
	#Adding a Job
	name=request.values.get("name")
	Company=request.values.get("Company")
	Manager=request.values.get("Manager")
	desc=request.values.get("desc")
	demand=request.values.get("demand")
	allList.insert_one({ "Job":name, "desc":desc,"demand":demand,"Company":Company,"Manager":Manager,"category":True})
	return redirect("/list")

@app.route("/remove")
def remove ():
	#Deleting a name 
	key=request.values.get("_id")
	allList.delete_one({"_id":ObjectId(key)})
	return redirect("/list")


@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=allList.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task)

@app.route("/update2")
def update2 ():
	id=request.values.get("_id")
	task=allList.find({"_id":ObjectId(id)})
	return render_template('update2.html',tasks=task)


@app.route("/action4", methods=['POST'])
def action4 ():
	#Updating a job
	name=request.values.get("name")
	Company=request.values.get("Company")
	Manager=request.values.get("Manager")
	desc=request.values.get("desc")
	demand=request.values.get("demand")
	id=request.values.get("_id")
	allList.update_one({"_id":ObjectId(id)}, {'$set':{"Job":name, "desc":desc,"demand":demand,"Company":Company,"Manager":Manager}})
	return redirect("/list")

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a name
	name=request.values.get("name")
	desc=request.values.get("desc")
	gender=request.values.get("gender")
	id=request.values.get("_id")
	allList.update_one({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc,"gender":gender}})
	return redirect("/list")	


if __name__ == "__main__":
	env = os.environ.get('FLASK_ENV', 'development')
	port = int(os.environ.get('PORT', 5000))
	debug = False if env == 'production' else True
	app.run(debug=True)
	app.run(port=port, debug=debug)
