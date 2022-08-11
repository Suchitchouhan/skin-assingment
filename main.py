from flask import Flask,request, jsonify
from flask_mongoengine import MongoEngine
import json
from datetime import datetime
from models import *

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'skinnydb',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)
#app.add_url_rule('/', 'index', index_dep)


	


@app.errorhandler
@app.route("/",methods=["GET"])
def index():
	return "<h3> Hi Welcome to Skinny assignment </h3>"




@app.errorhandler
@app.route("/AddBook",methods=['POST'])
def AddBook():
	record = json.loads(request.data)
	book_name = record['book_name']
	category = record['category']
	rent_per_day = record['rent_per_day']
	if Book.objects(book_name=book_name).first():
		return jsonify({"msg":"Book already exists"}),400
	else:
		book = Book(book_name=book_name,category=category,rent_per_day=rent_per_day)
		book.save()
		return jsonify(book.to_json()),200


@app.errorhandler
@app.route("/GetAllBook",methods=['GET'])
def GetAllBook():
	books = Book.objects.all()
	return jsonify(books),200



@app.errorhandler
@app.route("/GetBookByName",methods=['GET'])
def GetBookByName():
	book_name = request.args.get('book_name')
	book = Book.objects(book_name=book_name)
	return jsonify(book),200



@app.errorhandler
@app.route("/UpdateBook",methods=['PUT'])
def UpdateBook():
	record = json.loads(request.data)
	book_name = record['book_name']
	category = record['category']
	rent_per_day = record['rent_per_day']
	book = Book.objects(book_name=book_name).first()
	if not book:
		return jsonify({'error': 'data not found'}),400
	else:
		book.update(book_name=book_name,category=category,rent_per_day=rent_per_day)
		return jsonify(book.to_json()),200




@app.errorhandler
@app.route("/DeleteBookByName",methods=['DELETE'])
def DeleteBookByName():
	book_name = request.args.get('book_name')
	book = Book.objects(book_name=book_name)
	if not book:
		return jsonify({'error': 'data not found'}),400
	else:		
		book.delete()
		return jsonify({"msg":"Book has been deleted successfully"}),200


@app.errorhandler
@app.route("/GetBookByRange",methods=['GET'])
def GetBookByRange():
	start_limit = request.args.get("start_limit")
	end_limit = request.args.get("end_limit")
	book = Book.objects(rent_per_day__lt=int(end_limit),rent_per_day__gt=int(start_limit))
	return jsonify(book),200


@app.errorhandler
@app.route("/IssueBook",methods=['POST'])
def IssueBook():
	record = json.loads(request.data)
	person_name = record['person_name']
	book_name = record['book_name']
	book = Book.objects(book_name=book_name).first()
	if not book:
		return jsonify({"error":"Book is not exist"}),400
	else:
		if BookIssued.objects(person_name=person_name,Isissue=True,book=book).first():
			return jsonify({"error":"Book is already Issued"}),400
		else:	
			bookissue = BookIssued(person_name=person_name,Isissue=True,IsReturn=False,book=book)
			bookissue.action_data=datetime.now()
			bookissue.save()
			return jsonify({"msg":"Book has been successfully Issued","BookIssued":bookissue.to_json()}),200



@app.errorhandler
@app.route("/ReturnBook",methods=['POST'])
def ReturnBook():
	record = json.loads(request.data)
	person_name = record['person_name']
	book_name = record['book_name']
	book = Book.objects(book_name=book_name).first()
	if not book:
		return jsonify({"error":"Book is not exist"}),400
	else:
		BookIssuedO=BookIssued.objects(person_name=person_name,Isissue=True,book=book).first()
		if not BookIssuedO:
			return jsonify({"error":"Book is not Issued"}),400
		else:	
			BookIssuedO.IsReturn=True
			BookIssuedO.return_date=datetime.now()		
			BookIssuedO.save()
			return jsonify({"msg":"Book has been successfully Issued","BookIssued":BookIssuedO.to_json()}),200



@app.errorhandler
@app.route("/BookIssuedToPerson",methods=['POST'])
def BookIssuedToPerson():
	record = json.loads(request.data)
	person_name = record['person_name']
	BookIssuedO=BookIssued.objects(person_name=person_name,Isissue=True,IsReturn=False)
	return jsonify({"BookIssued":BookIssuedO,"count":BookIssuedO.count()}),200


@app.errorhandler
@app.route("/BookIssuedToPersonNotReturn",methods=['POST'])
def BookIssuedToPersonNotReturn():
	record = json.loads(request.data)
	person_name = record['person_name']
	BookIssuedO=BookIssued.objects(person_name=person_name,Isissue=True,IsReturn=True)
	print(BookIssuedO.count())
	return jsonify({"BookIssued":BookIssuedO,"count":BookIssuedO.count()}),200




@app.errorhandler
@app.route("/TotalBookRent",methods=['GET'])
def TotalBookRent():
	bo=BookIssued.objects(IsReturn=True)
	tmp_list=[]
	for x in bo:
		tmp_list.append(x.Rent()['Rent'])
	print(tmp_list)	
	return jsonify({"Total Rent":sum(tmp_list)})

if __name__ == "__main__":
	app.run(debug=True)