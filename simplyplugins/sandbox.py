from RestrictedPython import compile_restricted
from RestrictedPython import safe_builtins
from RestrictedPython.Eval import default_guarded_getitem
from RestrictedPython.Guards import guarded_unpack_sequence
import os
import sys
from . import pluginDir, permissionMsgbox, pluginMetas

class PluginSandbox:
    def __init__(self, pluginName):
        self.pluginName = pluginName
        self.module = None

        # 获取插件目录
        self.pluginRoot = os.path.join(pluginDir, pluginName)

        # 获取插件元数据
        self.pluginMeta:dict = pluginMetas.get(pluginName, {})

        self.permissions: dict=self.pluginMeta.get("permissions", {})
        for perm in self.permissions.keys():
            self.permissions[perm]["allowed"]=False
            if perm=="splugin.file.list":
                self.allowedPaths = set(self.permissions[perm]["dir"])

        # 加载插件代码
        self._loadPlugin()

    def permissionRequest(self, permId):
        """请求用户授予指定权限"""
        isAllowed=permissionMsgbox(permId, self.pluginMeta)
        self.permissions[permId]["allowed"]=isAllowed
        return isAllowed

    def _loadPlugin(self):
        """加载并执行插件代码"""
        restrictedGlobals = {
            "__builtins__": self._getSafeBuiltins(),
            "sys": self._createSafeSys(),
            "__name__": self.pluginName
        }

        # 构造 import ... as module 语句
        import_statement = f"import {self.pluginName} as module"

        # 编译 import 语句
        byteCode = compile_restricted(import_statement, filename=f"<{self.pluginName}>", mode="exec")
        # 执行编译后的字节码
        exec(byteCode, restrictedGlobals)
        # 从 restrictedGlobals 中获取插件模块
        self.module = restrictedGlobals["module"]

    def _getSafeBuiltins(self):
        """生成安全的builtins环境"""
        return {
            **safe_builtins,
            "__import__": self._safeImport,
            "open": self._safeOpen,
            "_getitem_": default_guarded_getitem,
            "_unpack_sequence_": guarded_unpack_sequence
        }

    def _safeImport(self, name, *args):
        """受限制的模块导入"""
        if not self.permissions["splugin.syspath"]["allowed"] and name in sys.builtin_module_names:
            raise ImportError(f"禁止导入系统模块: {name}")
        return __import__(name, *args)

    def _safeOpen(self, path, mode="r", *args, **kwargs):
        """受控的文件访问"""
        if self.allowedPaths is not None:
            absPath = os.path.abspath(path)
            if not any(absPath.startswith(p) for p in self.allowedPaths):
                if not self.permissionRequest("splugin.file.selector"):
                    raise PermissionError("用户拒绝文件访问授权")
        return open(path, mode, *args, **kwargs)

    def _createSafeSys(self):
        """创建安全的sys模块"""
        safeSys = sys.__dict__.copy()
        if not self.permissions["splugin.syspath"]["allowed"]:
            safeSys["path"] = [self.pluginRoot]
            del safeSys["modules"]
        return type("SafeSys", (object,), safeSys)