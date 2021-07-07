import os, shutil
from setuptools import setup, find_packages
#移除构建的build文件夹
# CUR_PATH = os.path.dirname(os.path.abspath(__file__))
# path = os.path.join(CUR_PATH, 'build')
# if os.path.isdir(path):
#     print('INFO del dir ', path)
#     shutil.rmtree(path)


setup(
    name = 'shily', #应用名
    author = 'shanlihou',
    version = '0.1',  #版本号
    packages = find_packages(),  #包括在安装包内的Python包
    include_package_data = True, #启用清单文件MANIFEST.in,包含数据文件

    # exclude_package_data = {'docs':['1.txt']},  #排除文件
    # install_requires = [#自动安装依赖
    #     '',
    # ],
)

shutil.rmtree('build')
shutil.rmtree('dist')
shutil.rmtree('shily.egg-info')