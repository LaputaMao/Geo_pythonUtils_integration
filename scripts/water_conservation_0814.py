# import os
# from natcap.invest import annual_water_yield
# import sys
#
# def run_annual_water_yield_model(workspace_dir, lulc_path, depth_to_root_rest_layer_path, precipitation_path, eto_path, pawc_path, watersheds_path, biophysical_table_path, seasonality_constant, alpha_m, beta_i, gamma):
#     # 定义模型参数
#     args = {
#         'workspace_dir': workspace_dir,
#         'results_suffix': '',
#         'lulc_path': lulc_path,
#         'precipitation_path': precipitation_path,
#         'eto_path': eto_path,
#         'depth_to_root_rest_layer_path': depth_to_root_rest_layer_path,
#         'pawc_path': pawc_path,
#         'watersheds_path': watersheds_path,
#         'biophysical_table_path': biophysical_table_path,
#         'seasonality_constant': seasonality_constant,
#         'alpha_m': alpha_m,
#         'beta_i': beta_i,
#         'gamma': gamma,
#         'user_defined_climate_zones': False,
#         'user_defined_climate_zones_path': '',
#         'monthly_alpha': False,
#         'monthly_alpha_path': '',
#         'rain_events_table_path': '',
#     }
#
#     # 创建工作目录
#     if not os.path.exists(workspace_dir):
#         os.makedirs(workspace_dir)
#
#     # 运行模型
#     annual_water_yield.execute(args)
#
# if __name__ == "__main__":
#     # 从命令行获取参数
#     if len(sys.argv) != 12:
#         print("用法: python script.py <workspace_dir> <lulc_path> <depth_to_root_rest_layer_path> <precipitation_path> <eto_path> <pawc_path> <watersheds_path> <biophysical_table_path> <seasonality_constant> <alpha_m> <beta_i> <gamma>")
#         sys.exit(1)
#
#     workspace_dir = r""
#     lulc_path = sys.argv[2]
#     depth_to_root_rest_layer_path = sys.argv[3]
#     precipitation_path = sys.argv[4]
#     eto_path = sys.argv[5]
#     pawc_path = sys.argv[6]
#     watersheds_path = sys.argv[7]
#     biophysical_table_path = sys.argv[8]
#     seasonality_constant = float(sys.argv[9])
#     alpha_m = float(sys.argv[10])
#     beta_i = float(sys.argv[11])
#     gamma = float(sys.argv[12])
#
#     run_annual_water_yield_model(workspace_dir, lulc_path, depth_to_root_rest_layer_path, precipitation_path, eto_path, pawc_path, watersheds_path, biophysical_table_path, seasonality_constant, alpha_m, beta_i, gamma)

# scripts/annual_water_yield_model.py
# -*- coding: utf-8 -*-
import os
from natcap.invest import annual_water_yield

def run(workspace_dir: str,
        lulc_path: str,
        depth_to_root_rest_layer_path: str,
        precipitation_path: str,
        eto_path: str,
        pawc_path: str,
        watersheds_path: str,
        biophysical_table_path: str,
        seasonality_constant: float,
        alpha_m: float,
        beta_i: float,
        gamma: float):
    """
    运行 InVEST 产水量模型的核心逻辑函数。
    """
    # 1. 定义模型参数字典
    # 注意：我们保留了对高级选项的硬编码（设为False或空），只暴露了核心参数
    args = {
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
        'alpha_m': alpha_m,
        'beta_i': beta_i,
        'gamma': gamma,
        'user_defined_climate_zones': False,
        'user_defined_climate_zones_path': '',
        'monthly_alpha': False,
        'monthly_alpha_path': '',
        'rain_events_table_path': '',
    }

    # 2. 确保工作目录存在
    # 使用 exist_ok=True 可以简化代码，如果目录已存在则不会报错
    os.makedirs(workspace_dir, exist_ok=True)

    # 3. 执行模型，让异常自然抛出给调用者
    annual_water_yield.execute(args)

    # 4. 如果执行成功，返回一个成功信息
    return f"产水量模型运行成功！结果已保存在目录: {workspace_dir}"

# 删除了所有 if __name__ == "__main__": 和 sys.argv 相关的代码
