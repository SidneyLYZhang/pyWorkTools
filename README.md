# 常用工具集合

这里开始重写一些小工具，都是在工作中用的比较多的那些工具。
这些小工具的核心目标是快速有效，尽量减小引用难度。

1. simdate: 基于 pendulum 的再封装，快速处理常用工作内容。
2. simreader: 基于 pandas和polars 实现常用数据包的读取。
3. simplot: 基于多个画图包，实现多种专用图表的绘制。
4. simdata: 目标实现快速数据分析，常用关键分析数据的直出。

**进度**

- [x] simdate : Complete
- [ ] simreader : 半成品……
- [ ] simplot : 未开始
- [ ] simdata : 粗制滥造中……

**使用说明**

1. 需要提前使用pip安装如下package：
    - pandas
    - numpy
    - polars[all]
    - pendulum
2. 使用 `pip install -r ./requirements.txt` 快速安装所需前置包。
3. git clone到本地使用 `import` 引用使用。
4. 各包的具体使用请参考对应脚本中的说明。