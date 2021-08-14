# RelUni Review

---

* RelUni Review is a web application that stands for reliable university reviews and where people can share their reviews about universities.


* It is written with Python & Flask Framework, used MySQL with SQLAlchemy (ORM - Object-Relational Mapping) as database.

---

## Project Status

RelUni Review is still under heavy development. There can be breaking changes, but I am trying to keep them as minimum as possible.

---

## Requirements

* Python 3.9


* Other required packages in requirements.txt

---

## Run Locally

* Clone the project

```bash
$ git clone https://github.com/TheNavyInfantry/RelUni-Review.git
```

* Go to the project directory

```bash
$ cd RelUni-Review
```

* Install `virtualenv`

```bash
$ pip3 install virtualenv
```

* Create a `venv`

```bash
$ virtualenv venv
```

* Activate created `venv`

```bash
$ source venv/bin/activate
```

* Install `requirements.txt`

```bash
$ (venv) pip3 install -r requirements.txt
```

* Create a database scheme and Run `db_initializer.py`

```bash
$ (venv) python db_initializer.py
```

* Create a `config.yml` file under RelUni-Review folder and insert personal values in it.
  **(See the example config.yml at the end of the document.)**


* Setup Flask

```bash
$ (venv) export FLASK_APP=app.py

$ (venv) export FLASK_DEBUG=True
```

* Start the server

```bash
$ (venv) flask run
```

* This server will start on port 5000 by default. You can change this in app.py by changing the following line to this

```bash
if __name__ == "__main__":
    app.run(debug=True, port=<desired port>)
```
  
`Example config.yml for this project:`
```bash
database:
  host: ''
  user: ''
  password: ''
  db: ''
  port: ''

secret_key: ''

mail_username: ''

mail_password: ''

mail_sender: ''
```
