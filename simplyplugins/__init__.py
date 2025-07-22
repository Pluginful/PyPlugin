r""".
  ____  _                 _         ____  _             _           
 / ___|(_)_ __ ___  _ __ | |_   _  |  _ \| |_   _  __ _(_)_ __  ___ 
 \___ \| | '_ ` _ \| '_ \| | | | | | |_) | | | | |/ _` | | '_ \/ __|
  ___) | | | | | | | |_) | | |_| | |  __/| | |_| | (_| | | | | \__ \
 |____/|_|_| |_| |_| .__/|_|\__, | |_|   |_|\__,_|\__, |_|_| |_|___/
                   |_|      |___/                 |___/             
一个简单的插件加载器
"""
import importlib.util
import os,sys
import ast
import warnings,traceback
from . import exceptions as exc
from typing import Callable

# =========================全局变量=========================
plugins=[]
pluginMetas={}

# ===========================配置===========================
PRINT_NOTHING=0
"""不打印任何警告"""

PRINT_WARNINGS=1
"""打印警告"""

PRINT_TO_FUNCTION=2
"""将警告传递给自定义函数"""


warningsPrint=PRINT_WARNINGS
"""警告打印配置，默认PRINT_WARNINGS"""

warningsPrintFunction: Callable[[str, Exception], None] = None  # 添加类型提示
"""用于自定义警告处理的函数，需接受两个参数：警告信息(str)和异常对象(Exception)"""

# ===========================函数===========================
def pluginDir(dir:str):
    """初始化Simply Plugins插件目录，可以重复调用来重置插件列表"""
    global plugins, pluginMetas
    plugins=[]
    pluginMetas={}

    if not os.path.isdir(dir):
        raise exc.Init_PluginFolderException("插件目录不存在")

    modules = []
    # 把插件目录加入到sys.path以便后续导入，和插件作者调用其他插件的API
    if dir not in sys.path:
        sys.path.insert(0, dir)

    def get_metadata(file_path):
        """获取插件元数据"""
        try: # 捕获格式异常
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                f.close()
                
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == 'SPLUGIN_META':
                            metadata = ast.literal_eval(node.value)
                            if not isinstance(metadata, dict):  # SPLUGIN_META，你是字典吗
                                raise exc.Init_PluginMetaException("SPLUGIN_META必须是字典类型")
                            return metadata
        
        except SyntaxError as e:  # 格式异常！
            raise e
        else:
            raise exc.Init_PluginFormatException("插件必须要有SPLUGIN_META元数据")

    
    for entry in os.listdir(dir): # 开始遍历插件目录
        path = os.path.join(dir, entry)
        name, ext = os.path.splitext(entry)

        if name.startswith('__'):
            continue
        
        try:
            if ext in {'.py', '.pyw'}: # 单文件插件
                if importlib.util.find_spec(name) is None:
                    raise exc.Init_PluginFormatException(f"无法导入模块: {name}，恭喜你遇到了常人都无法遇到的错误！")

                metadata = get_metadata(path)
                pluginMetas[name] = metadata
                modules.append(name)
            elif os.path.isdir(path) and os.path.exists(os.path.join(path, '__init__.py')): # 文件夹插件
                if importlib.util.find_spec(name) is None:
                    raise exc.Init_PluginFormatException(f"无法导入模块: {name}，恭喜你遇到了常人都无法遇到的错误！")

                init_path = os.path.join(path, '__init__.py')
                metadata = get_metadata(init_path)
                pluginMetas[name] = metadata
                modules.append(name)
            elif ext in {'.pyd', '.pyz', '.pyx'}: # 我们不要二进制插件！
                raise exc.Init_PluginFormatException("单文件插件 和 文件夹插件的__init__.py 不能为二进制格式或Cython格式")
        except Exception as e:
            if warningsPrint == PRINT_WARNINGS:
                warnings.warn(f" {name} 插件有异常，跳过！", exc.Init_PluginLoadWarning)
                traceback.print_exception(e)
                print()
            elif warningsPrint == PRINT_TO_FUNCTION:
                if not callable(warningsPrintFunction):  # 添加运行时检查
                    raise exc.LibraryConfigError("warningsPrintFunction 必须是一个可调用的函数")
                warningsPrintFunction(f" {name} 插件有异常，跳过！", e)
            elif warningsPrint == PRINT_NOTHING: 
                pass
            
    plugins=modules
plugindir=pluginDir

