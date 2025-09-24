# -*- coding: utf-8 -*-
# import sys
# import os
# from natcap.invest import carbon
# import tkinter as tk
# from tkinter import messagebox
#
#
# def run_carbon_model(workspace_dir, lulc_cur_path, lulc_fut_path, lulc_redd_path, carbon_pools_path, do_redd, calc_sequestration, status_label, root):
#     # 定义模型参数
#     args = {
#         'workspace_dir': workspace_dir,
#         'results_suffix': '',
#         'lulc_cur_path': lulc_cur_path,
#         'lulc_fut_path': lulc_fut_path,
#         'lulc_redd_path': lulc_redd_path,
#         'carbon_pools_path': carbon_pools_path,
#         'do_redd': do_redd,
#         'calc_sequestration': calc_sequestration,
#     }
#
#     # 删除值为 None 的可选参数
#     args = {k: v for k, v in args.items() if v is not None}
#
#     # 创建工作目录
#     if not os.path.exists(workspace_dir):
#         os.makedirs(workspace_dir)
#
#     try:
#         # 显示状态提示
#         status_label.config(text="模型正在运行，请稍候...")
#         root.update_idletasks()
#
#         # 运行模型
#         carbon.execute(args)
#
#         # 显示完成提示
#         messagebox.showinfo("运行完成", "碳储量模型运行完成。")
#     except Exception as e:
#         messagebox.showerror("运行错误", f"模型运行出错: {str(e)}")
#     finally:
#         # 关闭状态提示窗口
#         root.destroy()
#
# if __name__ == "__main__":
#     # 初始化Tkinter根窗口
#     root = tk.Tk()
#     root.title("模型运行状态")
#     root.geometry("300x100")
#
#     # 创建一个简单的状态标签
#     status_label = tk.Label(root, text="准备运行模型...")
#     status_label.pack(pady=20)
#
#     # 从命令行获取参数
#     if len(sys.argv) != 8:
#         messagebox.showerror("参数错误", "用法: python carbon_storage.py <workspace_dir> <lulc_cur_path> <lulc_fut_path> <lulc_redd_path> <carbon_pools_path> <do_redd> <calc_sequestration>")
#         sys.exit(1)
#
#     workspace_dir = sys.argv[1]
#     lulc_cur_path = sys.argv[2]
#     lulc_fut_path = sys.argv[3] if sys.argv[3] != 'None' else None
#     lulc_redd_path = sys.argv[4] if sys.argv[4] != 'None' else None
#     carbon_pools_path = sys.argv[5]
#     do_redd = sys.argv[6].lower() == 'true'
#     calc_sequestration = sys.argv[7].lower() == 'true'
#
#     # 运行模型并显示状态
#     root.after(100, run_carbon_model, workspace_dir, lulc_cur_path, lulc_fut_path, lulc_redd_path, carbon_pools_path, do_redd, calc_sequestration, status_label, root)
#     root.mainloop()

# scripts/carbon_model.py
# -*- coding: utf-8 -*-
import os
from natcap.invest import carbon

def run(workspace_dir: str,
        lulc_cur_path: str,
        carbon_pools_path: str,
        lulc_fut_path: str = None,
        lulc_redd_path: str = None,
        do_redd: bool = False,
        calc_sequestration: bool = True):
    """
    运行 InVEST 碳储量模型的核心逻辑函数。
    这个函数是纯粹的，不包含任何UI元素。
    """
    # 1. 定义模型参数字典
    args = {
        'workspace_dir': workspace_dir,
        'results_suffix': '',
        'lulc_cur_path': lulc_cur_path,
        'carbon_pools_path': carbon_pools_path,
        'lulc_fut_path': lulc_fut_path,
        'lulc_redd_path': lulc_redd_path,
        'do_redd': do_redd,
        'calc_sequestration': calc_sequestration,
    }

    # 2. 删除值为 None 的可选参数，这是 InVEST 模型的要求
    args = {k: v for k, v in args.items() if v is not None and v != ''}

    # 3. 确保工作目录存在
    if not os.path.exists(workspace_dir):
        os.makedirs(workspace_dir)

    # 4. 执行模型，并让异常自然抛出
    # 我们不再使用 try...except 来显示 messagebox，而是让调用者去处理
    carbon.execute(args)

    # 5. 如果执行成功，返回一个成功信息
    return f"模型运行成功！结果已保存在目录: {workspace_dir}"

# 我们删除了整个 if __name__ == "__main__": 部分，
# 因为这个脚本现在是作为一个模块被 app.py 调用的，而不是直接运行。
