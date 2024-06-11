import io
import os

from django.http import FileResponse
from docxtpl.template import DocxTemplate


def create_file(context, template_path, file_path):
    """Создание файла"""
    doc = DocxTemplate(template_path)
    doc.render(context)
    doc.save(file_path)


def upload_file(file_path, user):
    """Отправка файла с документом"""
    try:
        with open(file_path, "rb") as file:
            file_content = file.read()
        file_obj = io.BytesIO(file_content)
        response = FileResponse(file_obj, as_attachment=True)
        response["Content-Disposition"] = f'attachment; filename="{user}.docx"'
        return response
    finally:
        os.remove(file_path)
