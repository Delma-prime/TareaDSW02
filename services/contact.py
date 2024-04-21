from flask import Blueprint, request, jsonify
from model.contact import Contact
from utils.db import db

contacts = Blueprint('contacts', __name__)

@contacts.route('/contactos/v1', methods = ['GET'])
def getMensaje():
    result = {}
    result["data"] = 'flask-crud-backend'
    return jsonify(result)

@contacts.route('/contactos/v1/listar', methods = ['GET'])
def getContactos():
    result = {}
    contactos = Contact.query.all() 
    result["data"] = contactos
    result["status_cod"] = 200 
    result["status_msg"] = "Contacts were recovery succesfully..."
    return jsonify(result), 200

@contacts.route('/contactos/<int:id>', methods = ['GET'])
def getContacto(id):
    result = {}
    contactos = Contact.query.get(id)
    result["data"] = contactos
    result["status_cod"] = 200 
    result["status_msg"] = "Contacts were recovery succesfully..."
    return jsonify(result), 200



@contacts.route('/contactos/v1/insert', methods = ['POST'])
def insert():
    result = {}
    body = request.get_json()
    fullname = body.get('fullname')
    email = body.get('email')
    phone = body.get('phone')
    
    if not fullname or not email or not phone:
        result["status_cod"] = 400 
        result["status_msg"] = "Data is missing"
        return jsonify(result), 400
    
    contacto = Contact(fullname, email, phone)
    db.session.add(contacto) 
    db.session.commit()
    result["data"] = contacto
    result["status_cod"] = 201 
    result["status_msg"] = "Data was created"
    return jsonify(result), 201

@contacts.route('/contactos/v1/update', methods = ['POST'])
def update():
    result = {}
    body = request.get_json()
    id = body.get('id')
    fullname = body.get('fullname')
    email = body.get('email')
    phone = body.get('phone')
    
    #if data is missing
    if not id or not fullname or not email or not phone:
        result["status_cod"] = 400 
        result["status_msg"] = "Data is missing"
        return jsonify(result), 400
    
    contacto = Contact.query.get(id)
    
    if not contacto:
        result["status_cod"] = 400 
        result["status_msg"] = "ID does not exist"
        return jsonify(result), 400
    
    contacto.fullname = fullname
    contacto.email = email
    contacto.phone = phone
    db.session.commit()
    
    result["data"] = contacto
    result["status_cod"] = 202 
    result["status_msg"] = "Data was modified"
    return jsonify(result), 202

@contacts.route('/contactos/v1/delete', methods = ['DELETE'])
def delete():
    result = {}
    body = request.get_json()
    id = body.get('id')    

    if not id:
        result["status_cod"] = 400 
        result["status_msg"] = "ID must be provided"
        return jsonify(result), 400
    
    contacto = Contact.query.get(id)
    
    if not contacto:
        result["status_cod"] = 400
        result["status_msg"] = "ID does not exist"
        return jsonify(result), 400
    
    db.session.delete(contacto) 
    db.session.commit() 
    
    result["data"] = contacto
    result["status_cod"] = 200
    result["status_msg"] = "Data was deleted"
    return jsonify(result), 200