from datetime import datetime
import os


from werkzeug.utils import secure_filename


base_dir =  os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_FOLDER = os.path.join(base_dir, "migration", "files")
ALLOWED_EXTENSIONS = ["csv"]



def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def store_file(file_obj):
    if file_obj.filename == '':
        return False
    if file_obj and allowed_files(file_obj.filename):
        filename = secure_filename(file_obj.filename)
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
        full_file_path = os.path.join(UPLOAD_FOLDER, filename)
        file_obj.save(full_file_path)
        return full_file_path
