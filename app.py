from flask import Flask,redirect,request,g,render_template,jsonify
import sqlite3
from database import get_db

app = Flask(__name__)
api_username = 'admin'
api_password = 'password'

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()


@app.route('/member',methods=['GET'])
def get_members():

    db = get_db()
    members_cur = db.execute("select id,name,email,level from members")
    members_res = members_cur.fetchall()
    values = []
    for x in members_res:
        dict = {}
        dict['id'] = x['id']
        dict['name'] = x['name']
        dict['email'] = x['email']
        dict['level'] = x['level']
        values.append(dict)


    return jsonify({'members':values})

@app.route('/member/<int:member_id>',methods=['GET'])
def get_member(member_id):
    db = get_db()
    member_cur = db.execute("select id,name,email,level from members where id =?",[member_id])
    member_res = member_cur.fetchone()
    return jsonify({'member':{'id':member_res['id'], 'name':member_res['name'], 'email':member_res['email'],'level':member_res['level']}})

@app.route('/member',methods=['POST'])
def add_member():
    try:
        username = request.authorization.username
        password = request.authorization.password
    except:
        return jsonify({'message':'Authentication Failed'}),403


    if username!=api_username or password!=api_password:
        return jsonify({'message':'Authentication Failed'}),403
    new_member_data = request.get_json()
    name = new_member_data['name']
    email = new_member_data['email']
    level = new_member_data['level']

    db = get_db()
    db.execute("insert into members (name,email,level) values (?,?,?)",[name,email,level])
    db.commit()

    member_cur = db.execute("select id,name,email,level from members where name=?",[name])
    member_res = member_cur.fetchone()

    return jsonify({'id':member_res['id'],'name':member_res['name'],'email':member_res['email'],'level':member_res['level']})

@app.route('/member/<int:member_id>',methods=['PUT','PATCH'])
def edit_member(member_id):
    try:
        username = request.authorization.username
        password = request.authorization.password
    except:
        return jsonify({'message':'Authentication Failed'}),403


    if username!=api_username or password!=api_password:
        return jsonify({'message':'Authentication Failed'}),403
    member_data = request.get_json()
    name = member_data['name']
    email = member_data['email']
    level = member_data['level']

    db = get_db()
    db.execute("update members set name=?, email=?, level=? where id=?",[name,email,level,member_id])
    db.commit()

    member_cur = db.execute("select id,name,email,level from members where id=?",[member_id])
    member_res = member_cur.fetchone()
    return jsonify({'member':{'id':member_res['id'], 'name':member_res['name'], 'email':member_res['email'],'level':member_res['level']}})

@app.route('/member/<int:member_id>',methods=['DELETE'])
def delete_member(member_id):
    try:
        username = request.authorization.username
        password = request.authorization.password
    except:
        return jsonify({'message':'Authentication Failed'}),403


    if username!=api_username or password!=api_password:
        return jsonify({'message':'Authentication Failed'}),403
    db = get_db()
    db.execute("delete from members where id=?",[member_id])
    db.commit()
    return jsonify({'message':'deleted member {}'.format(member_id)})

if __name__ == '__main__':
    app.run(debug=True)
