class MsgWarning(Warning):
    """带消息的警告基类"""
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class Init_PluginLoadWarning(MsgWarning): pass

class Init_PluginFolderException(Exception): pass
class Init_PluginFormatException(Exception): pass
class Init_PluginMetaException(Exception): pass
class Init_UnknownException(Exception): pass

class LibraryConfigError(Exception): pass