# app.py
import streamlit as st
from scripts import soil_conservation, sand_break, carbon_storage, water_conservation  # 从scripts文件夹导入你的脚本模块

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

    # 为 task1 创建参数输入框
    # param_a = st.text_input("请输入字符串参数 (Parameter A)", "hello")

    # --- 使用表单来组织输入 ---
    with st.form("carbon_form"):
        st.subheader("必填参数")
        workspace_dir = st.text_input("1. 工作空间目录 (存放结果的文件夹路径)", "/your/project/path")
        lulc_cur_path = st.text_input("2. 当前土地利用/覆盖数据路径 (.tif)")
        carbon_pools_path = st.text_input("3. 碳库路径 (.csv)")

        st.subheader("可选参数")
        lulc_fut_path = st.text_input("4. 未来土地利用/覆盖数据路径 (.tif, 用于计算固碳量)")
        lulc_redd_path = st.text_input("5. REDD情景土地利用/覆盖数据路径 (.tif)")

        st.subheader("布尔选项")
        calc_sequestration = st.checkbox("计算固碳量 (需要提供未来土地利用数据)", value=True)
        do_redd = st.checkbox("运行REDD情景分析 (需要提供REDD情景数据)", value=False)

        # 表单的提交按钮
        submitted = st.form_submit_button("开始运行模型")

    # 运行按钮
    # if st.button("运行模型一"):
    #     with st.spinner('正在执行模型一，请稍候...'):
    #         try:
    #             # 调用 task1.py 里的 run 函数
    #             # result = task1.run(parameter_a=param_a, parameter_b=param_b)
    #             result = "运行结果"
    #             st.success("模型一执行成功！")
    #             st.write("返回结果:")
    #             st.code(result, language='text')
    #         except Exception as e:
    #             st.error(f"执行出错: {e}")
    # --- 当用户点击按钮后执行 ---
    if submitted:
        # 1. 输入验证
        if not all([workspace_dir, lulc_cur_path, carbon_pools_path]):
            st.error("错误：请确保所有必填参数（1, 2, 3）都已填写！")
        else:
            # 2. 显示加载动画，并执行模型
            with st.spinner("模型正在运行，这可能需要几分钟，请不要关闭页面..."):
                try:
                    # 3. 直接调用我们重构后的函数！
                    # 注意：空字符串的输入会被视为 None，符合我们函数的设计
                    result_message = carbon_storage.run(
                        workspace_dir=workspace_dir,
                        lulc_cur_path=lulc_cur_path,
                        carbon_pools_path=carbon_pools_path,
                        lulc_fut_path=lulc_fut_path or None,
                        lulc_redd_path=lulc_redd_path or None,
                        do_redd=do_redd,
                        calc_sequestration=calc_sequestration
                    )
                    # 4. 显示成功信息
                    st.success(result_message)
                    st.balloons()
                except Exception as e:
                    # 5. 如果函数抛出异常，在这里捕获并显示
                    st.error("模型运行出错！")
                    st.exception(e)  # st.exception 会漂亮地打印出错误的详细信息，非常适合调试

elif script_choice == '模型二：防风固沙':
    st.header("模型二：防风固沙模型 (RWEQ)")
    st.info("请输入运行模型所需的各项参数和数据路径。")

    with st.form("sand_break_form"):
        st.subheader("1. 输出与基本参数")
        output_folder = st.text_input("结果输出文件夹路径")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            U1 = st.number_input("起沙风速 U1 (m/s)", value=5.0, format="%.2f")
        with col2:
            Nd = st.number_input("沙尘天气日数 Nd", value=50, step=1)
        with col3:
            Rd = st.number_input("降水日数 Rd", value=100, step=1)
        with col4:
            N = st.number_input("年总日数 N", value=365, step=1)

        st.subheader("2. 核心数据路径 (.tif)")
        col1, col2, col3 = st.columns(3)
        with col1:
            U2_path = st.text_input("风速 U2")
            ETp_path = st.text_input("潜在蒸散发 ETp")
            R_path = st.text_input("降雨量 R")
            I_path = st.text_input("灌溉量 I")
        with col2:
            SD_path = st.text_input("积雪深度 SD")
            sa_path = st.text_input("土壤沙粒含量 sa")
            si_path = st.text_input("土壤粉粒含量 si")
            cl_path = st.text_input("土壤粘粒含量 cl")
        with col3:
            om_path = st.text_input("土壤有机质 om")
            K_path = st.text_input("地表糙度 K")
            C_path = st.text_input("植被覆盖度 C")

        st.subheader("3. 特殊参数 (ρ 和 g)")
        # 使用单选按钮让用户选择输入方式
        rho_option = st.radio("空气密度 ρ (rho)", ["输入常数值", "使用TIF文件"], horizontal=True)
        if rho_option == "输入常数值":
            rho_input = st.number_input("ρ 值", value=1.225, format="%.4f")
        else:
            rho_input = st.text_input("ρ 的TIF文件路径")

        g_option = st.radio("重力加速度 g", ["输入常数值", "使用TIF文件"], horizontal=True)
        if g_option == "输入常数值":
            g_input = st.number_input("g 值", value=9.8, format="%.2f")
        else:
            g_input = st.text_input("g 的TIF文件路径")

        # 表单的提交按钮
        submitted = st.form_submit_button("开始运行模型")

    if submitted:
        if not output_folder:
            st.error("错误：请必须填写结果输出文件夹路径！")
        else:
            with st.spinner("模型正在运行，参数较多，请耐心等待..."):
                try:
                    # 直接调用重构后的函数
                    result_message = sand_break.run(
                        output_folder=output_folder, U1=U1, U2_path=U2_path, Nd=Nd,
                        ETp_path=ETp_path, R_path=R_path, I_path=I_path, Rd=Rd, N=N,
                        rho=rho_input, SD_path=SD_path, g=g_input,
                        sa_path=sa_path, si_path=si_path, cl_path=cl_path, om_path=om_path,
                        K_path=K_path, C_path=C_path
                    )
                    st.success(result_message)
                except Exception as e:
                    st.error("模型运行出错！")
                    st.exception(e)

elif script_choice == '模型三：土壤保持':
    st.header("模型三：土壤保持 (SDR) 模型")
    # ... 在这里为 task3 添加输入框和按钮 ...

    st.info("请输入运行模型所需的各项参数和数据路径。")

    # --- 使用表单来组织所有输入参数 ---
    with st.form("sdr_form"):
        st.subheader("必填参数")
        # 使用分栏让布局更紧凑
        col1, col2 = st.columns(2)
        with col1:
            workspace_dir = st.text_input("工作空间目录")
            dem_path = st.text_input("DEM 数据路径 (.tif)")
            lulc_path = st.text_input("土地利用/覆盖数据路径 (.tif)")
            erodibility_path = st.text_input("土壤可蚀性数据路径 (.tif)")
            erosivity_path = st.text_input("降雨侵蚀力数据路径 (.tif)")
        with col2:
            watersheds_path = st.text_input("流域矢量数据路径 (.shp)")
            biophysical_table_path = st.text_input("生物物理参数表路径 (.csv)")
            threshold_flow_accumulation = st.number_input("汇流阈值 (整数)", min_value=1, step=1, value=1000)
            k_param = st.number_input("k_param (Borselli 校准参数)", format="%.4f", value=2.0)
            ic_0_param = st.number_input("ic_0_param (植被连接度参数)", format="%.4f", value=0.5)
            sdr_max = st.number_input("sdr_max (最大泥沙输送比)", format="%.4f", value=0.8)

        st.subheader("可选参数 (留空则不使用)")
        col3, col4 = st.columns(2)
        with col3:
            l_max = st.number_input("l_max (最大坡长)", min_value=0, step=1, value=0)  # 用0表示不填
            drainage_path = st.text_input("排水路径 (.tif)")
        with col4:
            lulc_path_bare_soil = st.text_input("裸土土地利用路径 (.tif)")

        # 表单的提交按钮
        submitted = st.form_submit_button("开始运行模型")

    # --- 当用户点击按钮后执行 ---
    if submitted:
        # 输入验证
        required_paths = [workspace_dir, dem_path, lulc_path, erodibility_path, erosivity_path, watersheds_path,
                          biophysical_table_path]
        if not all(required_paths):
            st.error("错误：请确保所有必填参数的路径都已填写！")
        else:
            with st.spinner("模型正在运行，请稍候..."):
                try:
                    # 调用我们重构后的 sdr_model.run 函数
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
                        l_max=l_max if l_max > 0 else None,  # 如果用户填0或不填，则传递None
                        drainage_path=drainage_path or None,
                        lulc_path_bare_soil=lulc_path_bare_soil or None
                    )
                    st.success(result_message)
                except Exception as e:
                    st.error("模型运行出错！")
                    st.exception(e)

elif script_choice == '模型四：水源涵养':
    st.header("模型四：水源涵养模型")
    # ... 在这里为 task4 添加输入框和按钮 ...
    st.info("产水与水源涵养整合模型")

    with st.form("water_yield_retention_form"):
        st.subheader("1. InVEST 产水量模型参数")
        workspace_dir = st.text_input("工作空间目录 (所有结果将保存在此)")

        col1, col2 = st.columns(2)
        with col1:
            lulc_path = st.text_input("土地利用/覆盖数据 (.tif)")
            depth_to_root_rest_layer_path = st.text_input("土壤深度数据 (.tif)")
            precipitation_path = st.text_input("降水量数据 (.tif)")
            eto_path = st.text_input("参考蒸散发数据 (.tif)")
        with col2:
            pawc_path = st.text_input("植物有效含水量数据 (.tif)")
            watersheds_path = st.text_input("流域矢量数据 (.shp)")
            biophysical_table_path = st.text_input("生物物理参数表 (.csv)")
            seasonality_constant = st.number_input("季节性参数 Z (整数)", min_value=1, max_value=30, value=5)

        st.subheader("2. 水源涵养量计算参数")
        col3, col4 = st.columns(2)
        with col3:
            c1_path = st.text_input("黏粒含量数据 C1 (.tif)")
            c2_path = st.text_input("沙粒含量数据 C2 (.tif)")
        with col4:
            v_path = st.text_input("流速速率数据 V (.tif)")
            t_path = st.text_input("地形指数数据 T1 (.tif)")

        submitted = st.form_submit_button("开始运行完整工作流")

    if submitted:
        # 基本的输入验证
        all_inputs = [workspace_dir, lulc_path, depth_to_root_rest_layer_path,
                      precipitation_path, eto_path, pawc_path, watersheds_path,
                      biophysical_table_path, c1_path, c2_path, v_path, t_path]
        if not all(all_inputs):
            st.error("错误：请确保所有输入框都已填写！")
        else:
            with st.spinner("正在执行多步骤工作流，过程较长，请耐心等待..."):
                try:
                    # 只需调用一个函数，传入所有参数
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
                    st.exception(e)  # 打印详细的错误堆栈信息
# --- 模块五 ---
elif script_choice == '模型五：内插模型':
    st.header("模型五：内插模型")
    # ... 在这里为 task4 添加输入框和按钮 ...
    st.info("这个模型模拟一个需要选择模型和上传文件的场景。")

    # 为 task2 创建参数输入框
    model_type = st.selectbox("请选择模型类型", ["模型A (SVM)", "模型B (Random Forest)"])
    uploaded_file = st.file_uploader("请上传你的训练数据 (CSV)", type=['csv'])
    param_b = st.number_input("请输入数字参数 (Parameter B)", min_value=1, max_value=100, value=10)
    param_c = st.text_input("请输入字符串参数 (Parameter C)", "world")
    param_d = st.text_input("请输入字符串参数 (Parameter D)", "apple")

    if st.button("开始训练模型二"):
        if uploaded_file is not None:
            with st.spinner(f'正在使用 {model_type} 进行训练...'):
                # 这里我们假设 task2.run 接受文件内容和模型名
                # result = task2.run(file_content=uploaded_file.getvalue(), model=model_type)
                st.success("模拟训练完成！")
                st.balloons()  # 来点庆祝
        else:
            st.warning("请先上传文件！")

# --- 测试运行 ---
# 在 PyCharm 终端中输入 `streamlit run app.py` 来预览你的应用
# 选择文件夹弹窗选择本地路径
