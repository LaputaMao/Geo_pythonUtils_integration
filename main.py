# main.py
# import subprocess
# import os
# import sys
#
# def get_path(filename):
#     """ 获取文件的绝对路径，兼容打包后的情况 """
#     if hasattr(sys, "_MEIPASS"):
#         # 如果是 PyInstaller 打包后的 .exe
#         return os.path.join(sys._MEIPASS, filename)
#     else:
#         # 如果是正常运行 .py
#         return filename
#
# # 构造 streamlit run app.py 命令
# # 注意：我们用 get_path 来确保能找到 app.py
# app_path = get_path("app.py")
# command = f'streamlit run "{app_path}" --server.headless=true --server.enableCORS=false'
#
# # 运行命令
# try:
#     subprocess.run(command, shell=True)
# except KeyboardInterrupt:
#     print("Application stopped.")
# main.py

import streamlit.web.cli as stcli
import sys
import os

# 定义一个函数，用于获取资源的绝对路径，兼容打包后的情况
def get_path(filename):
    if hasattr(sys, "_MEIPASS"):
        # 如果是 PyInstaller 打包后的 .exe
        return os.path.join(sys._MEIPASS, filename)
    else:
        # 如果是正常运行 .py
        return filename

# 在 main.py 中直接调用 Streamlit 的内部函数
if __name__ == '__main__':
    app_path = get_path("app.py")

    # 强制将控制台编码设置为 UTF-8，以防乱码
    # 这对于处理包含中文的错误信息非常有用
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

    try:
        sys.argv = [
            "streamlit", "run", app_path,
            "--server.headless=true",
            "--server.enableCORS=true"
        ]
        sys.exit(stcli.main())
    except Exception as e:
        # 如果发生任何错误，打印错误信息并暂停
        print(f"An unexpected error occurred: {e}")
        input("Press Enter to exit...")