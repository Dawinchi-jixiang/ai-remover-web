import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import zipfile

# ==================== 1. 页面基础配置 ====================
st.set_page_config(
    page_title="Auspice AI Cloud - 在线抠图",
    page_icon="🎨",
    layout="centered"
)

# 隐藏右上角菜单和底部水印
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ==================== 2. 侧边栏 (SaaS 变现区) ====================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100) # 你的Logo
    st.title("Auspice AI Cloud")
    st.markdown("---")
    
    st.write("### 💎 会员解锁 / Pro")
    license_key = st.text_input("输入授权码 (License Key)", type="password")
    
    # 简单的验证逻辑 (你可以把这个码设为你在 Gumroad 卖的码)
    is_pro = False
    if license_key == "AUSPICE-VIP-2025": # 这里是你的“暗号”
        is_pro = True
        st.success("✅ PRO 会员已激活")
    else:
        st.info("🔒 免费版限制：仅支持单张处理\n购买 Pro 版解锁批量模式。")
        st.markdown("[👉 点击购买授权码 ($5)](https://budgetbuffoon.gumroad.com/l/background-remover)")

# ==================== 3. 主界面 ====================
st.title("🚀 AI 智能一键抠图 (Web版)")
st.write("上传图片，AI 自动去除背景。100% 自动，发丝级精度。")

# 文件上传器
uploaded_files = st.file_uploader("拖拽图片到这里", type=['png', 'jpg', 'jpeg', 'webp'], accept_multiple_files=True)

if uploaded_files:
    # --- 限制逻辑 ---
    if not is_pro and len(uploaded_files) > 1:
        st.warning("⚠️ 免费版一次只能处理 1 张图片。请升级 Pro 解锁批量功能。")
        # 强制只取第一张
        uploaded_files = [uploaded_files[0]]

    # 开始处理按钮
    if st.button(f"开始处理 ({len(uploaded_files)} 张)"):
        progress_bar = st.progress(0)
        
        # 准备一个内存里的 ZIP 文件 (用于批量下载)
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for i, uploaded_file in enumerate(uploaded_files):
                # 1. 读取图片
                bytes_data = uploaded_file.getvalue()
                
                # 2. AI 抠图
                output_data = remove(bytes_data)
                
                # 3. 展示结果 (只展示前3张，避免网页太长)
                if i < 3:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(uploaded_file, caption="原图", use_column_width=True)
                    with col2:
                        st.image(output_data, caption="去背结果", use_column_width=True)
                
                # 4. 写入 ZIP
                file_name = uploaded_file.name.split('.')[0] + "_no_bg.png"
                zip_file.writestr(file_name, output_data)
                
                # 更新进度
                progress_bar.progress((i + 1) / len(uploaded_files))
        
        # --- 下载区域 ---
        st.success("🎉 处理完成！")
        
        # 将指针移回 ZIP 文件开头
        zip_buffer.seek(0)
        
        st.download_button(
            label="📥 下载处理结果 (ZIP)",
            data=zip_buffer,
            file_name="auspice_ai_results.zip",
            mime="application/zip",
            type="primary" # 醒目的按钮

        )
