import os
import sys
import json

from flask import Flask, request, abort, jsonify
from flask_cors import CORS

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from migration.load import load_data
from migration.exceptions import DuplicateDataError
from utils.utils import store_file


app = Flask(__name__)
CORS(app)


@app.route("/migrate", methods=['POST'])
def migrate():
    import pdb; pdb.set_trace()

    if request.method == 'POST':
        if 'file' not in request.files:
            return abort(400, "Missing file")
        data = request.form.to_dict().get("data")
        if data:
            entity = json.loads(data).get("entity")
            if not entity:
                return abort(400, "Missing entity key in payload")
        
        file = request.files['file']
        file_path = store_file(file)
        try:
            rowcount = load_data(file_path, entity)
            return jsonify({"message": f"Inserted {rowcount} new rows to {entity} table"}), 201

        except DuplicateDataError as e:
            return jsonify({"ids": e.duplicates, "entity": e.entity, "message": e.message}), 409

