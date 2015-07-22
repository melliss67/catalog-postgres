from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Categories, Subcategories, Items, Users

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# User1 = Users(name="Mariah Ellis", email="mriahels@gmail.com",
#             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
# session.add(User1)
# session.commit()

Category1 = Categories(name="Screws")
session.add(Category1)

Subcategory1 = Subcategories(name="Machine Screws",parentCategory=Category1)
session.add(Subcategory1)

Item1 = Items(title="1/4\"-20 x 5\" Phillips Drive Flat Head Grade 18-8 Stainless Steel",description="1/4\"-20 x 5\" Phillips Drive Flat Head Grade 18-8 Stainless Steel Machine Screw",category=Category1,subcategory=Subcategory1)
Item2 = Items(title="1/4\"-20 x 10\" Phillips Drive Flat Head Grade 18-8 Stainless Steel",description="1/4\"-20 x 5\" Phillips Drive Flat Head Grade 18-8 Stainless Steel Machine Screw",category=Category1,subcategory=Subcategory1)
session.add(Item1)
session.add(Item2)

Subcategory2 = Subcategories(name="Sheet Metal Screws",parentCategory=Category1)
session.add(Subcategory2)

Item1 = Items(title="#8-15 x 1\" Phillips Drive Flat Head Zinc Finish Type A Point",description="#8-15 x 1\" Phillips Drive Flat Head Zinc Finish Type A Point Sheet Metal Screw",category=Category1,subcategory=Subcategory2)
Item2 = Items(title="#8-15 x 2\" Phillips Drive Flat Head Zinc Finish Type A Point",description="#8-15 x 1\" Phillips Drive Flat Head Zinc Finish Type A Point Sheet Metal Screw",category=Category1,subcategory=Subcategory2)
Item3 = Items(title="#8-15 x 3\" Phillips Drive Flat Head Zinc Finish Type A Point",description="#8-15 x 1\" Phillips Drive Flat Head Zinc Finish Type A Point Sheet Metal Screw",category=Category1,subcategory=Subcategory2)
session.add(Item1)
session.add(Item2)
session.add(Item3)

Category2 = Categories(name="Bolts")
session.add(Category2)

Subcategory3 = Subcategories(name="Carriage",parentCategory=Category2)
session.add(Subcategory3)

Item1 = Items(title="3/8\"-16 x 3\" Zinc Finish ASTM A307 Grade A Round Head",description="3/8\"-16 x 3\" Zinc Finish ASTM A307 Grade A Round Head Carriage Bolt",category=Category2,subcategory=Subcategory3)
Item2 = Items(title="3/8\"-16 x 1\" Zinc Finish ASTM A307 Grade A Round Head Carriage Bolt",description="3/8\"-16 x 1\" Zinc Finish ASTM A307 Grade A Round Head Carriage Bolt",category=Category2,subcategory=Subcategory3)
session.add(Item1)
session.add(Item2)

Subcategory4 = Subcategories(name="Flange",parentCategory=Category2)
session.add(Subcategory4)

Item1 = Items(title="5/16\"-18 x 3/4\" Hex Head Zinc Finish Case Hardened Steel",description="5/16\"-18 x 3/4\" Hex Head Zinc Finish Case Hardened Steel Serrated Flange Bolt",category=Category2,subcategory=Subcategory4)
Item2 = Items(title="1/2\"-13 x 2\" Hex Head Grade 8 Phosphate and Oil Finish Steel",description="1/2\"-13 x 2\" Hex Head Grade 8 Phosphate and Oil Finish Steel Flange Bolt",category=Category2,subcategory=Subcategory4)
Item3 = Items(title="3/8\"-16 x 1-1/4\" Hex Head Grade 5 Yellow Zinc Finish Steel",description="3/8\"-16 x 1-1/4\" Hex Head Grade 5 Yellow Zinc Finish Steel Flange Bolt",category=Category2,subcategory=Subcategory4)
Item4 = Items(title="1/2\"-13 x 1\" Hex Head Zinc Finish Case Hardened Steel",description="1/2\"-13 x 1\" Hex Head Zinc Finish Case Hardened Steel Serrated Flange Bolt",category=Category2,subcategory=Subcategory4)
session.add(Item1)
session.add(Item2)
session.add(Item3)
session.add(Item4)

session.commit()