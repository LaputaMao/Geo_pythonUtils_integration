# # -*- coding: utf-8 -*-
# import sys
# import os
# from natcap.invest.sdr import sdr
# import tkinter as tk
# from tkinter import messagebox
#
# def run_sdr_model(workspace_dir, dem_path, lulc_path, soil_erosion_path, rainfall_erosivity_index_path, watersheds_path, biophysical_table_path, threshold_flow_accumulation, k_param, ic_0_param, sdr_max, drainage_path, lulc_path_bare_soil, l_max, status_label, root):
#     # 定义模型参数
#     args = {
#         'workspace_dir': workspace_dir,
#         'results_suffix': '',
#         'dem_path': dem_path,
#         'lulc_path': lulc_path,
#         'erodibility_path': soil_erosion_path,
#         'erosivity_path': rainfall_erosivity_index_path,
#         'watersheds_path': watersheds_path,
#         'biophysical_table_path': biophysical_table_path,
#         'threshold_flow_accumulation': threshold_flow_accumulation,
#         'k_param': k_param,
#         'ic_0_param': ic_0_param,
#         'sdr_max': sdr_max,
#     }
#
#     if drainage_path:
#         args['drainage_path'] = drainage_path
#     if lulc_path_bare_soil:
#         args['lulc_path_bare_soil'] = lulc_path_bare_soil
#     if l_max:
#         args['l_max'] = l_max
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
#         sdr.execute(args)
#
#         # 模型运行完成
#         messagebox.showinfo("运行完成", "水土保持模型运行完成。")
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
#     root.geometry("300x100")  # 设置窗口大小
#
#     # 创建一个简单的状态标签
#     status_label = tk.Label(root, text="准备运行模型...")
#     status_label.pack(pady=20)
#
#     # 从命令行获取参数
#     if len(sys.argv) < 13 or len(sys.argv) > 15:
#         messagebox.showerror("参数错误", "用法: python sdr_model.py <workspace_dir> <dem_path> <lulc_path> <soil_erosion_path> <rainfall_erosivity_index_path> <watersheds_path> <biophysical_table_path> <threshold_flow_accumulation> <k_param> <ic_0_param> <sdr_max> <l_max> [<drainage_path>] [<lulc_path_bare_soil>]")
#         sys.exit(1)
#
#     workspace_dir = sys.argv[1]
#     dem_path = sys.argv[2]
#     lulc_path = sys.argv[3]
#     soil_erosion_path = sys.argv[4]
#     rainfall_erosivity_index_path = sys.argv[5]
#     watersheds_path = sys.argv[6]
#     biophysical_table_path = sys.argv[7]
#     threshold_flow_accumulation = int(sys.argv[8])
#     k_param = float(sys.argv[9])
#     ic_0_param = float(sys.argv[10])
#     sdr_max = float(sys.argv[11])
#     l_max = int(sys.argv[12])
#
#     drainage_path = sys.argv[13] if len(sys.argv) > 13 else None
#     lulc_path_bare_soil = sys.argv[14] if len(sys.argv) > 14 else None
#
#     # 运行模型并显示状态
#     root.after(100, run_sdr_model, workspace_dir, dem_path, lulc_path, soil_erosion_path, rainfall_erosivity_index_path, watersheds_path, biophysical_table_path, threshold_flow_accumulation, k_param, ic_0_param, sdr_max, drainage_path, lulc_path_bare_soil, l_max, status_label, root)
#     root.mainloop()

# scripts/sdr_model.py
# -*- coding: utf-8 -*-
import os
from natcap.invest.sdr import sdr


# def run(workspace_dir: str,
#         dem_path: str,
#         lulc_path: str,
#         erodibility_path: str,
#         erosivity_path: str,
#         watersheds_path: str,
#         biophysical_table_path: str,
#         threshold_flow_accumulation: int,
#         k_param: float,
#         ic_0_param: float,
#         sdr_max: float,
#         l_max: int = None,
#         drainage_path: str = None,
#         lulc_path_bare_soil: str = None):
def run():
    """
    运行 InVEST 水土保持 (SDR) 模型的核心逻辑函数。
    """
    # # 1. 定义模型参数字典
    # args = {
    #     'workspace_dir': workspace_dir,
    #     'results_suffix': '',
    #     'dem_path': dem_path,
    #     'lulc_path': lulc_path,
    #     'erodibility_path': erodibility_path,
    #     'erosivity_path': erosivity_path,
    #     'watersheds_path': watersheds_path,
    #     'biophysical_table_path': biophysical_table_path,
    #     'threshold_flow_accumulation': threshold_flow_accumulation,
    #     'k_param': k_param,
    #     'ic_0_param': ic_0_param,
    #     'sdr_max': sdr_max,
    #     'l_max': l_max,
    #     'drainage_path': drainage_path,
    #     'lulc_path_bare_soil': lulc_path_bare_soil,
    # }

    workspace_dir = "E:\项目\环境监测院\OutPut1"

    args = {
        'workspace_dir': "E:\项目\环境监测院\OutPut1",
        'results_suffix': '',
        'dem_path': "E:\项目\环境监测院\水土保持数据\Shuozhou_30m_reprojected.tif",
        'lulc_path': "E:\项目\环境监测院\水土保持数据\shuozhou2023_LULC_reprojected.tif",
        'erodibility_path': "E:\项目\环境监测院\水土保持数据\SE.tif",  # soil_erosion_path
        'erosivity_path': "E:\项目\环境监测院\水土保持数据\REI_30m.tif",  # rainfall_erosivity_index_path
        'watersheds_path': "E:\项目\环境监测院\水土保持数据\朔州市_reprojected.shp",
        'biophysical_table_path': "E:\项目\环境监测院\水土保持数据\soil_density.csv",
        'threshold_flow_accumulation': 1000,
        'k_param': 0.2,
        'ic_0_param': 0.5,
        'sdr_max': 0.8,
        'l_max': None,
        'drainage_path': None,
        'lulc_path_bare_soil': None,
    }

    # 2. 删除值为 None 或空字符串的可选参数
    args = {k: v for k, v in args.items() if v is not None and v != ''}

    # 3. 确保工作目录存在
    if not os.path.exists(workspace_dir):
        os.makedirs(workspace_dir)

    # 4. 执行模型，让异常自然抛出给调用者
    sdr.execute(args)

    # 5. 如果执行成功，返回一个成功信息
    return f"水土保持模型运行成功！结果已保存在目录: {workspace_dir}"

# 同样，我们删除了整个 if __name__ == "__main__": 部分。
if __name__ == "__main__":
    run()