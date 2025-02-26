# create_project.py
import os
import configparser
from datetime import datetime


def create_project_structure(project_name: str) -> None:
    """创建项目基本结构
    
    Args:
        project_name: 项目名称
    """
    # 基础目录结构
    directories = [
        'logs',
        'utils',
        'jsonfile',
        'results',
        'configs',
    ]

    # 创建主项目目录
    os.makedirs(project_name, exist_ok=True)

    # 创建子目录
    for directory in directories:
        os.makedirs(os.path.join(project_name, directory), exist_ok=True)

    # 创建基础文件
    files = {
        # utils 中的基础文件
        'utils/__init__.py':
        '''
from .log_config import setup_logger
from .feishu_inform import feishu_inform

''',
        'utils/feishu_inform.py':
        '''
import requests
def feishu_inform(msg):
    url = 'https://open.feishu.cn/open-apis/bot/v2/hook/121f6b81-46a4-44e1-998d-04f6a9f4f1cf'
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "msg_type": "text",
        "content": {"text": msg}
    }
    response = requests.post(url, headers=headers, json=data)  # 使用 json 参数直接发送 JSON 数据

    print('Response:', response.text)  # 输出响应文本方便调试

''',
        'utils/log_config.py':
        '''
from loguru import logger
import os
import sys

def setup_logger(log_name="__main__"):
    # 设置日志文件目录
    logfile_dir = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(logfile_dir):
        os.makedirs(logfile_dir)

    # 定义日志文件路径
    log_file = os.path.join(logfile_dir, f"{log_name}.log")

    # 清除默认日志处理器
    logger.remove()

    # 定义格式
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss,SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{file.name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    # 添加文件处理器（带自定义名字）
    logger.add(log_file, format=log_format, level="INFO", rotation="1 day", retention="5 days",compression="zip")

    # 控制台日志输出（含颜色）
    logger.add(sys.stdout, format=log_format, level="INFO")

    return logger

''',

        # 配置文件
        'configs/config.ini':
        '''
[DEFAULT]
debug = true

[database]
host = localhost
port = 3306
database = test
username = root
password = password

[api]
base_url = http://api.example.com
api_key = your_api_key_here
proxies = 127.0.0.1:10809
''',

        # README
        'README.md':
        f'''
# {project_name}

项目创建时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 目录结构
- logs/: 日志文件
- utils/: 工具函数
- jsonfile/: JSON 文件存储
- results/: 结果输出
- configs/: 配置文件

## 使用说明
1. 配置文件在 configs/config.ini
2. 日志文件保存在 logs/ 目录
''',

        # 主程序
        'main.py':
        '''
from utils.log_config import setup_logger
from utils.feishu_inform import feishu_inform
import configparser
import os
from DrissionPage import ChromiumPage,ChromiumOptions,SessionOptions,SessionPage
import requests
from jsonpath import jsonpath
import json
from typing import List, Dict, Any, Optional

logger = setup_logger('main')

class name:
    def __init__(self):
        self._load_config()
        pass

    def _load_config(self):
        self.config = configparser.ConfigParser()
        self.config.read('configs/config.ini', encoding='utf-8')
        # return config

    def _load_json(self):
        pass
    
    def _get_chrome_page(self):
        options = ChromiumOptions()
        options.headless(False)
        options.set_local_port(9225)
        options.no_imgs(True)
        self.chrome_page = ChromiumPage(options)
        self.chrome_page.set.auto_handle_alert()

    def _get_session_page(self):
        so = SessionOptions()
        # so.set_proxies(self.config['api']['proxies'])
        self.session_page = SessionPage(so)


def main():
    pass

    
if __name__ == "__main__":
    main()
''',

        # gitignore
        '.gitignore':
        '''
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 日志
logs/*
!logs/.gitkeep

# 结果文件
results/*
!results/.gitkeep

# JSON文件
jsonfile/*
!jsonfile/.gitkeep

# 环境文件
.env
.venv
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
''',
    }

    # 创建文件
    for file_path, content in files.items():
        full_path = os.path.join(project_name, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content.strip() + '\n')

    # 创建空的 .gitkeep 文件来保持空目录
    empty_dirs = ['logs', 'results', 'jsonfile']
    for dir_name in empty_dirs:
        with open(os.path.join(project_name, dir_name, '.gitkeep'), 'w') as f:
            pass


if __name__ == '__main__':
    project_name = input("请输入项目名称: ")
    create_project_structure(project_name)
    print(f"\n项目 {project_name} 创建成功！")
    print(f"目录结构：\n")
    for root, dirs, files in os.walk(project_name):
        level = root.replace(project_name, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")
