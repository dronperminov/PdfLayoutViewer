from pdf_extractor import PdfExtractor
from flask import Flask
from flask import request, send_file, redirect, send_from_directory, url_for
from werkzeug.utils import secure_filename
from layout_viewer import LayoutViewer
import os


app = Flask(__name__)

app.config['IMAGES_FOLDER'] = 'images'  # папка с изображениями
app.config['STYLES_FOLDER'] = 'styles'  # папка со стилями
app.config['JS_FOLDER'] = 'js'  # папка с javascript скриптами
app.config['UPLOAD_FOLDER'] = 'uploads'  # папка для загрузок pdf-документов


@app.route('/images/<filename>')
def image_file(filename):
    return send_from_directory(app.config['IMAGES_FOLDER'], filename)


@app.route('/styles/<filename>')
def style_file(filename):
    return send_from_directory(app.config['STYLES_FOLDER'], filename)


@app.route('/js/<filename>')
def js_file(filename):
    return send_from_directory(app.config['JS_FOLDER'], filename)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']

        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('view_file', filename=filename))

    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Демо версия просмотра PDF с извлечённой структурой</title>
            <link rel="stylesheet" type="text/css" href="/styles/form.css?v=10">
        </head>
        <body>
            <h1>Демо версия просмотра PDF с извлечённой структурой</h1>
            
            <p>Сюда можно загрузить PDF документ и посмотреть на результат</p>
            <form action="" method="post" enctype="multipart/form-data">
                <h2>Форма для загрузки</h2>
                <div>
                    <input type="file" name="file" id="file" class="input-file" accept=".pdf" onchange="UpdateLabel()" />
                    <label for="file">Выберите pdf файл</label>
                </div>
                <div id="selected-file"></div>

                <div><input type="submit" value="Загрузить файл"></div>
            </form>
            
            <h2>Несколько примеров разбора pdf'ок</h2>
            
            <p>Результат разбора изображения с блок-схемой</p>
            <div class="example-image">
                <img src="/images/example1.png">
            </div>

            <br><p>Результат разбора изображения с описанием задания по программированию</p>
            <div class="example-image">
                <img src="/images/example2.png">
            </div>
            
            <script>
                function UpdateLabel() {
                    let input = document.getElementById("file")
                    let label = document.getElementById("selected-file")
                    
                    label.innerHTML = input.value
                }
            </script>
        </body>
        </html>
    '''


@app.route('/view-file/<filename>')
def view_file(filename):
    path = app.config["UPLOAD_FOLDER"] + '/' + filename

    extractor = PdfExtractor()
    images, pages = extractor.extract(path, 110)

    layout_viewer = LayoutViewer(images, pages, filename)
    layout_viewer.save_images()
    hash_pdf = layout_viewer.get_md5(path)

    return layout_viewer.get_html(hash_pdf)


if __name__ == '__main__':
    app.run(debug=True)
