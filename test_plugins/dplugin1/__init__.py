"""文件夹插件测试"""
SPLUGIN_META= {
    "name":"Folder Plugin Example",
    "displayVersion":"0",
    "version":0,
    "author":"SystemFileB",
    "description":"Nothing ;)",
    "descriptionType":"text",
    "license":"BSD 3-Clause",
    "deps": {
        "python": ">0",
        "loader": ">0",
        "pip": {},
        "plugins": {}
    },
    "permissions": {
        "splugin.file.list":{"dir":[".."],"desc":"Test permission"}, # 只允许访问上一级目录
        "splugin.file.selector":{"desc":"Test permission"},        # 只能访问选择器给出的文件
        "splugin.file.all":{"desc":"Test permission"},             # 无限制地文件访问（危险权限）
        "splugin.syspath":{"desc":"Used to load another plugins"}, # 允许操作sys.path变量（危险权限）
        "splugin.nothing":{}                                       # 没写权限说明的示例权限
    },
    "i18n": {
        "zh-cn": {
            "name": "文件夹插件示例",
            "description": "没有说明 ;)",
            "permissions": {
                "splugin.file.list": "测试权限",
                "splugin.file.selector": "测试权限",
                "splugin.file.all": "测试权限",
                "splugin.syspath": "用于加载其他插件"
            }
        }
    }
}