# # app.py
# import streamlit as st
# from scripts import soil_conservation, sand_break, carbon_storage, water_conservation  # 从scripts文件夹导入你的脚本模块
#
# # --- 页面基础设置 ---
# st.set_page_config(
#     page_title="Python模型库",
#     page_icon="🛠️",
#     layout="centered"
# )
#
# st.title("🛠️ Python 模型库")
#
# # --- 使用侧边栏进行导航 ---
# # 使用 Markdown 和 CSS 控制间距
# st.markdown("""
# <style>
# .stRadio > label {
#     font-size: 30px; /* 字体大小 */
#     padding-top: 20px; /* 上间距 */
#     padding-bottom: 20px; /* 下间距 */
# }
#
#
# </style>
# """, unsafe_allow_html=True)
#
# st.sidebar.title("生态系统服务功能模型")
# script_choice = st.sidebar.radio(
#     "请选择要使用的模型:",
#     ('模型一：碳储量', '模型二：防风固沙', '模型三：土壤保持', '模型四：水源涵养', '模型五：内插模型')
# )
# # --- 根据选择显示不同的UI界面 ---
#
# if script_choice == '模型一：碳储量':
#     st.header("模型一：碳储量")
#     st.info("这是一个用于计算碳储量和固碳量的模型。请输入必要的路径和参数。")
#
#     # 为 task1 创建参数输入框
#     # param_a = st.text_input("请输入字符串参数 (Parameter A)", "hello")
#
#     # --- 使用表单来组织输入 ---
#     with st.form("carbon_form"):
#         st.subheader("必填参数")
#         workspace_dir = st.text_input("1. 工作空间目录 (存放结果的文件夹路径)", "/your/project/path")
#         lulc_cur_path = st.text_input("2. 当前土地利用/覆盖数据路径 (.tif)")
#         carbon_pools_path = st.text_input("3. 碳库路径 (.csv)")
#
#         st.subheader("可选参数")
#         lulc_fut_path = st.text_input("4. 未来土地利用/覆盖数据路径 (.tif, 用于计算固碳量)")
#         lulc_redd_path = st.text_input("5. REDD情景土地利用/覆盖数据路径 (.tif)")
#
#         st.subheader("布尔选项")
#         calc_sequestration = st.checkbox("计算固碳量 (需要提供未来土地利用数据)", value=True)
#         do_redd = st.checkbox("运行REDD情景分析 (需要提供REDD情景数据)", value=False)
#
#         # 表单的提交按钮
#         submitted = st.form_submit_button("开始运行模型")
#
#     # 运行按钮
#     # if st.button("运行模型一"):
#     #     with st.spinner('正在执行模型一，请稍候...'):
#     #         try:
#     #             # 调用 task1.py 里的 run 函数
#     #             # result = task1.run(parameter_a=param_a, parameter_b=param_b)
#     #             result = "运行结果"
#     #             st.success("模型一执行成功！")
#     #             st.write("返回结果:")
#     #             st.code(result, language='text')
#     #         except Exception as e:
#     #             st.error(f"执行出错: {e}")
#     # --- 当用户点击按钮后执行 ---
#     if submitted:
#         # 1. 输入验证
#         if not all([workspace_dir, lulc_cur_path, carbon_pools_path]):
#             st.error("错误：请确保所有必填参数（1, 2, 3）都已填写！")
#         else:
#             # 2. 显示加载动画，并执行模型
#             with st.spinner("模型正在运行，这可能需要几分钟，请不要关闭页面..."):
#                 try:
#                     # 3. 直接调用我们重构后的函数！
#                     # 注意：空字符串的输入会被视为 None，符合我们函数的设计
#                     result_message = carbon_storage.run(
#                         workspace_dir=workspace_dir,
#                         lulc_cur_path=lulc_cur_path,
#                         carbon_pools_path=carbon_pools_path,
#                         lulc_fut_path=lulc_fut_path or None,
#                         lulc_redd_path=lulc_redd_path or None,
#                         do_redd=do_redd,
#                         calc_sequestration=calc_sequestration
#                     )
#                     # 4. 显示成功信息
#                     st.success(result_message)
#                     st.balloons()
#                 except Exception as e:
#                     # 5. 如果函数抛出异常，在这里捕获并显示
#                     st.error("模型运行出错！")
#                     st.exception(e)  # st.exception 会漂亮地打印出错误的详细信息，非常适合调试
#
# elif script_choice == '模型二：防风固沙':
#     st.header("模型二：防风固沙模型 (RWEQ)")
#     st.info("请输入运行模型所需的各项参数和数据路径。")
#
#     with st.form("sand_break_form"):
#         st.subheader("1. 输出与基本参数")
#         output_folder = st.text_input("结果输出文件夹路径")
#
#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             U1 = st.number_input("起沙风速 U1 (m/s)", value=5.0, format="%.2f")
#         with col2:
#             Nd = st.number_input("沙尘天气日数 Nd", value=50, step=1)
#         with col3:
#             Rd = st.number_input("降水日数 Rd", value=100, step=1)
#         with col4:
#             N = st.number_input("年总日数 N", value=365, step=1)
#
#         st.subheader("2. 核心数据路径 (.tif)")
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             U2_path = st.text_input("风速 U2")
#             ETp_path = st.text_input("潜在蒸散发 ETp")
#             R_path = st.text_input("降雨量 R")
#             I_path = st.text_input("灌溉量 I")
#         with col2:
#             SD_path = st.text_input("积雪深度 SD")
#             sa_path = st.text_input("土壤沙粒含量 sa")
#             si_path = st.text_input("土壤粉粒含量 si")
#             cl_path = st.text_input("土壤粘粒含量 cl")
#         with col3:
#             om_path = st.text_input("土壤有机质 om")
#             K_path = st.text_input("地表糙度 K")
#             C_path = st.text_input("植被覆盖度 C")
#
#         st.subheader("3. 特殊参数 (ρ 和 g)")
#         # 使用单选按钮让用户选择输入方式
#         rho_option = st.radio("空气密度 ρ (rho)", ["输入常数值", "使用TIF文件"], horizontal=True)
#         if rho_option == "输入常数值":
#             rho_input = st.number_input("ρ 值", value=1.225, format="%.4f")
#         else:
#             rho_input = st.text_input("ρ 的TIF文件路径")
#
#         g_option = st.radio("重力加速度 g", ["输入常数值", "使用TIF文件"], horizontal=True)
#         if g_option == "输入常数值":
#             g_input = st.number_input("g 值", value=9.8, format="%.2f")
#         else:
#             g_input = st.text_input("g 的TIF文件路径")
#
#         # 表单的提交按钮
#         submitted = st.form_submit_button("开始运行模型")
#
#     if submitted:
#         if not output_folder:
#             st.error("错误：请必须填写结果输出文件夹路径！")
#         else:
#             with st.spinner("模型正在运行，参数较多，请耐心等待..."):
#                 try:
#                     # 直接调用重构后的函数
#                     result_message = sand_break.run(
#                         output_folder=output_folder, U1=U1, U2_path=U2_path, Nd=Nd,
#                         ETp_path=ETp_path, R_path=R_path, I_path=I_path, Rd=Rd, N=N,
#                         rho=rho_input, SD_path=SD_path, g=g_input,
#                         sa_path=sa_path, si_path=si_path, cl_path=cl_path, om_path=om_path,
#                         K_path=K_path, C_path=C_path
#                     )
#                     st.success(result_message)
#                 except Exception as e:
#                     st.error("模型运行出错！")
#                     st.exception(e)
#
# elif script_choice == '模型三：土壤保持':
#     st.header("模型三：土壤保持 (SDR) 模型")
#     # ... 在这里为 task3 添加输入框和按钮 ...
#
#     st.info("请输入运行模型所需的各项参数和数据路径。")
#
#     # --- 使用表单来组织所有输入参数 ---
#     with st.form("sdr_form"):
#         st.subheader("必填参数")
#         # 使用分栏让布局更紧凑
#         col1, col2 = st.columns(2)
#         with col1:
#             workspace_dir = st.text_input("工作空间目录")
#             dem_path = st.text_input("DEM 数据路径 (.tif)")
#             lulc_path = st.text_input("土地利用/覆盖数据路径 (.tif)")
#             erodibility_path = st.text_input("土壤可蚀性数据路径 (.tif)")
#             erosivity_path = st.text_input("降雨侵蚀力数据路径 (.tif)")
#         with col2:
#             watersheds_path = st.text_input("流域矢量数据路径 (.shp)")
#             biophysical_table_path = st.text_input("生物物理参数表路径 (.csv)")
#             threshold_flow_accumulation = st.number_input("汇流阈值 (整数)", min_value=1, step=1, value=1000)
#             k_param = st.number_input("k_param (Borselli 校准参数)", format="%.4f", value=2.0)
#             ic_0_param = st.number_input("ic_0_param (植被连接度参数)", format="%.4f", value=0.5)
#             sdr_max = st.number_input("sdr_max (最大泥沙输送比)", format="%.4f", value=0.8)
#
#         st.subheader("可选参数 (留空则不使用)")
#         col3, col4 = st.columns(2)
#         with col3:
#             l_max = st.number_input("l_max (最大坡长)", min_value=0, step=1, value=0)  # 用0表示不填
#             drainage_path = st.text_input("排水路径 (.tif)")
#         with col4:
#             lulc_path_bare_soil = st.text_input("裸土土地利用路径 (.tif)")
#
#         # 表单的提交按钮
#         submitted = st.form_submit_button("开始运行模型")
#
#     # --- 当用户点击按钮后执行 ---
#     if submitted:
#         # 输入验证
#         required_paths = [workspace_dir, dem_path, lulc_path, erodibility_path, erosivity_path, watersheds_path,
#                           biophysical_table_path]
#         if not all(required_paths):
#             st.error("错误：请确保所有必填参数的路径都已填写！")
#         else:
#             with st.spinner("模型正在运行，请稍候..."):
#                 try:
#                     # 调用我们重构后的 sdr_model.run 函数
#                     result_message = soil_conservation.run(
#                         workspace_dir=workspace_dir,
#                         dem_path=dem_path,
#                         lulc_path=lulc_path,
#                         erodibility_path=erodibility_path,
#                         erosivity_path=erosivity_path,
#                         watersheds_path=watersheds_path,
#                         biophysical_table_path=biophysical_table_path,
#                         threshold_flow_accumulation=threshold_flow_accumulation,
#                         k_param=k_param,
#                         ic_0_param=ic_0_param,
#                         sdr_max=sdr_max,
#                         l_max=l_max if l_max > 0 else None,  # 如果用户填0或不填，则传递None
#                         drainage_path=drainage_path or None,
#                         lulc_path_bare_soil=lulc_path_bare_soil or None
#                     )
#                     st.success(result_message)
#                 except Exception as e:
#                     st.error("模型运行出错！")
#                     st.exception(e)
#
# elif script_choice == '模型四：水源涵养':
#     st.header("模型四：水源涵养模型")
#     # ... 在这里为 task4 添加输入框和按钮 ...
#     st.info("产水与水源涵养整合模型")
#
#     with st.form("water_yield_retention_form"):
#         st.subheader("1. InVEST 产水量模型参数")
#         workspace_dir = st.text_input("工作空间目录 (所有结果将保存在此)")
#
#         col1, col2 = st.columns(2)
#         with col1:
#             lulc_path = st.text_input("土地利用/覆盖数据 (.tif)")
#             depth_to_root_rest_layer_path = st.text_input("土壤深度数据 (.tif)")
#             precipitation_path = st.text_input("降水量数据 (.tif)")
#             eto_path = st.text_input("参考蒸散发数据 (.tif)")
#         with col2:
#             pawc_path = st.text_input("植物有效含水量数据 (.tif)")
#             watersheds_path = st.text_input("流域矢量数据 (.shp)")
#             biophysical_table_path = st.text_input("生物物理参数表 (.csv)")
#             seasonality_constant = st.number_input("季节性参数 Z (整数)", min_value=1, max_value=30, value=5)
#
#         st.subheader("2. 水源涵养量计算参数")
#         col3, col4 = st.columns(2)
#         with col3:
#             c1_path = st.text_input("黏粒含量数据 C1 (.tif)")
#             c2_path = st.text_input("沙粒含量数据 C2 (.tif)")
#         with col4:
#             v_path = st.text_input("流速速率数据 V (.tif)")
#             t_path = st.text_input("地形指数数据 T1 (.tif)")
#
#         submitted = st.form_submit_button("开始运行完整工作流")
#
#     if submitted:
#         # 基本的输入验证
#         all_inputs = [workspace_dir, lulc_path, depth_to_root_rest_layer_path,
#                       precipitation_path, eto_path, pawc_path, watersheds_path,
#                       biophysical_table_path, c1_path, c2_path, v_path, t_path]
#         if not all(all_inputs):
#             st.error("错误：请确保所有输入框都已填写！")
#         else:
#             with st.spinner("正在执行多步骤工作流，过程较长，请耐心等待..."):
#                 try:
#                     # 只需调用一个函数，传入所有参数
#                     result_message = water_conservation.run(
#                         workspace_dir=workspace_dir,
#                         lulc_path=lulc_path,
#                         depth_to_root_rest_layer_path=depth_to_root_rest_layer_path,
#                         precipitation_path=precipitation_path,
#                         eto_path=eto_path,
#                         pawc_path=pawc_path,
#                         watersheds_path=watersheds_path,
#                         biophysical_table_path=biophysical_table_path,
#                         seasonality_constant=seasonality_constant,
#                         c1_path=c1_path,
#                         c2_path=c2_path,
#                         v_path=v_path,
#                         t_path=t_path
#                     )
#                     st.success(result_message)
#                 except Exception as e:
#                     st.error("工作流运行出错！")
#                     st.exception(e)  # 打印详细的错误堆栈信息
# # --- 模块五 ---
# elif script_choice == '模型五：内插模型':
#     st.header("模型五：内插模型")
#     # ... 在这里为 task4 添加输入框和按钮 ...
#     st.info("这个模型模拟一个需要选择模型和上传文件的场景。")
#
#     # 为 task2 创建参数输入框
#     model_type = st.selectbox("请选择模型类型", ["模型A (SVM)", "模型B (Random Forest)"])
#     uploaded_file = st.file_uploader("请上传你的训练数据 (CSV)", type=['csv'])
#     param_b = st.number_input("请输入数字参数 (Parameter B)", min_value=1, max_value=100, value=10)
#     param_c = st.text_input("请输入字符串参数 (Parameter C)", "world")
#     param_d = st.text_input("请输入字符串参数 (Parameter D)", "apple")
#
#     if st.button("开始训练模型二"):
#         if uploaded_file is not None:
#             with st.spinner(f'正在使用 {model_type} 进行训练...'):
#                 # 这里我们假设 task2.run 接受文件内容和模型名
#                 # result = task2.run(file_content=uploaded_file.getvalue(), model=model_type)
#                 st.success("模拟训练完成！")
#                 st.balloons()  # 来点庆祝
#         else:
#             st.warning("请先上传文件！")
#
# # --- 测试运行 ---
# # 在 PyCharm 终端中输入 `streamlit run app.py` 来预览你的应用
# # 选择文件夹弹窗选择本地路径

# app.py
import streamlit as st
from scripts import soil_conservation, sand_break, carbon_storage, water_conservation  # 从scripts文件夹导入你的脚本模块
import os


# --- 辅助函数 ---
# Streamlit的st.file_uploader返回的是一个内存中的文件对象，而不是路径。
# 模型运行需要的是实际的文件路径，所以我们需要一个函数来将上传的文件保存到磁盘，并返回其路径。
def save_uploaded_file(uploaded_file, save_dir):
    """
    将Streamlit上传的文件对象保存到指定目录，并返回其完整路径。

    参数:
    - uploaded_file: st.file_uploader返回的文件对象。
    - save_dir: 用于保存文件的目录。

    返回:
    - 保存后文件的完整路径 (str)，如果uploaded_file为None则返回None。
    """
    if uploaded_file is not None:
        # 如果保存目录不存在，则创建它
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 拼接文件的完整保存路径
        file_path = os.path.join(save_dir, uploaded_file.name)

        # 以二进制写入模式打开文件，并写入上传文件的数据
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return file_path
    return None


# --- 页面基础设置 ---
st.set_page_config(
    page_title="Python模型库",
    page_icon="🛠️",
    layout="centered"
)

st.title("🛠️ Python 模型库")

# --- 使用侧边栏进行导航 ---
# 使用 Markdown 和 CSS 控制间距
st.markdown("""
<style>
.stRadio > label {
    font-size: 30px; /* 字体大小 */
    padding-top: 20px; /* 上间距 */
    padding-bottom: 20px; /* 下间距 */
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("生态系统服务功能模型")
script_choice = st.sidebar.radio(
    "请选择要使用的模型:",
    ('模型一：碳储量', '模型二：防风固沙', '模型三：土壤保持', '模型四：水源涵养', '模型五：内插模型')
)
# --- 根据选择显示不同的UI界面 ---

if script_choice == '模型一：碳储量':
    st.header("模型一：碳储量")
    st.info("这是一个用于计算碳储量和固碳量的模型。请输入必要的路径和参数。")

    with st.form("carbon_form"):
        st.subheader("必填参数")
        # 修改点2: 目录选择保留文本输入，并增加提示信息
        workspace_dir = st.text_input("1. 工作空间目录 (存放结果的文件夹路径)", "E:\项目\环境监测院\OutPut")
        st.info(
            "选择文件夹可能会暴露您计算机的文件系统结构,导致数据泄露,处于安全考虑请复制并粘贴一个本地文件夹的完整路径，例如：`D:/GIS_Project/Carbon_Results`")

        # 修改点1: 文件路径输入改为文件上传组件
        lulc_cur_path_uploader = st.file_uploader("2. 当前土地利用/覆盖数据 (.tif)", type=['tif', 'tiff'])
        carbon_pools_path_uploader = st.file_uploader("3. 碳库路径 (.csv)", type=['csv'])

        st.subheader("可选参数")
        lulc_fut_path_uploader = st.file_uploader("4. 未来土地利用/覆盖数据路径 (.tif, 用于计算固碳量)",
                                                  type=['tif', 'tiff'])
        lulc_redd_path_uploader = st.file_uploader("5. REDD情景土地利用/覆盖数据路径 (.tif)", type=['tif', 'tiff'])

        st.subheader("布尔选项")
        calc_sequestration = st.checkbox("计算固碳量 (需要提供未来土地利用数据)", value=True)
        do_redd = st.checkbox("运行REDD情景分析 (需要提供REDD情景数据)", value=False)

        submitted = st.form_submit_button("开始运行模型")

    if submitted:
        # 1. 输入验证
        if not all([workspace_dir, lulc_cur_path_uploader, carbon_pools_path_uploader]):
            st.error("错误：请确保所有必填参数（1, 2, 3）都已填写！")
        else:
            with st.spinner("模型正在运行，这可能需要几分钟，请不要关闭页面..."):
                try:
                    # 在工作空间内创建一个专门存放上传文件的子目录
                    upload_save_dir = os.path.join(workspace_dir, "uploaded_files")

                    # 保存上传的文件并获取其路径
                    lulc_cur_path = save_uploaded_file(lulc_cur_path_uploader, upload_save_dir)
                    carbon_pools_path = save_uploaded_file(carbon_pools_path_uploader, upload_save_dir)
                    lulc_fut_path = save_uploaded_file(lulc_fut_path_uploader, upload_save_dir)
                    lulc_redd_path = save_uploaded_file(lulc_redd_path_uploader, upload_save_dir)

                    # 3. 调用模型函数，传入保存后的文件路径
                    result_message = carbon_storage.run(
                        workspace_dir=workspace_dir,
                        lulc_cur_path=lulc_cur_path,
                        carbon_pools_path=carbon_pools_path,
                        lulc_fut_path=lulc_fut_path,  # 如果未上传文件，save_uploaded_file会返回None，符合模型要求
                        lulc_redd_path=lulc_redd_path,
                        do_redd=do_redd,
                        calc_sequestration=calc_sequestration
                    )
                    st.success(result_message)
                    st.balloons()
                except Exception as e:
                    st.error("模型运行出错！")
                    st.exception(e)

elif script_choice == '模型二：防风固沙':
    st.header("模型二：防风固沙模型 (RWEQ)")
    st.info("请输入运行模型所需的各项参数和数据路径。")

    with st.form("sand_break_form"):
        st.subheader("1. 输出与基本参数")
        output_folder = st.text_input("结果输出文件夹路径", "E:\项目\环境监测院\OutPut")
        st.info(
            "选择文件夹可能会暴露您计算机的文件系统结构,导致数据泄露,处于安全考虑请复制并粘贴一个本地文件夹的完整路径，例如：`D:/GIS_Project/Sand_Break_Results`")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            U1 = st.number_input("起沙风速 U1 (m/s)", value=5.0, format="%.2f")
        with col2:
            Nd = st.number_input("大于5m/s风速天数 Nd", value=50, step=1)
        with col3:
            Rd = st.number_input("降水日数 Rd", value=100, step=1)
        with col4:
            N = st.number_input("年总日数 N", value=365, step=1)

        st.subheader("2. 核心数据路径 (.tif)")
        col1, col2, col3 = st.columns(3)
        with col1:
            U2_path_uploader = st.file_uploader("风速 U2", type=['tif', 'tiff'])
            ETp_path_uploader = st.file_uploader("潜在蒸散发 ETp", type=['tif', 'tiff'])
            R_path_uploader = st.file_uploader("降雨量 R", type=['tif', 'tiff'])
            I_path_uploader = st.file_uploader("灌溉量 I", type=['tif', 'tiff'])
        with col2:
            SD_path_uploader = st.file_uploader("积雪深度 SD", type=['tif', 'tiff'])
            sa_path_uploader = st.file_uploader("土壤沙粒含量 sa", type=['tif', 'tiff'])
            si_path_uploader = st.file_uploader("土壤粉粒含量 si", type=['tif', 'tiff'])
            cl_path_uploader = st.file_uploader("土壤粘粒含量 cl", type=['tif', 'tiff'])
        with col3:
            om_path_uploader = st.file_uploader("土壤有机质 om", type=['tif', 'tiff'])
            K_path_uploader = st.file_uploader("地表糙度 K", type=['tif', 'tiff'])
            C_path_uploader = st.file_uploader("植被覆盖度 C", type=['tif', 'tiff'])

        # 修改点3: 实现可切换的输入模式
        st.subheader("3. 特殊参数 (ρ 和 g)")

        # rho_option = st.radio("空气密度 ρ (rho)", ["输入常数值", "使用TIF文件"], horizontal=True, key="rho_radio")
        # if rho_option == "输入常数值":
        #     rho_input = st.number_input("ρ 值", value=1.225, format="%.4f")
        #     rho_uploader = None
        # else:
        #     rho_uploader = st.file_uploader("上传 ρ 的TIF文件", type=['tif', 'tiff'], key="rho_uploader")
        #     rho_input = None
        #
        # g_option = st.radio("重力加速度 g", ["输入常数值", "使用TIF文件"], horizontal=True, key="g_radio")
        # if g_option == "输入常数值":
        #     g_input = st.number_input("g 值", value=9.8, format="%.2f")
        #     g_uploader = None
        # else:
        #     g_uploader = st.file_uploader("上传 g 的TIF文件", type=['tif', 'tiff'], key="g_uploader")
        #     g_input = None
        # --- ρ (rho) 的输入模式 ---
        rho_mode_options = ["输入常数值", "使用TIF文件"]
        # 使用 st.session_state 来存储 radio 按钮的当前选择
        if "rho_mode" not in st.session_state:
            st.session_state.rho_mode = rho_mode_options[0]

        rho_option = st.radio(
            "空气密度 ρ (rho)",
            rho_mode_options,
            index=rho_mode_options.index(st.session_state.rho_mode),
            key="rho_radio"
        )
        st.session_state.rho_mode = rho_option  # 每次选择后更新状态

        if st.session_state.rho_mode == "输入常数值":
            rho_input = st.number_input("ρ 值", value=1.225, format="%.4f")
            rho_uploader = None
        else:
            rho_uploader = st.file_uploader("上传 ρ 的TIF文件", type=['tif', 'tiff'], key="rho_uploader")
            rho_input = None

        # --- g (重力加速度) 的输入模式 ---
        g_mode_options = ["输入常数值", "使用TIF文件"]
        # 使用 st.session_state 来存储 radio 按钮的当前选择
        if "g_mode" not in st.session_state:
            st.session_state.g_mode = g_mode_options[0]

        g_option = st.radio(
            "重力加速度 g",
            g_mode_options,
            index=g_mode_options.index(st.session_state.g_mode),
            key="g_radio"
        )
        st.session_state.g_mode = g_option  # 每次选择后更新状态

        if st.session_state.g_mode == "输入常数值":
            g_input = st.number_input("g 值", value=9.8, format="%.2f")
            g_uploader = None
        else:
            g_uploader = st.file_uploader("上传 g 的TIF文件", type=['tif', 'tiff'], key="g_uploader")
            g_input = None

        submitted = st.form_submit_button("开始运行模型")

    if submitted:
        if not output_folder:
            st.error("错误：请必须填写结果输出文件夹路径！")
        else:
            with st.spinner("模型正在运行，参数较多，请耐心等待..."):
                try:
                    upload_save_dir = os.path.join(output_folder, "uploaded_files")

                    # 保存所有上传的文件
                    U2_path = save_uploaded_file(U2_path_uploader, upload_save_dir)
                    ETp_path = save_uploaded_file(ETp_path_uploader, upload_save_dir)
                    R_path = save_uploaded_file(R_path_uploader, upload_save_dir)
                    I_path = save_uploaded_file(I_path_uploader, upload_save_dir)
                    SD_path = save_uploaded_file(SD_path_uploader, upload_save_dir)
                    sa_path = save_uploaded_file(sa_path_uploader, upload_save_dir)
                    si_path = save_uploaded_file(si_path_uploader, upload_save_dir)
                    cl_path = save_uploaded_file(cl_path_uploader, upload_save_dir)
                    om_path = save_uploaded_file(om_path_uploader, upload_save_dir)
                    K_path = save_uploaded_file(K_path_uploader, upload_save_dir)
                    C_path = save_uploaded_file(C_path_uploader, upload_save_dir)

                    # 根据用户的选择决定 rho 和 g 的最终值 (是数值还是文件路径)
                    final_rho = save_uploaded_file(rho_uploader, upload_save_dir) if rho_uploader else rho_input
                    final_g = save_uploaded_file(g_uploader, upload_save_dir) if g_uploader else g_input

                    result_message = sand_break.run(
                        output_folder=output_folder, U1=U1, U2_path=U2_path, Nd=Nd,
                        ETp_path=ETp_path, R_path=R_path, I_path=I_path, Rd=Rd, N=N,
                        rho=final_rho, SD_path=SD_path, g=final_g,
                        sa_path=sa_path, si_path=si_path, cl_path=cl_path, om_path=om_path,
                        K_path=K_path, C_path=C_path
                    )
                    st.success(result_message)
                except Exception as e:
                    st.error("模型运行出错！")
                    st.exception(e)

elif script_choice == '模型三：土壤保持':
    st.header("模型三：土壤保持 (SDR) 模型")
    st.info(
        "选择文件夹可能会暴露您计算机的文件系统结构,导致数据泄露,处于安全考虑请输入运行模型所需的各项参数和数据路径。")

    with st.form("sdr_form"):
        st.subheader("必填参数")
        col1, col2 = st.columns(2)
        with col1:
            workspace_dir = st.text_input("工作空间目录", "E:\项目\环境监测院\OutPut")
            st.info("所有结果将保存在此目录下。")
            dem_path_uploader = st.file_uploader("DEM 数据 (.tif)", type=['tif', 'tiff'])
            lulc_path_uploader = st.file_uploader("土地利用/覆盖数据 (.tif)", type=['tif', 'tiff'])
            erodibility_path_uploader = st.file_uploader("土壤可蚀性数据 (.tif)", type=['tif', 'tiff'])
            erosivity_path_uploader = st.file_uploader("降雨侵蚀力数据 (.tif)", type=['tif', 'tiff'])
        with col2:
            # 注意：Shapefile通常包含多个文件(.shp, .shx, .dbf等)，需要用户全部上传
            watersheds_path_uploader = st.file_uploader("流域矢量数据 (.shp)", type=['shp', 'shx', 'dbf', 'prj'],
                                                        accept_multiple_files=True)
            st.warning("请务必将 .shp, .shx, .dbf 等所有相关文件一同选中并上传。")
            biophysical_table_path_uploader = st.file_uploader("生物物理参数表 (.csv)", type=['csv'])
            threshold_flow_accumulation = st.number_input("汇流阈值 (整数)", min_value=1, step=1, value=1000)
            k_param = st.number_input("k_param (Borselli 校准参数)", format="%.4f", value=2.0)
            ic_0_param = st.number_input("ic_0_param (植被连接度参数)", format="%.4f", value=0.5)
            sdr_max = st.number_input("sdr_max (最大泥沙输送比)", format="%.4f", value=0.8)

        st.subheader("可选参数 (留空则不使用)")
        col3, col4 = st.columns(2)
        with col3:
            l_max = st.number_input("l_max (最大坡长)", min_value=0, step=1, value=0)  # 用0表示不填
            drainage_path_uploader = st.file_uploader("排水路径 (.tif)", type=['tif', 'tiff'])
        with col4:
            lulc_path_bare_soil_uploader = st.file_uploader("裸土土地利用路径 (.tif)", type=['tif', 'tiff'])

        submitted = st.form_submit_button("开始运行模型")

    if submitted:
        required_uploads = [workspace_dir, dem_path_uploader, lulc_path_uploader, erodibility_path_uploader,
                            erosivity_path_uploader, watersheds_path_uploader, biophysical_table_path_uploader]
        if not all(required_uploads):
            st.error("错误：请确保所有必填参数的路径都已填写！")
        else:
            with st.spinner("模型正在运行，请稍候..."):
                try:
                    upload_save_dir = os.path.join(workspace_dir, "uploaded_files")

                    # 保存所有上传文件
                    dem_path = save_uploaded_file(dem_path_uploader, upload_save_dir)
                    lulc_path = save_uploaded_file(lulc_path_uploader, upload_save_dir)
                    erodibility_path = save_uploaded_file(erodibility_path_uploader, upload_save_dir)
                    erosivity_path = save_uploaded_file(erosivity_path_uploader, upload_save_dir)
                    biophysical_table_path = save_uploaded_file(biophysical_table_path_uploader, upload_save_dir)
                    drainage_path = save_uploaded_file(drainage_path_uploader, upload_save_dir)
                    lulc_path_bare_soil = save_uploaded_file(lulc_path_bare_soil_uploader, upload_save_dir)

                    # 特殊处理Shapefile
                    watersheds_path = None
                    if watersheds_path_uploader:
                        main_shp_path = None
                        for f in watersheds_path_uploader:
                            saved_path = save_uploaded_file(f, upload_save_dir)
                            if saved_path and saved_path.lower().endswith('.shp'):
                                main_shp_path = saved_path
                        watersheds_path = main_shp_path

                    result_message = soil_conservation.run(
                        workspace_dir=workspace_dir,
                        dem_path=dem_path,
                        lulc_path=lulc_path,
                        erodibility_path=erodibility_path,
                        erosivity_path=erosivity_path,
                        watersheds_path=watersheds_path,
                        biophysical_table_path=biophysical_table_path,
                        threshold_flow_accumulation=threshold_flow_accumulation,
                        k_param=k_param,
                        ic_0_param=ic_0_param,
                        sdr_max=sdr_max,
                        l_max=l_max if l_max > 0 else None,
                        drainage_path=drainage_path,
                        lulc_path_bare_soil=lulc_path_bare_soil
                    )
                    st.success(result_message)
                except Exception as e:
                    st.error("模型运行出错！")
                    st.exception(e)

elif script_choice == '模型四：水源涵养':
    st.header("模型四：水源涵养模型")
    st.info("产水与水源涵养整合模型")

    with st.form("water_yield_retention_form"):
        st.subheader("1. InVEST 产水量模型参数")
        workspace_dir = st.text_input("工作空间目录 (所有结果将保存在此)", "E:\项目\环境监测院\OutPut")
        st.info(
            "选择文件夹可能会暴露您计算机的文件系统结构,导致数据泄露,处于安全考虑请复制并粘贴一个本地文件夹的完整路径。")

        col1, col2 = st.columns(2)
        with col1:
            lulc_path_uploader = st.file_uploader("土地利用/覆盖数据 (.tif)", type=['tif', 'tiff'])
            depth_to_root_rest_layer_path_uploader = st.file_uploader("土壤深度数据 (.tif)", type=['tif', 'tiff'])
            precipitation_path_uploader = st.file_uploader("降水量数据 (.tif)", type=['tif', 'tiff'])
            eto_path_uploader = st.file_uploader("参考蒸散发数据 (.tif)", type=['tif', 'tiff'])
        with col2:
            pawc_path_uploader = st.file_uploader("植物有效含水量数据 (.tif)", type=['tif', 'tiff'])
            watersheds_path_uploader = st.file_uploader("流域矢量数据 (.shp)", type=['shp', 'shx', 'dbf', 'prj'],
                                                        accept_multiple_files=True)
            st.warning("请务必将 .shp, .shx, .dbf 等所有相关文件一同选中并上传。")
            biophysical_table_path_uploader = st.file_uploader("生物物理参数表 (.csv)", type=['csv'])
            seasonality_constant = st.number_input("季节性参数 Z", min_value=1.0, max_value=30.0, value=5.0, step=0.1)

        st.subheader("2. 水源涵养量计算参数")
        col3, col4 = st.columns(2)
        with col3:
            c1_path_uploader = st.file_uploader("黏粒含量数据 C1 (.tif)", type=['tif', 'tiff'])
            c2_path_uploader = st.file_uploader("沙粒含量数据 C2 (.tif)", type=['tif', 'tiff'])
        with col4:
            v_path_uploader = st.file_uploader("流速速率数据 V (.tif)", type=['tif', 'tiff'])
            t_path_uploader = st.file_uploader("地形指数数据 T1 (.tif)", type=['tif', 'tiff'])

        submitted = st.form_submit_button("开始运行完整工作流")

    if submitted:
        all_uploads = [workspace_dir, lulc_path_uploader, depth_to_root_rest_layer_path_uploader,
                       precipitation_path_uploader, eto_path_uploader, pawc_path_uploader, watersheds_path_uploader,
                       biophysical_table_path_uploader, c1_path_uploader, c2_path_uploader, v_path_uploader,
                       t_path_uploader]
        if not all(all_uploads):
            st.error("错误：请确保所有输入框都已填写！")
        else:
            with st.spinner("正在执行多步骤工作流，过程较长，请耐心等待..."):
                try:
                    upload_save_dir = os.path.join(workspace_dir, "uploaded_files")

                    # 保存所有文件
                    lulc_path = save_uploaded_file(lulc_path_uploader, upload_save_dir)
                    depth_to_root_rest_layer_path = save_uploaded_file(depth_to_root_rest_layer_path_uploader,
                                                                       upload_save_dir)
                    precipitation_path = save_uploaded_file(precipitation_path_uploader, upload_save_dir)
                    eto_path = save_uploaded_file(eto_path_uploader, upload_save_dir)
                    pawc_path = save_uploaded_file(pawc_path_uploader, upload_save_dir)
                    biophysical_table_path = save_uploaded_file(biophysical_table_path_uploader, upload_save_dir)
                    c1_path = save_uploaded_file(c1_path_uploader, upload_save_dir)
                    c2_path = save_uploaded_file(c2_path_uploader, upload_save_dir)
                    v_path = save_uploaded_file(v_path_uploader, upload_save_dir)
                    t_path = save_uploaded_file(t_path_uploader, upload_save_dir)

                    # 特殊处理Shapefile
                    watersheds_path = None
                    if watersheds_path_uploader:
                        main_shp_path = None
                        for f in watersheds_path_uploader:
                            saved_path = save_uploaded_file(f, upload_save_dir)
                            if saved_path and saved_path.lower().endswith('.shp'):
                                main_shp_path = saved_path
                        watersheds_path = main_shp_path

                    result_message = water_conservation.run(
                        workspace_dir=workspace_dir,
                        lulc_path=lulc_path,
                        depth_to_root_rest_layer_path=depth_to_root_rest_layer_path,
                        precipitation_path=precipitation_path,
                        eto_path=eto_path,
                        pawc_path=pawc_path,
                        watersheds_path=watersheds_path,
                        biophysical_table_path=biophysical_table_path,
                        seasonality_constant=seasonality_constant,
                        c1_path=c1_path,
                        c2_path=c2_path,
                        v_path=v_path,
                        t_path=t_path
                    )
                    st.success(result_message)
                except Exception as e:
                    st.error("工作流运行出错！")
                    st.exception(e)
