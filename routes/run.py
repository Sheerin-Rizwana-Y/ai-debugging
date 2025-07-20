import subprocess
from flask import Blueprint, request, jsonify
from flask_login import login_required
import tempfile
import os

bp = Blueprint("run", __name__)

@bp.route("/run", methods=["POST"])
@login_required
def run_code():
    code = request.get_json().get("code", "")
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(code.encode())
            temp_file.flush()
            output = subprocess.check_output(["python3", temp_file.name], stderr=subprocess.STDOUT, timeout=3)
            result = output.decode().strip()
        os.unlink(temp_file.name)
    except subprocess.CalledProcessError as e:
        result = e.output.decode()
    except Exception as ex:
        result = str(ex)

    return jsonify({"output": result})
