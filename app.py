import streamlit as st
import os
import sys
import zipfile
from io import BytesIO
from rembg import remove
from PIL import Image

# ==================== 0. 多语言数据中心 ====================
LANG_DATA = {
    "cn": {
        "title": "Auspice AI Cloud - 在线抠图",
        "lang_label": "选择语言:",
        "header_main": "🚀 AI 智能一键抠图 (Web版)",
        "header_sub": "上传图片，AI 自动去除背景。100% 自动，发丝级精度。",
        "upload_label": "拖拽图片到这里 (支持多张)",
        "sidebar_pro": "💎 会员解锁 / Pro",
        "sidebar_license_input": "输入授权码 (License Key)",
        "status_pro_active": "✅ PRO 会员已激活",
        "status_free_limit": "🔒 免费版限制：仅支持单张处理",
        "status_buy_link": "👉 点击购买授权码 (解锁批量处理)",
        "button_start": "开始处理",
        "button_download": "📥 下载处理结果 (ZIP)",
        "caption_original": "原图",
        "caption_result": "去背结果",
        "warning_free_limit": "⚠️ 免费版一次只能处理 1 张图片。请升级 Pro 解锁批量功能。",
        "status_init": "正在初始化 AI 模型 (首次运行需加载组件)...",
        "status_complete": "🎉 处理完成！",
        "status_processing": "正在处理图片:",
        "file_name_zip": "auspice_ai_results.zip"
    },
    "en": {
        "title": "Auspice AI Cloud - Online Remover",
        "lang_label": "Select Language:",
        "header_main": "🚀 AI Smart One-Click Remover (Web)",
        "header_sub": "Upload images, AI automatically removes background. 100% automatic, high precision.",
        "upload_label": "Drag and drop images here (Supports multiple files)",
        "sidebar_pro": "💎 Member Unlock / Pro",
        "sidebar_license_input": "Enter License Key",
        "status_pro_active": "✅ PRO Membership Activated",
        "status_free_limit": "🔒 Free Version Limit: Single image only",
        "status_buy_link": "👉 Click to Purchase License Key",
        "button_start": "Start Processing",
        "button_download": "📥 Download Results (ZIP)",
        "caption_original": "Original Image",
        "caption_result": "Result",
        "warning_free_limit": "⚠️ Free version is limited to 1 image. Please upgrade to Pro for batch functionality.",
        "status_init": "Initializing AI Model (First run may take time...)",
        "status_complete": "🎉 Processing Complete!",
        "status_processing": "Processing file:",
        "file_name_zip": "auspice_ai_results.zip"
    },
    "de": {
        "title": "Auspice AI Cloud - Online Entferner",
        "lang_label": "Sprache wählen:",
        "header_main": "🚀 AI Intelligente Bildentfernung (Web)",
        "header_sub": "Bilder hochladen, KI entfernt automatisch den Hintergrund. 100% automatisch.",
        "upload_label": "Bilder hierher ziehen (Mehrere Dateien möglich)",
        "sidebar_pro": "💎 Mitgliedschaft freischalten",
        "sidebar_license_input": "Lizenzschlüssel eingeben",
        "status_pro_active": "✅ PRO Mitgliedschaft aktiviert",
        "status_free_limit": "🔒 Kostenlose Version: Nur Einzelbilder",
        "status_buy_link": "👉 Hier klicken, um Lizenz zu kaufen",
        "button_start": "Verarbeitung starten",
        "button_download": "📥 Ergebnisse herunterladen (ZIP)",
        "caption_original": "Originalbild",
        "caption_result": "Ergebnis",
        "warning_free_limit": "⚠️ Die kostenlose Version ist auf 1 Bild beschränkt. Bitte auf Pro upgraden.",
        "status_init": "Initialisiere AI-Modell...",
        "status_complete": "🎉 Verarbeitung abgeschlossen!",
        "status_processing": "Verarbeite Datei:",
        "file_name_zip": "auspice_ai_results.zip"
    }
}

# ==================== 1. GSC & 语言状态管理 ====================
# GSC 验证代码 (已修复位置)
VERIFICATION_CODE = "68nKEmv8Ywd2MOzO9Qt_LKyvndK3biYJ08JPiFECChI" # ⚠️ 替换为你的真实代码！
st.markdown(f'<meta name="google-site-verification" content="{VERIFICATION_CODE}" />', unsafe_allow_html=True)

# 隐藏 Streamlit 默认样式
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 初始化语言状态
if 'lang' not in st.session_state:
    st.session_state.lang = 'en' # 默认英语

# 获取当前语言文本
def _(key):
    return LANG_DATA[st.session_state.lang].get(key, key)

# 语言切换函数 (当用户选择语言时触发)
def set_lang(lang_code):
    st.session_state.lang = lang_code

st.set_page_config(
    page_title=_( "title"),
    page_icon="🎨",
    layout="centered"
)

# ==================== 2. 侧边栏 (SaaS 变现区) ====================
with st.sidebar:
    # 语言选择器
    st.markdown("### 🌍 " + _("lang_label"))
    lang_choice = st.selectbox(
        label=" ", # 标签留空，防止重复显示
        options=["English", "中文", "Deutsch"],
        index=0, # 默认选中 English
        format_func=lambda x: x # 显示完整的选项文本
    )
    if lang_choice == "中文": set_lang('cn')
    elif lang_choice == "Deutsch": set_lang('de')
    else: set_lang('en')
    
    st.markdown("---")
    
    # 授权码验证区
    st.write("### " + _("sidebar_pro"))
    license_key = st.text_input(_("sidebar_license_input"), type="password")
    
    is_pro = False
    if license_key == "AUSPICE-VIP-2025": # 你的授权码
        is_pro = True
        st.success(_("status_pro_active"))
    else:
        st.info(_("status_free_limit"))
        st.markdown(f"[{_('status_buy_link')}](https://budgetbuffoon.gumroad.com/l/background-remover)")

# ==================== 3. 主界面 ====================
st.title(_("header_main"))
st.write(_("header_sub"))

# 文件上传器
uploaded_files = st.file_uploader(_("upload_label"), type=['png', 'jpg', 'jpeg', 'webp'], accept_multiple_files=True)

if uploaded_files:
    # --- 限制逻辑 ---
    if not is_pro and len(uploaded_files) > 1:
        st.warning(_("warning_free_limit"))
        uploaded_files = [uploaded_files[0]]
    
    st.markdown("---")
    
    # 开始处理按钮
    if st.button(_("button_start"), type="primary"):
        
        # 第一次运行的 AI 模型下载提示
        st.warning(_("status_init"))
        
        progress_bar = st.progress(0)
        
        # 准备 ZIP 文件缓冲区
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for i, uploaded_file in enumerate(uploaded_files):
                st.info(f"{_('status_processing')} {uploaded_file.name}")
                
                bytes_data = uploaded_file.getvalue()
                output_data = remove(bytes_data)
                
                # 3. 展示结果 (只展示第一张的对比图)
                if i == 0:
                    st.subheader("--- Result Preview ---")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(bytes_data, caption=_("caption_original"), use_column_width=True)
                    with col2:
                        st.image(output_data, caption=_("caption_result"), use_column_width=True)
                
                # 4. 写入 ZIP
                file_name = uploaded_file.name.split('.')[0] + "_no_bg.png"
                zip_file.writestr(file_name, output_data)
                
                # 更新进度
                progress_bar.progress((i + 1) / len(uploaded_files))
        
        # --- 下载区域 ---
        st.success(_("status_complete"))
        
        zip_buffer.seek(0)
        
        st.download_button(
            label=_("button_download"),
            data=zip_buffer,
            file_name=_("file_name_zip"),
            mime="application/zip",
            type="primary"
        )
