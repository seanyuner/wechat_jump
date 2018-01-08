# wechat_jump


经过对游戏的观察，自己想到了几种理论上可行的方案，慢慢完善在这里吧

经实践，发现理论都是完美的，现实都是残酷的，，，tencent也在不断地升级反作弊吧。

---
**运行环境**：

软件：python3.6、OpenCV2

驱动：adb，用于安卓手机调试，参考[https://github.com/wangshub/wechat_jump_game](https://github.com/wangshub/wechat_jump_game)

## [方案1](https://github.com/seanyuner/wechat_jump/blob/master/1_track_whitedot_simplest.py)：

### 观察：
- 游戏开始的第一跳都是固定的步长
- 如果上次跳到中心，下一个目标会显示白点

### 思路：
1. 通过pixel值来识别棋子，作为初始点
2. 第一步手动设置distance来跳中目标中心，后面追踪白点作为目标点
3. 计算距离，换算时间

**理论上这是最简单，同时分数也上涨最快的方案**


## [方案2](https://github.com/seanyuner/wechat_jump/blob/master/2_track_shadow.py)：

### 观察：
- 下一目标块阴影的位置相对稳定

### 思路：
1. 通过pixel值来识别棋子，作为初始点
2. 直接计算阴影的起始点，然后将其向右偏移一定距离作为目标点
3. 计算距离，换算时间

**理论上这是最简单，同时最稳定的方案**
