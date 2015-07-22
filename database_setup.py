from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Users(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	picture = Column(String(250))

class Categories(Base):
	__tablename__ = 'categories'   
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	
	@property
	def serialize(self):
	
		return {
			'id'        : self.id,
			'name'        : self.name,
		}
	
	
		
class Subcategories(Base):
	__tablename__ = 'subcategories'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	category_id = Column(Integer,ForeignKey('categories.id'))
	parentCategory = relationship(Categories)
	
	@property
	def serialize(self):
	
		return {
			'id'        : self.id,
			'name'        : self.name,
			'category_id'		: self.category_id
		}
	
 
class Items(Base):
	__tablename__ = 'items'
	id = Column(Integer, primary_key = True)
	title = Column(String(80), nullable = False)
	description = Column(String(250))
	picture = Column(String(250))
	category_id = Column(Integer,ForeignKey('categories.id'))
	category = relationship(Categories)
	subcategory_id = Column(Integer,ForeignKey('subcategories.id'))
	subcategory = relationship(Subcategories)
	
	@property
	def serialize(self):
	
		return {
			'id'         : self.id,
			'title'         : self.title,
			'description'         : self.description,
		}	

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)