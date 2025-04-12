from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from utils.document_processor import process_document

app = Flask(__name__)

# 配置设置
app.config.update({
    'UPLOAD_FOLDER': 'tmp/',
    'TEMPLATE_PATH': 'templates/report_template.ods',
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 限制上传大小为16MB
    'ALLOWED_EXTENSIONS': {'png', 'jpg', 'jpeg', 'pdf'}  # 允许的图片格式
})

@app.route('/')
def index():
    """显示首页表单"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_pdf():
    """处理表单提交并生成PDF"""
    try:
        # 获取表单文本数据
        form_data = request.form.to_dict()
        
        # 处理文件上传
        image_replacements = {}
        if 'image1' in request.files:
            image_file = request.files['image1']
            if image_file.filename != '':
                if allowed_file(image_file.filename):
                    # 安全保存上传的文件
                    filename = secure_filename(f"upload_{datetime.now().strftime('%Y%m%d%H%M%S')}_{image_file.filename}")
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image_file.save(filepath)
                    image_replacements['image1'] = filepath
                else:
                    return "不支持的文件类型", 400
        
        # 处理文档并生成PDF
        output_path = process_document(
            template_path=app.config['TEMPLATE_PATH'],
            output_dir=app.config['UPLOAD_FOLDER'],
            data=form_data,
            image_replacements=image_replacements if image_replacements else None
        )
        
        # 返回生成的PDF
        # 返回生成的PDF
        return send_file(
            output_path,
            as_attachment=True,
            download_name=f'{form_data.get("name", "自荐表")}_自荐表_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        app.logger.error(f"生成PDF失败: {str(e)}")
        return f"生成PDF时出错: {str(e)}", 500

def allowed_file(filename):
    """检查文件扩展名是否合法"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# 确保上传目录存在
def create_upload_folder():
    """创建上传目录（如果不存在）"""
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        app.logger.info(f"创建上传目录: {app.config['UPLOAD_FOLDER']}")

if __name__ == '__main__':
    create_upload_folder()
    app.run(host='0.0.0.0', port=5000, debug=True)