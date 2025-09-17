from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required

app=Flask(__name__)
app.config["JWT_SECRET_KEY"]="super-secret-key"
jwt=JWTManager(app)

ECART=[
    {"id": 1, "item": "kurti with pant","price": 500},
    {"id": 2, "item": "jegin with shirt","price": 450},
    {"id": 3, "item": "scart with tees","price": 400},
    {"id": 4, "item": "salwar", "price": 300}
]

@app.route('/ecart', methods=['GET'])
def ecart():
    return jsonify({"ecart": ECART})

@app.route('/order', methods=['POST'])
@jwt_required()
def order():
    data=request.get_json()
    id=data.get('id')
    item=next((i for i in ECART if i["id"]==id),None)
    if not item:
        return jsonify({"msg": "Item not found"})
    return jsonify({"msg": "Order placed successfully", "item":item})

if __name__ == "__main__":

    app.run(debug=True, port=5001)
