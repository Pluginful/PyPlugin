# 🧩 Simply Plugins
一个超级简单的，基于事件和importlib的插件加载器

以后将会被NotClock和PluginMC两个项目使用

## 🔨 功能
- 加载插件
- 卸载插件
- 插件列表
- 插件（热）重载

## 📦 安装
没错，由于这个库才刚刚开始开发，所以你只能克隆这个仓库然后自己构建+安装
```bash
git clone https://github.com/Pluginful/plugin-loader
cd PyPlugin
pip install build
python -m build
pip install dist/PyPlugin-*.whl
```

## ❓怎么有README_SAME.md文件
这个项目的原名就是pyplugin，但是已经重名了  
而这个文件就是撞车了的pyplugin的README，使用MIT许可

我可以基于[pyplugin/pyplugin](https://github.com/pyplugin/pyplugin)的插件加载功能，来代替掉原来计划的importlib核心