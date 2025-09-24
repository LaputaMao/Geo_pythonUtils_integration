# import os
# import sys
# from osgeo import gdal
# import numpy as np
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
# def writeTiff(im_data, im_geotrans, im_proj, path, nodata_value=-9999):
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
# # 计算风力因子Wf的函数
# def calculate_Wf(U1, U2_path, Nd, output_path):
#     # 读取数据集
#     U2_ds = readTif(U2_path)
#
#     # 读取栅格数据为数组
#     U2 = U2_ds.GetRasterBand(1).ReadAsArray()
#
#     # 计算风力因子Wf
#     Wf = U2 * (U2 - U1)**2 * Nd
#
#     # 处理 NaN 值，将其设置为 NoData
#     Wf[np.isnan(Wf)] = -9999  # 设置一个常见的 NoData 值
#     Wf[np.isinf(Wf)] = -9999  # 设置一个常见的 NoData 值
#     no_data_value = -9999
#
#     # 获取仿射变换参数和投影信息
#     geotransform = U2_ds.GetGeoTransform()
#     projection = U2_ds.GetProjection()
#
#     # 保存计算结果为tif文件
#     writeTiff(Wf, geotransform, projection, output_path)
#
#     # 返回计算的Wf矩阵
#     return Wf
#
#
# # 计算土壤湿度因子SW的函数
# def calculate_SW(ETp_path, R_path, I_path, Rd, output_path, N=365):
#     # 读取数据集
#     ETp_ds = readTif(ETp_path)
#     R_ds = readTif(R_path)
#     I_ds = readTif(I_path)
#
#     # 读取栅格数据为数组
#     ETp = ETp_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
#     R = R_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
#     I = I_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
#
#     # ###############################
#     # ###############################
#     # ###############################
#     # # 只在演示数据集中保留，记得删！！！！！
#     # # 只在演示数据集中保留，记得删！！！！！
#     # # 只在演示数据集中保留，记得删！！！！！
#     # ETp = ETp * 12
#     # Rd = Rd * 14
#     # ###############################
#     # ###############################
#     # ###############################
#
#     # 计算土壤湿度因子SW
#     SW = (ETp - ((R + I) * Rd / N)) / ETp
#
#     # 处理 NaN 值，将其设置为 NoData
#     SW[np.isnan(SW)] = -9999  # 设置一个常见的 NoData 值
#     SW[np.isinf(SW)] = -9999  # 设置一个常见的 NoData 值
#     no_data_value = -9999
#
#     # 获取仿射变换参数和投影信息
#     geotransform = ETp_ds.GetGeoTransform()
#     projection = ETp_ds.GetProjection()
#
#     # 保存计算结果为tif文件
#     writeTiff(SW, geotransform, projection, output_path)
#
#     # 返回计算的SW矩阵
#     return SW
#
#
# # 计算气象因子WF的函数
# def calculate_WF(Wf, rho, SW, SD_path, g, output_path):
#     # 判断rho和g是常数还是tif文件路径
#     if isinstance(rho, str):
#         rho_ds = readTif(rho)
#         rho = rho_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
#     if isinstance(g, str):
#         g_ds = readTif(g)
#         g = g_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
#
#     # 读取栅格数据为数组
#     SD_ds = readTif(SD_path)
#     SD = SD_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
#
#     # 计算气象因子WF
#     WF = (Wf * rho * SW * SD) / g
#
#     # 处理 NaN 值，将其设置为 NoData
#     WF[np.isnan(WF)] = -9999  # 设置一个常见的 NoData 值
#     WF[np.isinf(WF)] = -9999  # 设置一个常见的 NoData 值
#
#     # 排除掉大于10000和小于-10000的值
#     WF[(WF > 1000) | (WF < -1000)] = -9999  # 将这些异常值也设置为 NoData
#
#     # 获取仿射变换参数和投影信息
#     geotransform = SD_ds.GetGeoTransform()
#     projection = SD_ds.GetProjection()
#
#     # 保存计算结果为tif文件
#     writeTiff(WF, geotransform, projection, output_path)
#
#     # 返回计算的WF矩阵
#     return WF
#
#
# # 计算土壤可蚀性因子EF的函数
# def calculate_EF(sa_path, si_path, cl_path, om_path, output_path=None):
#     # 读取数据集
#     sa_ds = readTif(sa_path)
#     si_ds = readTif(si_path)
#     cl_ds = readTif(cl_path)
#     om_ds = readTif(om_path)
#
#     # 读取栅格数据为数组
#     sa = sa_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
#     si = si_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
#     cl = cl_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
#     om = om_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
#
#     # 根据国标要求，数据转化为百分比（0~100 to 0~1）
#     sa = sa / 100
#     si = si / 100
#     cl = cl / 100
#     om = om / 100
#
#     # 计算土壤可蚀性因子EF
#     EF = (29.09 + 0.31 * sa + 0.17 * si + 0.33 * (sa / cl) + 2.59 * om) / 100
#
#     # 处理 NaN 值，将其设置为 NoData
#     EF[np.isnan(EF)] = -9999  # 设置一个常见的 NoData 值
#     EF[np.isinf(EF)] = -9999  # 设置一个常见的 NoData 值
#
#     # 排除掉大于1000和小于0的值
#     EF[(EF > 1000) | (EF < 0)] = -9999  # 将这些异常值也设置为 NoData
#
#     # 如果提供了输出路径，则保存结果
#     if output_path is not None:
#         # 获取仿射变换参数和投影信息
#         geotransform = sa_ds.GetGeoTransform()
#         projection = sa_ds.GetProjection()
#         writeTiff(EF, geotransform, projection, output_path)
#
#     # 返回计算的EF矩阵
#     return EF
#
#
# # 计算土壤结皮因子SCF的函数
# def calculate_SCF(cl_path, om_path, output_path=None):
#     # 读取数据集
#     cl_ds = readTif(cl_path)
#     om_ds = readTif(om_path)
#
#     # 读取栅格数据为数组
#     cl = cl_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
#     om = om_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
#
#     # 计算土壤结皮因子SCF
#     SCF = 1 / (1 + 0.0066 * cl**2 + 0.021 * om**2)
#
#     # 处理 NaN 值，将其设置为 NoData
#     SCF[np.isnan(SCF)] = -9999  # 设置一个常见的 NoData 值
#     SCF[np.isinf(SCF)] = -9999  # 设置一个常见的 NoData 值
#
#     # 排除掉大于1和小于等于0的值
#     SCF[(SCF > 1) | (SCF <= 0)] = -9999  # 将这些异常值也设置为 NoData
#
#     # 如果提供了输出路径，则保存结果
#     if output_path is not None:
#         # 获取仿射变换参数和投影信息
#         geotransform = cl_ds.GetGeoTransform()
#         projection = cl_ds.GetProjection()
#         writeTiff(SCF, geotransform, projection, output_path)
#
#     # 返回计算的SCF矩阵
#     return SCF
#
#
# # 计算防风固沙量SR的综合函数
# def calculate_SR(WF, EF, SCF, K_path, C_path, output_path=None):
#     # 读取K和C因子的数据集
#     K_ds = readTif(K_path)
#     C_ds = readTif(C_path)
#
#     # 读取栅格数据为数组
#     K = K_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
#     C = C_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
#
#     # 常量z
#     z = 50
#
#     # 计算Sp和QMAXp
#     Sp = 150.71 * (WF * EF * SCF * K)**-0.3711
#     QMAXp = 109.8 * (WF * EF * SCF * K)
#
#     # 计算SLp
#     SLp = (2 * z / Sp**2) * QMAXp * np.exp(-(z / Sp)**2)
#
#     # 计算S和QMAX
#     S = 150.71 * (WF * EF * SCF * K * C)**-0.3711
#     QMAX = 109.8 * (WF * EF * SCF * K * C)
#
#     # 计算SL
#     SL = (2 * z / S**2) * QMAX * np.exp(-(z / S)**2)
#
#     # 计算SR
#     SR = SLp - SL
#
#     # 处理 NaN 值，将其设置为 NoData
#     SR[np.isnan(SR)] = -9999  # 设置一个常见的 NoData 值
#
#     # 如果提供了输出路径，则保存结果
#     if output_path is not None:
#         # 获取仿射变换参数和投影信息
#         geotransform = K_ds.GetGeoTransform()
#         projection = K_ds.GetProjection()
#         writeTiff(SR, geotransform, projection, output_path)
#
#     # 返回计算的SR矩阵
#     return SR
#
#
# def run_sand_break_model(output_folder, U1_path, U2_path, Nd_path, ETp_path, R_path, I_path, Rd_path, N, rho_path, SD_path, g, sa_path, si_path, cl_path, om_path, K_path, C_path, status_label, root):
#     # 显示状态提示
#     status_label.config(text="模型正在运行，请稍候...")
#     root.update_idletasks()
#
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
#
#     intermediate_output_folder = os.path.join(output_folder, "intermediate_outputs")
#     if not os.path.exists(intermediate_output_folder):
#         os.makedirs(intermediate_output_folder)
#
#     # 输出路径设置
#     Wf_path = os.path.join(intermediate_output_folder, "wf_output.tif")
#     SW_path = os.path.join(intermediate_output_folder, "SW_output.tif")
#     WF_path = os.path.join(intermediate_output_folder, "WF_output.tif")
#     EF_path = os.path.join(intermediate_output_folder, "EF_output.tif")
#     SCF_path = os.path.join(intermediate_output_folder, "SCF_output.tif")
#     SR_path = os.path.join(output_folder, "SR_output.tif")
#
#     # 计算各项
#     try:
#         Wf = calculate_Wf(U1_path, U2_path, Nd_path, Wf_path)
#         SW = calculate_SW(ETp_path, R_path, I_path, Rd_path, SW_path, N)
#         WF = calculate_WF(Wf, rho_path, SW, SD_path, g, WF_path)
#         EF = calculate_EF(sa_path, si_path, cl_path, om_path, EF_path)
#         SCF = calculate_SCF(cl_path, om_path, SCF_path)
#         SR = calculate_SR(WF, EF, SCF, K_path, C_path, SR_path)
#
#         messagebox.showinfo("运行完成", "防风固沙模型运行完成。")
#     except Exception as e:
#         messagebox.showerror("运行错误", f"模型运行出错: {str(e)}")
#     finally:
#         root.destroy()
#
#
# if __name__ == "__main__":
#     if len(sys.argv) != 19:
#         print("用法: python sand_break.py <output_folder> <U1> <U2> <Nd> <ETp> <R> <I> <Rd> <N> <rho> <SD> <g> <sa> <si> <cl> <om> <K> <C>")
#         sys.exit(1)
#
#     output_folder = sys.argv[1]
#     U1_path = float(sys.argv[2])
#     U2_path = sys.argv[3]
#     Nd_path = int(sys.argv[4])
#     ETp_path = sys.argv[5]
#     R_path = sys.argv[6]
#     I_path = sys.argv[7]
#     Rd_path = int(sys.argv[8])
#     N = int(sys.argv[9])
#     rho_path = sys.argv[10]
#     SD_path = sys.argv[11]
#     g = sys.argv[12]
#     sa_path = sys.argv[13]
#     si_path = sys.argv[14]
#     cl_path = sys.argv[15]
#     om_path = sys.argv[16]
#     K_path = sys.argv[17]
#     C_path = sys.argv[18]
#
#     if g[0].isdigit() or (g[0] == '-' and len(g) > 1 and g[1].isdigit()):
#         g = float(g)
#     if rho_path[0].isdigit() or (rho_path[0] == '-' and len(rho_path) > 1 and rho_path[1].isdigit()):
#         rho_path = float(rho_path)
#
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
#     # 在100ms后启动模型运行
#     root.after(100, run_sand_break_model, output_folder, U1_path, U2_path, Nd_path, ETp_path, R_path, I_path, Rd_path, N, rho_path, SD_path, g, sa_path, si_path, cl_path, om_path, K_path, C_path, status_label, root)
#     root.mainloop()
#

# scripts/sand_break_model.py
import os
from osgeo import gdal
import numpy as np
from typing import Union

# ===================================================================
# 以下所有辅助函数和计算函数 (readTif, writeTiff, calculate_Wf, etc.)
# 保持原样，无需任何修改。这里为了简洁省略，实际文件中需要保留它们。
# ... (此处省略了 readTif, writeTiff, calculate_Wf, SW, WF, EF, SCF, SR 函数)
# ===================================================================

# 读取tif数据集
def readTif(fileName):
    dataset = gdal.Open(fileName)
    if dataset is None:
        # 在模块化代码中，打印并抛出异常是更好的做法
        error_msg = f"{fileName} 文件无法打开或不存在。"
        print(error_msg)
        raise FileNotFoundError(error_msg)
    return dataset


# 保存tif文件函数
def writeTiff(im_data, im_geotrans, im_proj, path, nodata_value=-9999):
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

# ... 此处应包含你所有的 calculate_* 函数 ...
# (为了简洁，我只复制了几个作为示例，你需要把它们都放进来)
def calculate_Wf(U1, U2_path, Nd, output_path):
    U2_ds = readTif(U2_path)
    U2 = U2_ds.GetRasterBand(1).ReadAsArray()
    Wf = U2 * (U2 - U1)**2 * Nd
    Wf[np.isnan(Wf)] = -9999
    Wf[np.isinf(Wf)] = -9999
    geotransform = U2_ds.GetGeoTransform()
    projection = U2_ds.GetProjection()
    writeTiff(Wf, geotransform, projection, output_path)
    return Wf

def calculate_SW(ETp_path, R_path, I_path, Rd, output_path, N=365):
    ETp_ds = readTif(ETp_path)
    R_ds = readTif(R_path)
    I_ds = readTif(I_path)
    ETp = ETp_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
    R = R_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
    I = I_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
    SW = (ETp - ((R + I) * Rd / N)) / ETp
    SW[np.isnan(SW)] = -9999
    SW[np.isinf(SW)] = -9999
    geotransform = ETp_ds.GetGeoTransform()
    projection = ETp_ds.GetProjection()
    writeTiff(SW, geotransform, projection, output_path)
    return SW

# 计算气象因子WF的函数
def calculate_WF(Wf, rho, SW, SD_path, g, output_path):
    # 判断rho和g是常数还是tif文件路径
    if isinstance(rho, str):
        rho_ds = readTif(rho)
        rho = rho_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
    if isinstance(g, str):
        g_ds = readTif(g)
        g = g_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)

    # 读取栅格数据为数组
    SD_ds = readTif(SD_path)
    SD = SD_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)

    # 计算气象因子WF
    WF = (Wf * rho * SW * SD) / g

    # 处理 NaN 值，将其设置为 NoData
    WF[np.isnan(WF)] = -9999  # 设置一个常见的 NoData 值
    WF[np.isinf(WF)] = -9999  # 设置一个常见的 NoData 值

    # 排除掉大于10000和小于-10000的值
    WF[(WF > 1000) | (WF < -1000)] = -9999  # 将这些异常值也设置为 NoData

    # 获取仿射变换参数和投影信息
    geotransform = SD_ds.GetGeoTransform()
    projection = SD_ds.GetProjection()

    # 保存计算结果为tif文件
    writeTiff(WF, geotransform, projection, output_path)

    # 返回计算的WF矩阵
    return WF


# 计算土壤可蚀性因子EF的函数
def calculate_EF(sa_path, si_path, cl_path, om_path, output_path=None):
    # 读取数据集
    sa_ds = readTif(sa_path)
    si_ds = readTif(si_path)
    cl_ds = readTif(cl_path)
    om_ds = readTif(om_path)

    # 读取栅格数据为数组
    sa = sa_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
    si = si_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
    cl = cl_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
    om = om_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)

    # 根据国标要求，数据转化为百分比（0~100 to 0~1）
    sa = sa / 100
    si = si / 100
    cl = cl / 100
    om = om / 100

    # 计算土壤可蚀性因子EF
    EF = (29.09 + 0.31 * sa + 0.17 * si + 0.33 * (sa / cl) + 2.59 * om) / 100

    # 处理 NaN 值，将其设置为 NoData
    EF[np.isnan(EF)] = -9999  # 设置一个常见的 NoData 值
    EF[np.isinf(EF)] = -9999  # 设置一个常见的 NoData 值

    # 排除掉大于1000和小于0的值
    EF[(EF > 1000) | (EF < 0)] = -9999  # 将这些异常值也设置为 NoData

    # 如果提供了输出路径，则保存结果
    if output_path is not None:
        # 获取仿射变换参数和投影信息
        geotransform = sa_ds.GetGeoTransform()
        projection = sa_ds.GetProjection()
        writeTiff(EF, geotransform, projection, output_path)

    # 返回计算的EF矩阵
    return EF


# 计算土壤结皮因子SCF的函数
def calculate_SCF(cl_path, om_path, output_path=None):
    # 读取数据集
    cl_ds = readTif(cl_path)
    om_ds = readTif(om_path)

    # 读取栅格数据为数组
    cl = cl_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
    om = om_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)

    # 计算土壤结皮因子SCF
    SCF = 1 / (1 + 0.0066 * cl**2 + 0.021 * om**2)

    # 处理 NaN 值，将其设置为 NoData
    SCF[np.isnan(SCF)] = -9999  # 设置一个常见的 NoData 值
    SCF[np.isinf(SCF)] = -9999  # 设置一个常见的 NoData 值

    # 排除掉大于1和小于等于0的值
    SCF[(SCF > 1) | (SCF <= 0)] = -9999  # 将这些异常值也设置为 NoData

    # 如果提供了输出路径，则保存结果
    if output_path is not None:
        # 获取仿射变换参数和投影信息
        geotransform = cl_ds.GetGeoTransform()
        projection = cl_ds.GetProjection()
        writeTiff(SCF, geotransform, projection, output_path)

    # 返回计算的SCF矩阵
    return SCF


# 计算防风固沙量SR的综合函数
def calculate_SR(WF, EF, SCF, K_path, C_path, output_path=None):
    # 读取K和C因子的数据集
    K_ds = readTif(K_path)
    C_ds = readTif(C_path)

    # 读取栅格数据为数组
    K = K_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
    C = C_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)

    # 常量z
    z = 50

    # 计算Sp和QMAXp
    Sp = 150.71 * (WF * EF * SCF * K)**-0.3711
    QMAXp = 109.8 * (WF * EF * SCF * K)

    # 计算SLp
    SLp = (2 * z / Sp**2) * QMAXp * np.exp(-(z / Sp)**2)

    # 计算S和QMAX
    S = 150.71 * (WF * EF * SCF * K * C)**-0.3711
    QMAX = 109.8 * (WF * EF * SCF * K * C)

    # 计算SL
    SL = (2 * z / S**2) * QMAX * np.exp(-(z / S)**2)

    # 计算SR
    SR = SLp - SL

    # 处理 NaN 值，将其设置为 NoData
    SR[np.isnan(SR)] = -9999  # 设置一个常见的 NoData 值

    # 如果提供了输出路径，则保存结果
    if output_path is not None:
        # 获取仿射变换参数和投影信息
        geotransform = K_ds.GetGeoTransform()
        projection = K_ds.GetProjection()
        writeTiff(SR, geotransform, projection, output_path)

    # 返回计算的SR矩阵
    return SR

def run(output_folder: str,
        U1: float,
        U2_path: str,
        Nd: int,
        ETp_path: str,
        R_path: str,
        I_path: str,
        Rd: int,
        N: int,
        rho: Union[float, str],
        SD_path: str,
        g: Union[float, str],
        sa_path: str,
        si_path: str,
        cl_path: str,
        om_path: str,
        K_path: str,
        C_path: str):
    """
    运行防风固沙模型的核心逻辑函数。
    """
    # 1. 创建输出目录
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    intermediate_output_folder = os.path.join(output_folder, "intermediate_outputs")
    if not os.path.exists(intermediate_output_folder):
        os.makedirs(intermediate_output_folder)

    # 2. 定义所有中间文件和最终文件的输出路径
    Wf_path = os.path.join(intermediate_output_folder, "wf_output.tif")
    SW_path = os.path.join(intermediate_output_folder, "SW_output.tif")
    WF_path = os.path.join(intermediate_output_folder, "WF_output.tif")
    EF_path = os.path.join(intermediate_output_folder, "EF_output.tif")
    SCF_path = os.path.join(intermediate_output_folder, "SCF_output.tif")
    SR_path = os.path.join(output_folder, "SR_output.tif")

    # 3. 按顺序执行所有计算步骤
    # 注意：我们不再捕获异常，让它直接抛给 app.py
    Wf = calculate_Wf(U1, U2_path, Nd, Wf_path)
    SW = calculate_SW(ETp_path, R_path, I_path, Rd, SW_path, N)
    WF = calculate_WF(Wf, rho, SW, SD_path, g, WF_path)
    EF = calculate_EF(sa_path, si_path, cl_path, om_path, EF_path)
    SCF = calculate_SCF(cl_path, om_path, SCF_path)
    SR = calculate_SR(WF, EF, SCF, K_path, C_path, SR_path)

    # 4. 返回成功信息
    return f"防风固沙模型运行成功！最终结果已保存在: {SR_path}"

# 同样，删除了 run_sand_break_model 函数和整个 if __name__ == "__main__": 部分。
