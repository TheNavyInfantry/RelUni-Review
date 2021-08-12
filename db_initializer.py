from reluni_review import db, create_app

try:
    db.create_all(app=create_app())
    print("Successful!")

except:
    print("Failed!")


