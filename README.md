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

2. 创建并激活虚拟环境（推荐，可选，可以直接运行第三步）：
   ```bash
   # Linux/macOS
   python -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 确保系统中安装了LibreOffice：
   - Ubuntu/Debian: `sudo apt install libreoffice`
   - CentOS/RHEL: `sudo yum install libreoffice`
   - macOS: `brew install libreoffice`
   - Windows: 从[官网](https://www.libreoffice.org/)下载安装

5. 创建必要的目录：
   ```bash
   mkdir -p tmp/
   ```

### 运行应用

```bash
# 确保虚拟环境已激活
python app.py
```

应用将运行在 `http://localhost:5000`

### 停止应用后

当完成使用后，可以停用虚拟环境：
```bash
deactivate
```

### 生产环境部署

建议使用Gunicorn + Nginx部署（在虚拟环境中）：

```bash
# 激活虚拟环境后
pip install gunicorn
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
## 模板文件要求

1. 必须使用`.ods`格式（OpenDocument Spreadsheet）
2. 模板应包含所有必要的表格结构和样式
3. 推荐使用LibreOffice或OpenOffice编辑模板

## 占位符格式

系统支持两种占位符格式：

1. **简单格式**：`${字段名}`
   - 示例：`${name}` 会被替换为表单中的"name"字段值

2. **双花括号格式**：`{{字段名}}`
   - 示例：`{{xb}}` 会被替换为表单中的"xb"（性别）字段值

## 图片占位符特殊处理

图片占位符需要特殊格式：

```xml
<draw:image xlink:href="Pictures/${image1}" ...>
  <svg:desc>${image1}</svg:desc>
</draw:image>
```

系统会自动：
1. 将`xlink:href`属性中的图片路径替换为实际上传的图片
2. 移除`<svg:desc>`中的占位符标记

## 模板制作步骤

1. 在LibreOffice中设计好表格样式
2. 在需要动态填充的位置插入文本占位符
   - 例如：在"姓名"单元格中输入`${name}`
3. 如需插入图片：
   - 先插入一个任意图片作为占位
   - 右键图片 → 编辑 → 将图片路径改为`Pictures/${image1}`
   - 在图片描述中添加`${image1}`
4. 保存为`.ods`格式

## 模板注意事项

1. 占位符区分大小写，必须与表单字段名完全一致
2. 图片占位符必须严格遵循XML格式要求
3. 修改模板后建议先在LibreOffice中测试打开
4. 复杂的格式（如合并单元格）应在模板中预先设置好
5. 系统会自动处理换行符，但复杂排版建议在模板中固定

## 示例模板片段

```xml
<table:table-cell>
  <text:p>姓名：${name}</text:p>
</table:table-cell>
<table:table-cell>
  <text:p>性别：{{xb}}</text:p>
</table:table-cell>
<draw:frame>
  <draw:image xlink:href="Pictures/${image1}">
    <svg:desc>${image1}</svg:desc>
  </draw:image>
</draw:frame>
```

## 注意事项

1. 确保服务器已安装LibreOffice并可在命令行中使用`libreoffice`命令
2. 上传目录(`tmp/`)需要有写入权限
3. 在微信中打开时，建议使用浏览器打开以获得最佳体验
