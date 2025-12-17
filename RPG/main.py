# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


import time
import math
import sys


def dynamic_gradient(text, start_rgb, end_rgb, duration=10):
    """
    动态流光渐变效果
    :param text: 显示的文字
    :param start_rgb: 颜色1 (R, G, B)
    :param end_rgb: 颜色2 (R, G, B)
    :param duration: 持续时间（秒）
    """
    r1, g1, b1 = start_rgb
    r2, g2, b2 = end_rgb

    start_time = time.time()

    # 隐藏光标（可选，某些终端有效）
    print("\033[?25l", end="")

    try:
        while time.time() - start_time < duration:
            # \r 表示回到行首，end="" 表示不换行
            # 这样下次打印就会覆盖这一行，而不是打在下一行
            sys.stdout.write("\r")

            # 当前的时间戳，用来控制波动的相位
            t = time.time() * 3  # *3 是速度，越大越快

            for i, char in enumerate(text):
                # 使用正弦波计算比例 (0.0 到 1.0 之间循环)
                # i * 0.3 控制波长的密度
                ratio = (math.sin(t + i * 0.3) + 1) / 2

                r = int(r1 + (r2 - r1) * ratio)
                g = int(g1 + (g2 - g1) * ratio)
                b = int(b1 + (b2 - b1) * ratio)

                sys.stdout.write(f"\033[38;2;{r};{g};{b}m{char}")

            sys.stdout.flush()  # 强制刷新缓冲区，确保立刻显示
            time.sleep(0.05)  # 控制帧率

    except KeyboardInterrupt:
        pass  # 允许按 Ctrl+C 停止
    finally:
        # 恢复光标并重置颜色
        print("\033[0m\033[?25h")
        print()  # 换行，避免后续输出在同一行




# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')
    # 比如：Excalibur 发光特效
    # 颜色从 金色(255, 215, 0) 流动到 红橙色(255, 69, 0)
    print("正在充能...\n")
    dynamic_gradient(
        "⚔️  EXCALIBUR - 誓约胜利之剑 [已激活]  ⚔️",
        (255, 215, 0),
        (255, 69, 0),
        duration=50  # 动画持续 5 秒
    )
    print("攻击完成！")

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
