import os
import sys
import json

from flask import Flask, request, abort, jsonify
from flask_cors import CORS

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from migration.load import load_data
from database.connection import run_query
from database.queries import employees_by_quarter, more_than_the_mean_hired_employees
from database.backup import backup, restore
from migration.exceptions import (
    DuplicateDataError,
    EmptyDataFrameError,
    InvalidModelError,
    IncompatibleAvroFileError,
)
from utils.utils import store_file


app = Flask(__name__)
CORS(app)


@app.route("/migrate", methods=["POST"])
def migrate():
    if request.method == "POST":
        if "file" not in request.files:
            return abort(400, "Missing file")
        data = request.form.to_dict().get("data")
        if data:
            entity = json.loads(data).get("entity")
            if not entity:
                return abort(400, "Missing entity key in payload")

            file = request.files["file"]
            file_path = store_file(file)
            try:
                rowcount = load_data(file_path, entity)
                return (
                    jsonify(
                        {"message": f"Inserted {rowcount} new rows to {entity} table"}
                    ),
                    201,
                )

            except DuplicateDataError as e:
                return (
                    jsonify(
                        {"ids": e.duplicates, "entity": e.entity, "message": e.message}
                    ),
                    409,
                )


@app.route("/backup", methods=["POST"])
def backup_handler():
    data = request.form.to_dict().get("data")
    if data:
        entity = json.loads(data).get("entity")
        if not entity:
            return abort(400, "Missing entity key in payload")
        try:
            file_location = backup(entity)
            return jsonify({"file_location": file_location}), 200
        except EmptyDataFrameError:
            return abort(400, f"Table {entity} is empty")
        except InvalidModelError:
            return abort(400, f"Entity name {entity} is not valid")
    else:
        return abort(400, "Missing data key in payload")


@app.route("/restore", methods=["POST"])
def restore_handler():
    if request.method == "POST":
        if "file" not in request.files:
            return abort(400, "Missing file")
        data = request.form.to_dict().get("data")
        if data:
            entity = json.loads(data).get("entity")
            if not entity:
                return abort(400, "Missing entity key in payload")

            file = request.files["file"]
            filename = store_file(file)
            try:
                row_count = restore(filename, entity)
                return (
                    jsonify(
                        {"message": f"Restored {row_count} rows to {entity} table"}
                    ),
                    201,
                )

            except DuplicateDataError as e:
                return (
                    jsonify(
                        {"ids": e.duplicates, "entity": e.entity, "message": e.message}
                    ),
                    409,
                )
            except IncompatibleAvroFileError as e:
                return (
                    jsonify({"message": e.message}),
                    400,
                )


@app.route("/employeesbyquarter/<year>", methods=["get"])
def employees_by_quarter_handler(year):
    query = employees_by_quarter(year)
    result = run_query(query)

    rows = result.fetchall()
    columns = result.keys()
    data = [dict(zip(columns, row)) for row in rows]

    return jsonify({"data": data}), 200


@app.route("/morethanthemean/<year>", methods=["GET"])
def more_than_the_mean_hired_employees_handler(year):
    query = more_than_the_mean_hired_employees(year)
    result = run_query(query)

    rows = result.fetchall()
    columns = result.keys()
    data = [dict(zip(columns, row)) for row in rows]

    return jsonify({"data": data}), 200
