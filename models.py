import json
from datetime import datetime
from main import db


class Book(db.Document):
	book_name = db.StringField()
	category = db.StringField()
	rent_per_day = db.IntField()
	def to_json(self):
		return {"book_name":self.book_name,
				"category":self.category,
				"rent_per_day":self.rent_per_day}	



class BookIssued(db.Document):
	person_name = db.StringField()
	Isissue = db.BooleanField()
	IsReturn = db.BooleanField()
	book = db.ReferenceField(Book)
	action_data = db.DateTimeField()
	return_date = db.DateTimeField()
	def to_json(self):
		print((self.action_data.date()-self.return_date.date()).days)
		return {"person_name":self.person_name,"IsReturn":self.IsReturn,"Isissue":self.Isissue,"book":self.book,"action_data":self.action_data,"return_date":self.return_date}
	def Rent(self):
		if self.IsReturn == True:
			total_rent=(self.action_data.date()-self.return_date.date()).days*self.book.rent_per_day
		else:
			total_rent=(self.action_data.date()-self.datetime.now().date()).days*self.book.rent_per_day
		return {"Rent":total_rent}