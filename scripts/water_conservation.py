# '''
#     to Mr.Mu:
#         在原来代码基础上，新增calculate_k和calculate_water_retention两个计算函数，以及readTif和writeTiff写入和输出函数
#         新增的输入数据变量有4个，c1_path，c2_path，v_path和t_path
#         k_path 和 y_path是中间过程的路径，依赖于workspace_dir路径
#
# '''
#
#
# # -*- coding: utf-8 -*-
# import os
# from natcap.invest import annual_water_yield
# from osgeo import gdal
# import numpy as np
# import sys
# import tkinter as tk
# from tkinter import messagebox
#
#
# # 读取tif数据集
# def readTif(fileName):
#     dataset = gdal.Open(fileName)
#     if dataset is None:
#         print(f"{fileName} 文件无法打开")
#     return dataset
#
#
# # 保存tif文件函数
# def writeTiff(im_data, im_geotrans, im_proj, path, nodata_value=0):
#     if 'int8' in im_data.dtype.name:
#         datatype = gdal.GDT_Byte
#     elif 'int16' in im_data.dtype.name:
#         datatype = gdal.GDT_UInt16
#     else:
#         datatype = gdal.GDT_Float32
#
#     if len(im_data.shape) == 3:
#         im_bands, im_height, im_width = im_data.shape
#     elif len(im_data.shape) == 2:
#         im_data = np.array([im_data])
#         im_bands, im_height, im_width = im_data.shape
#
#     # 创建文件
#     driver = gdal.GetDriverByName("GTiff")
#     dataset = driver.Create(path, int(im_width), int(im_height), int(im_bands), datatype)
#
#     if dataset is not None:
#         dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
#         dataset.SetProjection(im_proj)  # 写入投影
#
#         for i in range(im_bands):
#             band = dataset.GetRasterBand(i + 1)
#             band.WriteArray(im_data[i])
#             if nodata_value is not None:
#                 band.SetNoDataValue(nodata_value)
#
#         del dataset
#
#
# # 定义土壤饱和导水率计算函数
# def calculate_k(c1_path, c2_path, output_path):
#     """
#     计算土壤饱和导水率 (K)
#     :param c1_path: 黏粒含量 (C1) 的tif文件路径
#     :param c2_path: 沙粒含量 (C2) 的tif文件路径
#     :param output_path: 输出的土壤饱和导水率 (K) tif文件路径
#     """
#     # 读取输入数据
#     c1_ds = readTif(c1_path)
#     c2_ds = readTif(c2_path)
#
#     c1 = c1_ds.GetRasterBand(1).ReadAsArray()
#     c2 = c2_ds.GetRasterBand(1).ReadAsArray()
#
#     # 获取地理信息
#     geo_transform = c1_ds.GetGeoTransform()
#     projection = c1_ds.GetProjection()
#     nodata_value = c1_ds.GetRasterBand(1).GetNoDataValue()
#
#     # 初始化结果数组
#     k = np.full_like(c1, nodata_value, dtype=np.float32)
#
#     # 计算土壤饱和导水率 K
#     valid_mask = (c1 != nodata_value) & (c2 != nodata_value)
#     if np.any(valid_mask):
#         k[valid_mask] = (
#             114.8 * 10 ** (
#                 -0.6 + 1.26 * 0.01 * c2[valid_mask] - 6.4 * 0.001 * c1[valid_mask]
#             )
#         )
#
#     # 保存结果为tif
#     writeTiff(k, geo_transform, projection, output_path, nodata_value)
#
#     print(f"土壤饱和导水率计算完成，结果保存在: {output_path}")
#
#
# # 定义水源涵养量计算函数
# def calculate_water_retention(v_path, k_path, t1_path, y_path, output_path):
#     """
#     计算水源涵养量
#     :param v_path: 流速速率 (V) 的tif文件路径
#     :param k_path: 土壤饱和导水率 (K) 的tif文件路径
#     :param t1_path: 地形指数 (T1) 的tif文件路径
#     :param y_path: 产水量 (Y) 的tif文件路径
#     :param output_path: 输出的水源涵养量 (WR) tif文件路径
#     """
#     # 读取输入数据
#     v_ds = readTif(v_path)
#     k_ds = readTif(k_path)
#     t1_ds = readTif(t1_path)
#     y_ds = readTif(y_path)
#
#     v = v_ds.GetRasterBand(1).ReadAsArray()
#     k = k_ds.GetRasterBand(1).ReadAsArray()
#     t1 = t1_ds.GetRasterBand(1).ReadAsArray()
#     y = y_ds.GetRasterBand(1).ReadAsArray()
#
#     # 获取地理信息
#     geo_transform = v_ds.GetGeoTransform()
#     projection = v_ds.GetProjection()
#     nodata_value = v_ds.GetRasterBand(1).GetNoDataValue()
#
#     # 初始化结果数组
#     wr = np.full_like(v, nodata_value, dtype=np.float32)
#
#     # 计算水源涵养量 WR
#     valid_mask = (v != nodata_value) & (k != nodata_value) & (t1 != nodata_value) & (y != nodata_value)
#     if np.any(valid_mask):
#         wr[valid_mask] = (
#             np.minimum(249 / v[valid_mask], 1) *
#             np.minimum(0.3 * t1[valid_mask], 1) *
#             np.minimum(1, k[valid_mask] / 300) *
#             y[valid_mask]
#         )
#
#     # 保存结果为tif
#     writeTiff(wr, geo_transform, projection, output_path, nodata_value)
#
#     print(f"水源涵养量计算完成，结果保存在: {output_path}")
#
# # # 定义输入文件路径
# # workspace_dir = r'E:\遥相科技\环境监测院\模型测试\水源涵养'  # 工作目录
# # lulc_path = r'E:\遥相科技\环境监测院\水源涵养数据\clcd2019clip1.tif'  # 土地利用/覆盖数据
# # depth_to_root_rest_layer_path = r'E:\遥相科技\环境监测院\水源涵养数据\土壤厚度\区域已完成土壤厚度_Project_PolygonToR11.tif'  # 土壤组数据
# # precipitation_path = r'E:\遥相科技\环境监测院\水源涵养数据\降水\pre2022_Resample_Clip21.tif'  # 降水数据
# # eto_path = r'E:\遥相科技\环境监测院\水源涵养数据\蒸散发\etp_2022bahsang_Clip2.tif'  # 参考蒸散量数据
# # pawc_path = r"E:\遥相科技\环境监测院\水源涵养数据\pwac.tif"
# # watersheds_path = r'E:\遥相科技\环境监测院\水源涵养数据\坝上农草区范围.shp'  # 流域边界数据
# # biophysical_table_path = r'E:\遥相科技\环境监测院\水源涵养数据\biophysical_table_gura.csv'
# #
# # # 新增计算过程的输入参数和相对路径
# # c1_path = r"E:\遥相科技\环境监测院\水源涵养数据\水源涵养过程数据\V.tif"  # 黏粒含量 C1 的路径
# # c2_path = r"E:\遥相科技\环境监测院\水源涵养数据\水源涵养过程数据\T_30_mask.tif"  # 沙粒含量 C2 的路径
# # v_path = r"E:\遥相科技\环境监测院\水源涵养数据\水源涵养过程数据\V.tif"  # 流速速率 V 的路径
# # t_path = r"E:\遥相科技\环境监测院\水源涵养数据\水源涵养过程数据\T_30_mask.tif"  # 地形指数 T1 的路径
# # k_path = os.path.join(workspace_dir, "output\per_pixel\K_calculated.tif")  # 计算生成的土壤饱和导水率 K 的路径
# # # y_path = os.path.join(workspace_dir, "output\per_pixel\wyield_mask.tif")  # 从InVEST模型生成的产水量 Y 的路径
# # y_path = os.path.join(workspace_dir, "output\per_pixel\wyield.tif")  # 从InVEST模型生成的产水量 Y 的路径
# # output_path = os.path.join(workspace_dir, "water_conservation.tif")  # 水源涵养量 WR 的输出路径
#
#
# def run_model_with_gui():
#     if len(sys.argv) != 14:
#         print("用法: python water_conservation.py <workspace_dir> <lulc_path> depth_to_root_rest_layer_path> "
#               "<precipitation_path> <eto_path> <pawc_path> <watersheds_path> <biophysical_table_path> <seasonality_constant> "
#               "<c1_path> <c2_path> <v_path> <t_path>")
#         sys.exit(1)
#
#     workspace_dir = sys.argv[1]
#     lulc_path = sys.argv[2]
#     depth_to_root_rest_layer_path = sys.argv[3]
#     precipitation_path = sys.argv[4]
#     eto_path = sys.argv[5]
#     pawc_path = sys.argv[6]
#     watersheds_path = sys.argv[7]
#     biophysical_table_path = sys.argv[8]
#     seasonality_constant = int(sys.argv[9])
#     c1_path = sys.argv[10]
#     c2_path = sys.argv[11]
#     v_path = sys.argv[12]
#     t_path = sys.argv[13]
#
#     k_path = os.path.join(workspace_dir, "output\per_pixel\K_calculated.tif")  # 计算生成的土壤饱和导水率 K 的路径
#     # y_path = os.path.join(workspace_dir, "output\per_pixel\wyield_mask.tif")  # 测试数据行列号不统一
#     y_path = os.path.join(workspace_dir, "output\per_pixel\wyield.tif")  # 从InVEST模型生成的产水量 Y 的路径
#     output_path = os.path.join(workspace_dir, "water_conservation.tif")  # 水源涵养量 WR 的输出路径
#
#     # 初始化Tkinter窗口
#     root = tk.Tk()
#     root.title("模型运行状态")
#     root.geometry("300x100")
#
#     # 创建状态标签
#     status_label = tk.Label(root, text="准备运行模型...")
#     status_label.pack(pady=20)
#
#     # # 创建关闭按钮
#     # close_button = tk.Button(root, text="关闭", command=root.destroy, state=tk.DISABLED)
#     # close_button.pack(pady=10)
#
#     def update_status(new_status):
#         """更新状态标签的内容并刷新窗口"""
#         status_label.config(text=new_status)
#         root.update()
#
#     def run_steps():
#         try:
#             # 创建工作目录
#             if not os.path.exists(workspace_dir):
#                 os.makedirs(workspace_dir)
#             update_status("创建工作目录完成...")
#
#             # 运行 InVEST 产水量模型
#             update_status("正在运行 InVEST 产水量模型...")
#             args = {
#                 'workspace_dir': workspace_dir,
#                 'results_suffix': '',
#                 'lulc_path': lulc_path,
#                 'precipitation_path': precipitation_path,
#                 'eto_path': eto_path,
#                 'depth_to_root_rest_layer_path': depth_to_root_rest_layer_path,
#                 'pawc_path': pawc_path,
#                 'watersheds_path': watersheds_path,
#                 'biophysical_table_path': biophysical_table_path,
#                 'seasonality_constant': seasonality_constant,
#             }
#             annual_water_yield.execute(args)
#             update_status(f"InVEST模型运行完成，结果保存在: {workspace_dir}")
#
#             # 计算土壤饱和导水率 K
#             update_status("计算土壤饱和导水率 K...")
#             calculate_k(c1_path, c2_path, k_path)
#             if not os.path.exists(k_path):
#                 raise FileNotFoundError(f"土壤饱和导水率结果文件未生成: {k_path}")
#             update_status("土壤饱和导水率 K 计算完成")
#
#             # 计算水源涵养量 WR
#             update_status("计算水源涵养量 WR...")
#             calculate_water_retention(v_path, k_path, t_path, y_path, output_path)
#             if not os.path.exists(output_path):
#                 raise ValueError(f"水源涵养量计算失败，未生成结果文件: {output_path}")
#             update_status(f"水源涵养模型运行完成，结果保存在: {output_path}")
#
#         except FileNotFoundError as e:
#             update_status(f"运行错误: 文件未找到 - {str(e)}")
#             tk.messagebox.showerror("运行错误", f"文件未找到: {str(e)}")
#         except ValueError as e:
#             update_status(f"运行错误: 数据问题 - {str(e)}")
#             tk.messagebox.showerror("运行错误", f"数据问题: {str(e)}")
#         except Exception as e:
#             update_status(f"运行过程中发生错误: {str(e)}")
#             tk.messagebox.showerror("运行错误", f"发生未知错误: {str(e)}")
#         finally:
#             # close_button.config(state=tk.NORMAL)
#             update_status("运行已完成，您可以关闭窗口。")
#
#     # 在100毫秒后启动运行步骤
#     root.after(100, run_steps)
#     root.mainloop()
#
#
# if __name__ == "__main__":
#     run_model_with_gui()

# scripts/water_yield_retention_model.py
# -*- coding: utf-8 -*-
import os
import numpy as np
from osgeo import gdal
from natcap.invest import annual_water_yield


# --- 辅助函数 (无需修改) ---

def readTif(fileName):
    dataset = gdal.Open(fileName)
    if dataset is None:
        raise FileNotFoundError(f"{fileName} 文件无法打开或不存在")
    return dataset


def writeTiff(im_data, im_geotrans, im_proj, path, nodata_value=0):
    # (此函数代码与原脚本一致，此处省略以保持简洁)
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
        im_bands, im_height, im_width = im_data.shape
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, int(im_width), int(im_height), int(im_bands), datatype)
    if dataset is not None:
        dataset.SetGeoTransform(im_geotrans)
        dataset.SetProjection(im_proj)
        for i in range(im_bands):
            band = dataset.GetRasterBand(i + 1)
            band.WriteArray(im_data[i])
            if nodata_value is not None:
                band.SetNoDataValue(nodata_value)
        del dataset


def calculate_k(c1_path, c2_path, output_path):
    # (此函数代码与原脚本一致)
    c1_ds = readTif(c1_path)
    c2_ds = readTif(c2_path)
    c1 = c1_ds.GetRasterBand(1).ReadAsArray()
    c2 = c2_ds.GetRasterBand(1).ReadAsArray()
    geo_transform = c1_ds.GetGeoTransform()
    projection = c1_ds.GetProjection()
    nodata_value = c1_ds.GetRasterBand(1).GetNoDataValue()
    k = np.full_like(c1, nodata_value, dtype=np.float32)
    valid_mask = (c1 != nodata_value) & (c2 != nodata_value)
    if np.any(valid_mask):
        k[valid_mask] = (114.8 * 10 ** (-0.6 + 1.26 * 0.01 * c2[valid_mask] - 6.4 * 0.001 * c1[valid_mask]))
    writeTiff(k, geo_transform, projection, output_path, nodata_value)


def calculate_water_retention(v_path, k_path, t1_path, y_path, output_path):
    # (此函数代码与原脚本一致)
    v_ds = readTif(v_path)
    k_ds = readTif(k_path)
    t1_ds = readTif(t1_path)
    y_ds = readTif(y_path)
    v = v_ds.GetRasterBand(1).ReadAsArray()
    k = k_ds.GetRasterBand(1).ReadAsArray()
    t1 = t1_ds.GetRasterBand(1).ReadAsArray()
    y = y_ds.GetRasterBand(1).ReadAsArray()
    geo_transform = v_ds.GetGeoTransform()
    projection = v_ds.GetProjection()
    nodata_value = v_ds.GetRasterBand(1).GetNoDataValue()
    wr = np.full_like(v, nodata_value, dtype=np.float32)
    valid_mask = (v != nodata_value) & (k != nodata_value) & (t1 != nodata_value) & (y != nodata_value)
    if np.any(valid_mask):
        wr[valid_mask] = (np.minimum(249 / v[valid_mask], 1) * np.minimum(0.3 * t1[valid_mask], 1) * np.minimum(1, k[
            valid_mask] / 300) * y[valid_mask])
    writeTiff(wr, geo_transform, projection, output_path, nodata_value)


# --- 主工作流函数 ---

def run(workspace_dir: str, lulc_path: str, depth_to_root_rest_layer_path: str,
        precipitation_path: str, eto_path: str, pawc_path: str,
        watersheds_path: str, biophysical_table_path: str,
        seasonality_constant: int, c1_path: str, c2_path: str,
        v_path: str, t_path: str):
    """
    执行完整的水源涵养量计算工作流。
    1. 运行 InVEST 产水量模型。
    2. 计算土壤饱和导水率 (K)。
    3. 基于前两步的结果计算最终的水源涵养量 (WR)。
    """
    # 1. 确保工作目录存在
    if not os.path.exists(workspace_dir):
        os.makedirs(workspace_dir)

    # 2. 运行 InVEST 产水量模型
    print("步骤 1/3: 正在运行 InVEST 产水量模型...")
    invest_args = {
        'workspace_dir': workspace_dir,
        'results_suffix': '',
        'lulc_path': lulc_path,
        'precipitation_path': precipitation_path,
        'eto_path': eto_path,
        'depth_to_root_rest_layer_path': depth_to_root_rest_layer_path,
        'pawc_path': pawc_path,
        'watersheds_path': watersheds_path,
        'biophysical_table_path': biophysical_table_path,
        'seasonality_constant': seasonality_constant,
    }
    annual_water_yield.execute(invest_args)

    # 3. 定义中间文件和最终输出文件的路径
    intermediate_dir = os.path.join(workspace_dir, "output", "per_pixel")
    k_path = os.path.join(intermediate_dir, "K_calculated.tif")
    y_path = os.path.join(intermediate_dir, "wyield.tif")  # InVEST产水量模型的输出
    final_output_path = os.path.join(workspace_dir, "water_retention_final.tif")

    # 检查产水量模型是否成功生成了输出
    if not os.path.exists(y_path):
        raise FileNotFoundError(f"InVEST产水量模型未能生成预期的输出文件: {y_path}")

    # 4. 计算土壤饱和导水率 K
    print("步骤 2/3: 正在计算土壤饱和导水率 K...")
    calculate_k(c1_path, c2_path, k_path)
    if not os.path.exists(k_path):
        raise FileNotFoundError(f"土壤饱和导水率结果文件未生成: {k_path}")

    # 5. 计算水源涵养量 WR
    print("步骤 3/3: 正在计算最终水源涵养量 WR...")
    calculate_water_retention(v_path, k_path, t_path, y_path, final_output_path)
    if not os.path.exists(final_output_path):
        raise RuntimeError(f"最终水源涵养量计算失败，未生成结果文件: {final_output_path}")

    # 6. 返回成功信息
    return f"水源涵养工作流全部完成！最终结果保存在: {final_output_path}"
