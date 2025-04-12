# 学生会干部换届自荐表生成系统

一个基于Flask的Web应用，用于自动化生成信息科技学院学生会干部换届自荐表PDF文档。

## 功能特点

- 📝 在线填写自荐表表单
- 📷 支持上传证件照
- 📊 自动将表单数据填充到ODS模板
- 🖨️ 一键生成并下载PDF格式的自荐表
- 💾 自动保存表单数据到浏览器本地存储
- 📱 响应式设计，适配电脑和手机访问
- ⚠️ 微信内置浏览器检测与引导提示

## 技术栈

- 后端: Python + Flask
- 前端: HTML5 + CSS + JavaScript
- 文档处理: LibreOffice (用于ODS转PDF)
- 依赖管理: pip + requirements.txt

## 安装与运行

### 前提条件

- Python 3.7+
- LibreOffice (用于文档转换)
- pip 包管理工具

### 安装步骤

1. 克隆仓库：
   ```bash
   git clone https://github.com/AmaTsumeAkira/student-union-application.git
   cd student-union-application
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 确保系统中安装了LibreOffice：
   - Ubuntu/Debian: `sudo apt install libreoffice`
   - CentOS/RHEL: `sudo yum install libreoffice`
   - macOS: `brew install libreoffice`
   - Windows: 从[官网](https://www.libreoffice.org/)下载安装

4. 创建必要的目录：
   ```bash
   mkdir -p tmp/
   ```

### 运行应用

```bash
python app.py
```

应用将运行在 `http://localhost:5000`

### 生产环境部署

建议使用Gunicorn + Nginx部署：

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 文件结构

```
.
├── app.py                     # Flask主应用
├── utils/
│   └── document_processor.py  # 文档处理模块   
├── requirements.txt           # Python依赖
├── templates/
│   └── index.html             # 前端页面模板
└── tmp/                       # 临时文件目录
```

## 配置选项

可在`app.py`中修改以下配置：

```python
app.config.update({
    'UPLOAD_FOLDER': 'tmp/',               # 上传文件目录
    'TEMPLATE_PATH': 'templates/report_template.ods',  # ODS模板路径
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 最大上传大小(16MB)
    'ALLOWED_EXTENSIONS': {'png', 'jpg', 'jpeg', 'pdf'}  # 允许的文件类型
})
```

## 注意事项

1. 确保服务器已安装LibreOffice并可在命令行中使用`libreoffice`命令
2. 上传目录(`tmp/`)需要有写入权限
3. 在微信中打开时，建议使用浏览器打开以获得最佳体验
