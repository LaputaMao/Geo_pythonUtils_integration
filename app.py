# app.py
import streamlit as st
from scripts import soil_conservation, sand_break, carbon_storage, water_conservation  # 从scripts文件夹导入你的脚本模块

# --- 页面基础设置 ---
st.set_page_config(
    page_title="Python工具箱",
    page_icon="🛠️",
    layout="centered"
)

st.title("🛠️ Python 工具箱")

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

st.sidebar.title("导航栏")
script_choice = st.sidebar.radio(
    "请选择要使用的工具:",
    ('工具一：碳储量', '工具二：防风固沙', '工具三：土壤保持', '工具四：水分保持', '工具五：内插模型')
)
# --- 根据选择显示不同的UI界面 ---

if script_choice == '工具一：碳储量':
    st.header("工具一：碳储量")
    st.info("这是一个用于计算碳储量和固碳量的工具。请输入必要的路径和参数。")

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
    # if st.button("运行工具一"):
    #     with st.spinner('正在执行工具一，请稍候...'):
    #         try:
    #             # 调用 task1.py 里的 run 函数
    #             # result = task1.run(parameter_a=param_a, parameter_b=param_b)
    #             result = "运行结果"
    #             st.success("工具一执行成功！")
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

elif script_choice == '工具二：防风固沙':
    st.header("工具二：防风固沙模型 (RWEQ)")
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

# --- 为工具三和工具四添加类似的代码块 ---
elif script_choice == '工具三：土壤保持':
    st.header("工具三：土壤保持")
    # ... 在这里为 task3 添加输入框和按钮 ...

    st.info("这个工具模拟一个需要选择模型和上传文件的场景。")

    # 为 task2 创建参数输入框
    model_type = st.selectbox("请选择模型类型", ["模型A (SVM)", "模型B (Random Forest)"])
    uploaded_file = st.file_uploader("请上传你的训练数据 (CSV)", type=['csv'])
    param_b = st.number_input("请输入数字参数 (Parameter B)", min_value=1, max_value=100, value=10)
    param_c = st.text_input("请输入字符串参数 (Parameter C)", "world")
    param_d = st.text_input("请输入字符串参数 (Parameter D)", "apple")

    if st.button("开始训练工具二"):
        if uploaded_file is not None:
            with st.spinner(f'正在使用 {model_type} 进行训练...'):
                # 这里我们假设 task2.run 接受文件内容和模型名
                # result = task2.run(file_content=uploaded_file.getvalue(), model=model_type)
                st.success("模拟训练完成！")
                st.balloons()  # 来点庆祝
        else:
            st.warning("请先上传文件！")


elif script_choice == '工具四：水分保持':
    st.header("工具四：水分保持")
    # ... 在这里为 task4 添加输入框和按钮 ...
    st.info("这个工具模拟一个需要选择模型和上传文件的场景。")

    # 为 task2 创建参数输入框
    model_type = st.selectbox("请选择模型类型", ["模型A (SVM)", "模型B (Random Forest)"])
    uploaded_file = st.file_uploader("请上传你的训练数据 (CSV)", type=['csv'])
    param_b = st.number_input("请输入数字参数 (Parameter B)", min_value=1, max_value=100, value=10)
    param_c = st.text_input("请输入字符串参数 (Parameter C)", "world")
    param_d = st.text_input("请输入字符串参数 (Parameter D)", "apple")

    if st.button("开始训练工具二"):
        if uploaded_file is not None:
            with st.spinner(f'正在使用 {model_type} 进行训练...'):
                # 这里我们假设 task2.run 接受文件内容和模型名
                # result = task2.run(file_content=uploaded_file.getvalue(), model=model_type)
                st.success("模拟训练完成！")
                st.balloons()  # 来点庆祝
        else:
            st.warning("请先上传文件！")

# --- 模块五 ---
elif script_choice == '工具五：内插模型':
    st.header("工具五：内插模型")
    # ... 在这里为 task4 添加输入框和按钮 ...
    st.info("这个工具模拟一个需要选择模型和上传文件的场景。")

    # 为 task2 创建参数输入框
    model_type = st.selectbox("请选择模型类型", ["模型A (SVM)", "模型B (Random Forest)"])
    uploaded_file = st.file_uploader("请上传你的训练数据 (CSV)", type=['csv'])
    param_b = st.number_input("请输入数字参数 (Parameter B)", min_value=1, max_value=100, value=10)
    param_c = st.text_input("请输入字符串参数 (Parameter C)", "world")
    param_d = st.text_input("请输入字符串参数 (Parameter D)", "apple")

    if st.button("开始训练工具二"):
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
