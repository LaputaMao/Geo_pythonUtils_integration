# # main.py
# # import subprocess
# # import os
# # import sys
# #
# # def get_path(filename):
# #     """ 获取文件的绝对路径，兼容打包后的情况 """
# #     if hasattr(sys, "_MEIPASS"):
# #         # 如果是 PyInstaller 打包后的 .exe
# #         return os.path.join(sys._MEIPASS, filename)
# #     else:
# #         # 如果是正常运行 .py
# #         return filename
# #
# # # 构造 streamlit run app.py 命令
# # # 注意：我们用 get_path 来确保能找到 app.py
# # app_path = get_path("app.py")
# # command = f'streamlit run "{app_path}" --server.headless=true --server.enableCORS=false'
# #
# # # 运行命令
# # try:
# #     subprocess.run(command, shell=True)
# # except KeyboardInterrupt:
# #     print("Application stopped.")
# # main.py
#
# import streamlit.web.cli as stcli
# import sys
# import os
#
# # 定义一个函数，用于获取资源的绝对路径，兼容打包后的情况
# def get_path(filename):
#     if hasattr(sys, "_MEIPASS"):
#         # 如果是 PyInstaller 打包后的 .exe
#         return os.path.join(sys._MEIPASS, filename)
#     else:
#         # 如果是正常运行 .py
#         return filename
#
# # 在 main.py 中直接调用 Streamlit 的内部函数
# if __name__ == '__main__':
#     app_path = get_path("app.py")
#
#     # 强制将控制台编码设置为 UTF-8，以防乱码
#     # 这对于处理包含中文的错误信息非常有用
#     sys.stdout.reconfigure(encoding='utf-8')
#     sys.stderr.reconfigure(encoding='utf-8')
#
#     try:
#         sys.argv = [
#             "streamlit", "run", app_path,
#             "--server.headless=true",
#             "--server.enableCORS=true"
#         ]
#         sys.exit(stcli.main())
#     except Exception as e:
#         # 如果发生任何错误，打印错误信息并暂停
#         print(f"An unexpected error occurred: {e}")
#         input("Press Enter to exit...")

# main.py
import streamlit.web.cli as stcli
import sys
import os


# 定义一个函数，用于获取资源的绝对路径，兼容打包后的情况
def get_path(relative_path):
    """
    获取资源的绝对路径，兼容 PyInstaller 打包后的情况。
    当打包时，文件会被放入 sys._MEIPASS 或与可执行文件同级。
    """
    if hasattr(sys, "_MEIPASS"):
        # 如果是 PyInstaller 打包后的 .exe，文件在临时目录
        return os.path.join(sys._MEIPASS, relative_path)

    # 否则，在开发模式下，文件在项目根目录
    # 考虑到 app.py 也在项目根目录，这里直接拼接
    # 或者更稳妥地，获取当前 main.py 所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, relative_path)


# 在 main.py 中直接调用 Streamlit 的内部函数
if __name__ == '__main__':
    # 获取 app.py 的路径
    app_path = get_path("app.py")

    # 确保 sys._MEIPASS 被添加到 Streamlit 的模块搜索路径
    # 这对于 Streamlit 内部查找其自身资源至关重要
    if hasattr(sys, "_MEIPASS"):
        os.environ["STREAMLIT_SERVER_FOLDER"] = sys._MEIPASS

    # 模拟命令行参数，直接调用 Streamlit CLI
    sys.argv = [
        "streamlit", "run", app_path,
        "--server.headless=false",  # 设置为 True 在打包后不显示浏览器自动打开
        "--server.enableCORS=false",  # 禁用 CORS 允许本地访问
        "--server.port=8501",  # 可以指定一个端口，防止冲突
        "--global.developmentMode=false"  # <--- 添加这行
    ]

    try:
        sys.exit(stcli.main())
    except SystemExit as e:
        # Streamlit 可能会在正常退出时抛出 SystemExit
        if e.code == 0:
            print("Streamlit application exited gracefully.")
        else:
            print(f"Streamlit application exited with error code: {e.code}")
        # 如果需要调试，可以在这里添加 input() 暂停控制台
        # input("Press Enter to exit...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # input("Press Enter to exit...")
