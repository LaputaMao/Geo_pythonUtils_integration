# # coding=utf-8
# import os
# import subprocess
# from tqdm import tqdm
#
# # 参数配置区域
# CONFIG = {
#     'WORK_DIR': r"E:\xhz\code\ANUSPLIN-master\data\jcy_gjc\\",  # 工作目录
#     'elev_range': (-400, 9000),  # DEM范围，默认值为(-400, 9000)   默认
#     'data_format': "(A6,2F11.4,F9.2,F8.2)",  # 输入data format字符串内容   默认
#     'clean_temp': False,  # 不用修改
#     'max_data_points': 500,  # 插值站点（采样点）最大数量   默认
#     'station_id_digits': 5,  # 台站号数字位数   默认
#     'dem_txt': 'dem_222_s.txt',  # 高程 DEM txt数据 文件名在工作目录下
# }
#
#
# # ===========================================================================================info: 1.在工作目录下放置两个.exe文件 2.文件名在工作目录下
#
# def read_dem_params(dem_file):
#     """读取 DEM txt 文件中的参数"""
#     with open(dem_file, 'r', encoding='utf-8') as f:
#         lines = f.readlines()
#         params = {}
#         for line in lines[:6]:  # 前6行包含所需参数
#             key, value = line.strip().split()
#             if key in ['xllcorner', 'yllcorner', 'cellsize', 'NODATA_value']:
#                 params[key] = float(value)
#             else:
#                 params[key] = int(value)
#     return params
#
#
# def modify_dem_file(dem_file, params):
#     """根据 cellsize 修改 xllcorner 和 yllcorner，并写回文件"""
#     cellsize = params['cellsize']
#     cellsize_str = str(float(cellsize)).split('.')
#     decimal_places = len(cellsize_str[1]) if len(cellsize_str) > 1 else 0
#
#     xllcorner = f"{params['xllcorner']:.{decimal_places}f}" + "0" * (12 - decimal_places - 2)
#     yllcorner = f"{params['yllcorner']:.{decimal_places}f}" + "0" * (12 - decimal_places - 2)
#
#     with open(dem_file, 'r', encoding='utf-8') as f:
#         lines = f.readlines()
#
#     for i, line in enumerate(lines):
#         if line.startswith('xllcorner'):
#             lines[i] = f"xllcorner {xllcorner}\n"
#         elif line.startswith('yllcorner'):
#             lines[i] = f"yllcorner {yllcorner}\n"
#
#     with open(dem_file, 'w', encoding='utf-8') as f:
#         f.writelines(lines)
#
#     return float(xllcorner), float(yllcorner)
#
#
# def calculate_ranges(params, xllcorner, yllcorner):
#     """根据 xllcorner、yllcorner、ncols、nrows 和 cellsize 计算 lon_range 和 lat_range"""
#     lon_min = xllcorner
#     lon_max = xllcorner + params['ncols'] * params['cellsize']
#     lat_min = yllcorner
#     lat_max = yllcorner + params['nrows'] * params['cellsize']
#     return (lon_min, lon_max), (lat_min, lat_max)
#
#
# def read_sur_params(sur_file_path):
#     """从 sur 文件中读取 lon_range_sur 和 lat_range_sur 参数"""
#     with open(sur_file_path, 'r', encoding='utf-8') as f:
#         lines = f.readlines()
#         lon_vals = lines[2].split()[:2]
#         lat_vals = lines[3].split()[:2]
#         lon_range_sur = (float(lon_vals[0]), float(lon_vals[1]))
#         lat_range_sur = (float(lat_vals[0]), float(lat_vals[1]))
#     return lon_range_sur, lat_range_sur
#
#
# def generate_splina_script(dat_file, output_base, lon_range, lat_range, elev_range, data_format, max_data_points,
#                            station_id_digits):
#     """生成 splina 的输入脚本"""
#     script_content = [
#         f"{output_base}",  # 文件名
#         "7",  # 单位：度
#         "2",  # 自变量个数（经纬度）
#         "1",  # 协变量个数（高程）
#         "0",  # 表面样条变量个数
#         "0",  # 表面协变量个数
#         f"{lon_range[0]} {lon_range[1]} 0 5",  # 经度范围
#         f"{lat_range[0]} {lat_range[1]} 0 5",  # 纬度范围
#         f"{elev_range[0]} {elev_range[1]} 1 1",  # 高程范围
#         "1000.0",  # dem的m转为km
#         "0",  # 独立变量转换参数
#         "3",  # 样条次数
#         "1",  # 输出表面个数
#         "0",  # 表面权重
#         "1",  # 优化方式
#         "1",  # 平滑方式
#         f"{dat_file}",  # 输入数据文件名
#         f"{max_data_points}",  # 数据点最大数量
#         f"{station_id_digits}",  # 台站号位数
#         f"{data_format}",  # 数据格式
#         f"{output_base}.res",  # 输出文件
#         f"{output_base}.opt",
#         f"{output_base}.sur",
#         f"{output_base}.lis",
#         f"{output_base}.cov",
#         "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""  # 结尾 6 空行
#     ]
#     script_file = f"{output_base}_splina.txt"
#     with open(script_file, "w") as f:
#         f.write("\n".join(script_content))
#     return script_file
#
#
# def generate_lapgrd_script(output_base, lon_range_sur, lat_range_sur, dem_txt, lapgrd_resolution, output_nodata):
#     """生成 lapgrd 的输入脚本"""
#     script_content = [
#         f"{output_base}.sur",  # 输入表面文件
#         "1",
#         "1",  # 输出一个面
#         f"{output_base}.cov",  # 输入协变量文件
#         "2",  # 误差计算方法
#         "",  # 标准差最大值(自动判定)
#         "1",  # 格网采样位置
#         "1",  # 第一栅格变量指标
#         f"{lon_range_sur[0]} {lon_range_sur[1]} {lapgrd_resolution}",  # 经度范围及分辨率
#         "2",  # 第二栅格变量指标
#         f"{lat_range_sur[0]} {lat_range_sur[1]} {lapgrd_resolution}",  # 纬度范围及分辨率
#         "0",  # 无掩膜文件
#         "2",  # 协变量数据格式
#         f"{dem_txt}",  # 高程文件
#         "2",  # 输出栅格格式
#         f"{output_nodata}",  # 空值数据
#         f"{output_base}.tif",  # 输出栅格文件名
#         "",  # 输出数值格式
#         "2",  # 重复输出栅格格式
#         f"{output_nodata}",  # 空值数据
#         f"{output_base}_cov.tif",  # 标准差文件名
#         "", "", "", "", "", "", "", "", "", "", "", ""  # 结尾 12 空行
#     ]
#     script_file = f"{output_base}_lapgrd.txt"
#     with open(script_file, "w") as f:
#         f.write("\n".join(script_content))
#     return script_file
#
#
# def run_anusplin_batch(config=CONFIG):
#     """批量运行 ANUSPLIN 和 lapgrd"""
#     os.makedirs(config['WORK_DIR'], exist_ok=True)
#     os.chdir(config['WORK_DIR'])
#     print(f"当前工作目录: {os.getcwd()}")
#
#     dem_files = [f for f in os.listdir(config['WORK_DIR']) if f.endswith(".txt")]
#     if not dem_files:
#         raise FileNotFoundError("No DEM txt file found in the working directory.")
#
#     dem_file = config.get('dem_txt', dem_files[0])
#     dem_path = os.path.join(config['WORK_DIR'], dem_file)
#     if not os.path.exists(dem_path):
#         raise FileNotFoundError(f"DEM txt file '{dem_path}' not found.")
#     print(f"使用 DEM 文件: {dem_path}")
#
#     dem_params = read_dem_params(dem_path)
#     xllcorner, yllcorner = modify_dem_file(dem_path, dem_params)
#     lon_range, lat_range = calculate_ranges(dem_params, xllcorner, yllcorner)
#     config['lon_range'] = lon_range
#     config['lat_range'] = lat_range
#
#     dat_files = [f for f in os.listdir(config['WORK_DIR']) if f.endswith(".dat")]
#     for dat_file in tqdm(dat_files, desc="Processing files"):
#         base_name = os.path.splitext(dat_file)[0]
#         output_dir = os.path.join(config['WORK_DIR'], base_name)
#         os.makedirs(output_dir, exist_ok=True)
#         output_base = os.path.join(output_dir, base_name)
#         print(f"处理文件: {dat_file}, 输出目录: {output_dir}")
#
#         splina_script = generate_splina_script(
#             dat_file,
#             output_base,
#             config['lon_range'],
#             config['lat_range'],
#             config['elev_range'],
#             config['data_format'],
#             config['max_data_points'],
#             config['station_id_digits']
#         )
#         try:
#             print(f"运行 splina: {splina_script}")
#             subprocess.run(["splina.exe"], stdin=open(splina_script, "r"), check=True)
#             print(f"splina 处理完成 for {dat_file}")
#         except subprocess.CalledProcessError as e:
#             print(f"运行 splina.exe 失败 for {dat_file}: {str(e)}")
#             continue
#         except FileNotFoundError:
#             print(f"splina.exe 未找到 for {dat_file}，请确保位于 {config['WORK_DIR']}")
#             continue
#
#         sur_file = f"{output_base}.sur"
#         if not os.path.exists(sur_file):
#             print(f"SUR 文件未找到: {sur_file}")
#             continue
#
#         try:
#             lon_range_sur, lat_range_sur = read_sur_params(sur_file)
#             print(f"处理 {dat_file}: lon_range_sur={lon_range_sur}, lat_range_sur={lat_range_sur}")
#         except Exception as e:
#             print(f"读取 SUR 文件失败 for {dat_file}: {str(e)}")
#             continue
#
#         lapgrd_script = generate_lapgrd_script(
#             output_base,
#             lon_range_sur,
#             lat_range_sur,
#             dem_file,
#             dem_params['cellsize'],
#             dem_params['NODATA_value']
#         )
#         try:
#             print(f"运行 lapgrd: {lapgrd_script}")
#             subprocess.run(["lapgrd.exe"], stdin=open(lapgrd_script, "r"), check=True)
#             print(f"lapgrd 处理完成 for {dat_file}, 输出: {output_base}.tif")
#         except subprocess.CalledProcessError as e:
#             print(f"运行 lapgrd.exe 失败 for {dat_file}: {str(e)}")
#             continue
#         except FileNotFoundError:
#             print(f"lapgrd.exe 未找到 for {dat_file}，请确保位于 {config['WORK_DIR']}")
#             continue
#
#         if config['clean_temp']:
#             os.remove(splina_script)
#             os.remove(lapgrd_script)
#
#     print("All tasks completed!")
#
#
# def main():
#     run_anusplin_batch()
#
#
# if __name__ == "__main__":
#     main()

# scripts/interpolation_model.py
# coding=utf-8
import os
import subprocess
import logging

# 配置日志记录，这比使用print更适合在模块化代码中进行调试
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# ===========================================================================================
# info: 1.本脚本被设计为由app.py调用，而非直接运行。
#      2.splina.exe 和 lapgrd.exe 文件需要由用户放置在指定的工作目录中。
# ===========================================================================================

def read_dem_params(dem_file_path):
    """读取 DEM txt 文件中的参数"""
    with open(dem_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        params = {}
        for line in lines[:6]:
            try:
                key, value = line.strip().split()
                if key in ['xllcorner', 'yllcorner', 'cellsize', 'NODATA_value']:
                    params[key] = float(value)
                else:
                    params[key] = int(value)
            except ValueError:
                logging.warning(f"无法解析行: {line.strip()}")
                continue
    return params


def modify_dem_file(dem_file_path, params):
    """根据 cellsize 修改 xllcorner 和 yllcorner，并写回文件"""
    cellsize = params.get('cellsize', 0.0)
    cellsize_str = str(float(cellsize)).split('.')
    decimal_places = len(cellsize_str[1]) if len(cellsize_str) > 1 else 0

    xllcorner_val = params.get('xllcorner', 0.0)
    yllcorner_val = params.get('yllcorner', 0.0)

    # 格式化字符串以匹配原始脚本的逻辑
    xllcorner_str = f"{xllcorner_val:.{decimal_places}f}"
    yllcorner_str = f"{yllcorner_val:.{decimal_places}f}"

    with open(dem_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip().lower().startswith('xllcorner'):
            lines[i] = f"xllcorner      {xllcorner_str}\n"
        elif line.strip().lower().startswith('yllcorner'):
            lines[i] = f"yllcorner      {yllcorner_str}\n"

    with open(dem_file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    return float(xllcorner_val), float(yllcorner_val)


def calculate_ranges(params, xllcorner, yllcorner):
    """根据参数计算经纬度范围"""
    lon_min = xllcorner
    lon_max = xllcorner + params['ncols'] * params['cellsize']
    lat_min = yllcorner
    lat_max = yllcorner + params['nrows'] * params['cellsize']
    return (lon_min, lon_max), (lat_min, lat_max)


def read_sur_params(sur_file_path):
    """从 sur 文件中读取经纬度范围参数"""
    with open(sur_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lon_vals = lines[2].split()[:2]
        lat_vals = lines[3].split()[:2]
        lon_range_sur = (float(lon_vals[0]), float(lon_vals[1]))
        lat_range_sur = (float(lat_vals[0]), float(lat_vals[1]))
    return lon_range_sur, lat_range_sur


def generate_splina_script(script_path, dat_file_name, output_base_relative, lon_range, lat_range, elev_range,
                           data_format,
                           max_data_points, station_id_digits):
    """生成 splina 的输入脚本"""
    script_content = [
        f"{output_base_relative}", "7", "2", "1", "0", "0",
        f"{lon_range[0]} {lon_range[1]} 0 5",
        f"{lat_range[0]} {lat_range[1]} 0 5",
        f"{elev_range[0]} {elev_range[1]} 1 1",
        "1000.0", "0", "3", "1", "0", "1", "1",
        f"{dat_file_name}",
        f"{max_data_points}",
        f"{station_id_digits}",
        f"{data_format}",
        f"{output_base_relative}.res",
        f"{output_base_relative}.opt",
        f"{output_base_relative}.sur",
        f"{output_base_relative}.lis",
        f"{output_base_relative}.cov",
        "\n" * 16
    ]
    with open(script_path, "w") as f:
        f.write("\n".join(script_content))
    return script_path


def generate_lapgrd_script(script_path, output_base_relative, lon_range_sur, lat_range_sur, dem_txt_filename,
                           lapgrd_resolution, output_nodata):
    """生成 lapgrd 的输入脚本"""
    script_content = [
        f"{output_base_relative}.sur", "1", "1", f"{output_base_relative}.cov", "2", "", "1", "1",
        f"{lon_range_sur[0]} {lon_range_sur[1]} {lapgrd_resolution}", "2",
        f"{lat_range_sur[0]} {lat_range_sur[1]} {lapgrd_resolution}", "0", "2",
        f"{dem_txt_filename}", "2",
        f"{output_nodata}",
        f"{output_base_relative}.tif", "", "2",
        f"{output_nodata}",
        f"{output_base_relative}_cov.tif",
        "\n" * 12
    ]
    with open(script_path, "w") as f:
        f.write("\n".join(script_content))
    return script_path


def run(work_dir, dem_txt_filename, elev_range, data_format, max_data_points, station_id_digits, clean_temp=False):
    """
    重构后的主函数，用于批量运行 ANUSPLIN 插值。
    此函数被设计为从外部（如Streamlit App）调用。
    """
    # --- 1. 验证输入路径和文件 ---
    if not os.path.isdir(work_dir):
        raise FileNotFoundError(f"错误：提供的工作目录不存在: {work_dir}")

    splina_exe_path = os.path.join(work_dir, "splina.exe")
    lapgrd_exe_path = os.path.join(work_dir, "lapgrd.exe")
    if not os.path.exists(splina_exe_path) or not os.path.exists(lapgrd_exe_path):
        raise FileNotFoundError("错误：请确保 'splina.exe' 和 'lapgrd.exe' 文件存在于工作目录中。")

    dem_path = os.path.join(work_dir, dem_txt_filename)
    if not os.path.exists(dem_path):
        raise FileNotFoundError(f"错误：DEM txt 文件 '{dem_txt_filename}' 在工作目录中未找到。")

    dat_files = [f for f in os.listdir(work_dir) if f.endswith(".dat")]
    if not dat_files:
        raise FileNotFoundError(f"错误：在工作目录 {work_dir} 中没有找到任何 .dat 文件。")

    logging.info(f"工作目录设置为: {work_dir}")

    # --- 2. 准备 DEM 文件 ---
    dem_params = read_dem_params(dem_path)
    xllcorner, yllcorner = modify_dem_file(dem_path, dem_params)
    lon_range, lat_range = calculate_ranges(dem_params, xllcorner, yllcorner)

    # --- 3. 循环处理每个.dat文件 ---
    for dat_file in dat_files:
        base_name = os.path.splitext(dat_file)[0]

        # 创建一个相对于工作目录的输出子目录
        output_subdir_relative = base_name
        output_subdir_absolute = os.path.join(work_dir, output_subdir_relative)
        os.makedirs(output_subdir_absolute, exist_ok=True)

        # 所有在脚本中使用的路径都应是相对于工作目录的
        output_base_relative = os.path.join(output_subdir_relative, base_name).replace('\\', '/')

        logging.info(f"正在处理文件: {dat_file}, 输出到: {output_subdir_absolute}")

        # --- 4. 运行 splina.exe ---
        splina_script_path = os.path.join(work_dir, f"{base_name}_splina.txt")
        generate_splina_script(
            splina_script_path, dat_file, output_base_relative, lon_range, lat_range, elev_range,
            data_format, max_data_points, station_id_digits
        )
        try:
            logging.info(f"运行 splina for {dat_file}...")
            # 使用 cwd 参数来在指定目录下执行命令，这是比 os.chdir 更安全的方式
            subprocess.run([splina_exe_path], stdin=open(splina_script_path, "r"), check=True, cwd=work_dir,
                           capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            error_message = f"运行 splina.exe 失败 for {dat_file}: {e.stderr}"
            logging.error(error_message)
            raise RuntimeError(error_message)

        # --- 5. 运行 lapgrd.exe ---
        sur_file_path = os.path.join(work_dir, f"{output_base_relative}.sur")
        if not os.path.exists(sur_file_path):
            logging.warning(f"SUR 文件未找到: {sur_file_path}, 跳过 lapgrd 步骤。")
            continue

        try:
            lon_range_sur, lat_range_sur = read_sur_params(sur_file_path)
        except Exception as e:
            error_message = f"读取 SUR 文件失败 for {dat_file}: {str(e)}"
            logging.error(error_message)
            raise RuntimeError(error_message)

        lapgrd_script_path = os.path.join(work_dir, f"{base_name}_lapgrd.txt")
        generate_lapgrd_script(
            lapgrd_script_path, output_base_relative, lon_range_sur, lat_range_sur, dem_txt_filename,
            dem_params['cellsize'], dem_params['NODATA_value']
        )
        try:
            logging.info(f"运行 lapgrd for {dat_file}...")
            subprocess.run([lapgrd_exe_path], stdin=open(lapgrd_script_path, "r"), check=True, cwd=work_dir,
                           capture_output=True, text=True)
            logging.info(f"成功生成: {output_base_relative}.tif")
        except subprocess.CalledProcessError as e:
            error_message = f"运行 lapgrd.exe 失败 for {dat_file}: {e.stderr}"
            logging.error(error_message)
            raise RuntimeError(error_message)

        # --- 6. 清理临时脚本文件 ---
        if clean_temp:
            os.remove(splina_script_path)
            os.remove(lapgrd_script_path)

    return "所有插值任务已成功完成！"