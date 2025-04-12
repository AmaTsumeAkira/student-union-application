import os
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
import tempfile
import subprocess

def process_document(template_path, output_dir, data, image_replacements=None):
    if image_replacements is None:
        image_replacements = {}

    with tempfile.TemporaryDirectory() as temp_dir:
        # 1. 解压ODS模板
        temp_extract = os.path.join(temp_dir, "extracted")
        with zipfile.ZipFile(template_path, 'r') as zip_ref:
            zip_ref.extractall(temp_extract)
        
        # 2. 处理图片替换
        if image_replacements:
            # 确保Pictures目录存在
            pictures_dir = os.path.join(temp_extract, "Pictures")
            os.makedirs(pictures_dir, exist_ok=True)
            
            # 处理manifest.xml
            manifest_path = os.path.join(temp_extract, "META-INF", "manifest.xml")
            tree = ET.parse(manifest_path)
            root = tree.getroot()
            ns = {'manifest': 'urn:oasis:names:tc:opendocument:xmlns:manifest:1.0'}
            
            for placeholder, img_path in image_replacements.items():
                if not os.path.exists(img_path):
                    raise FileNotFoundError(f"图片文件不存在: {img_path}")
                
                # 获取文件扩展名
                _, ext = os.path.splitext(img_path)
                ext = ext.lower()
                
                if ext not in ('.png', '.jpg', '.jpeg'):
                    raise ValueError(f"不支持的图片格式: {ext}")
                
                media_type = 'image/png' if ext == '.png' else 'image/jpeg'
                new_img_name = f"{placeholder}{ext}"
                new_img_path = os.path.join(pictures_dir, new_img_name)
                
                # 复制图片文件
                shutil.copy2(img_path, new_img_path)
                
                # 更新manifest.xml
                found = False
                for entry in root.findall('manifest:file-entry', ns):
                    full_path = entry.get('{%s}full-path' % ns['manifest'])
                    if full_path == f"Pictures/{new_img_name}":
                        found = True
                        break
                
                if not found:
                    ET.SubElement(
                        root, 
                        '{%s}file-entry' % ns['manifest'],
                        {
                            '{%s}full-path' % ns['manifest']: f"Pictures/{new_img_name}",
                            '{%s}media-type' % ns['manifest']: media_type
                        }
                    )
            
            tree.write(manifest_path, encoding='UTF-8', xml_declaration=True)
        
        # 3. 修改content.xml
        content_path = os.path.join(temp_extract, "content.xml")
        with open(content_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 文本替换
        for key, value in data.items():
            content = content.replace(f'${{{key}}}', str(value))
            content = content.replace(f'{{{{{key}}}}}', str(value))  # 处理双花括号格式
        
        # 图片替换 (专门处理您提供的模板结构)
        for placeholder in image_replacements.keys():
            img_path = image_replacements[placeholder]
            _, ext = os.path.splitext(img_path)
            ext = ext.lower()
            
            if ext in ('.png', '.jpg', '.jpeg'):
                new_img_name = f"{placeholder}{ext}"
                
                # 替换图片引用 (使用正则表达式精确匹配)
                content = re.sub(
                    r'(<draw:image [^>]*xlink:href=")[^"]*("[^>]*>)',
                    rf'\1Pictures/{new_img_name}\2',
                    content
                )
                
                # 替换描述中的占位符
                content = content.replace(
                    f'<svg:desc>${{{placeholder}}}</svg:desc>',
                    f'<svg:desc>{placeholder}</svg:desc>'
                )
        
        with open(content_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 4. 重新打包为ODS
        temp_ods = os.path.join(temp_dir, "modified.ods")
        with zipfile.ZipFile(temp_ods, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            for root_dir, _, files in os.walk(temp_extract):
                for file in files:
                    file_path = os.path.join(root_dir, file)
                    arcname = os.path.relpath(file_path, temp_extract)
                    zip_ref.write(file_path, arcname)
        
        # 5. 转换为PDF
        output_pdf = os.path.join(output_dir, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            subprocess.run([
                "libreoffice", "--headless", "--convert-to", "pdf",
                "--outdir", output_dir, temp_ods
            ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # 查找生成的PDF文件
            generated_pdf = os.path.join(output_dir, "modified.pdf")
            if os.path.exists(generated_pdf):
                os.rename(generated_pdf, output_pdf)
                return output_pdf
            
            # 尝试其他可能的文件名
            for f in os.listdir(output_dir):
                if f.startswith("modified") and f.endswith(".pdf"):
                    actual_path = os.path.join(output_dir, f)
                    os.rename(actual_path, output_pdf)
                    return output_pdf
            
            raise FileNotFoundError("PDF生成失败: 未找到输出文件")
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode('utf-8') if e.stderr else str(e)
            raise RuntimeError(f"PDF转换失败: {error_msg}")