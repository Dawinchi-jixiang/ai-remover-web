import streamlit as st
import os
import sys
# ⚠️ 注意：这里我们移除了 rembg 库，以保证 Streamlit 服务器的稳定性

# ==================== GSC 验证代码 ====================
VERIFICATION_CODE = "68nKEmv8Ywd2MOzO9Qt_LKyvndK3biYJ08JPiFECChI" 
st.markdown(f'<meta name="google-site-verification" content="{VERIFICATION_CODE}" />', unsafe_allow_html=True)
# =======================================================

# 隐藏 Streamlit 默认样式
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 语言数据 (简化，但保持多语言切换功能)
LANG_DATA = {
    "cn": {
        "title": "Auspice AI Solution - 离线抠图神器",
        "header_main": "✅ 终极离线 AI 抠图解决方案",
        "header_sub": "100% 离线隐私安全 | 无限批量处理 | 无订阅费",
        "intro_text": "Streamlit Cloud 性能有限，无法运行 AI 引擎。为了您的数据安全和处理效率，请直接下载稳定且强大的 Windows 桌面应用程序。",
        "demo_title": "效果预览 (Preview)",
        "download_button": "🚀 点击购买/下载稳定版 (Windows EXE)",
        "privacy_note": "数据在本地 PC 处理，永不上传云端。",
        "buy_link": "https://budgetbuffoon.gumroad.com/l/background-remover" # 替换你的链接
    },
    "en": {
        "title": "Auspice AI Solution - Offline Remover",
        "header_main": "✅ Ultimate Offline AI Background Remover",
        "header_sub": "100% Private | Unlimited Batch Processing | No Subscription",
        "intro_text": "Streamlit Cloud is too weak for our AI engine. For your data security and processing speed, please download the stable and powerful Windows desktop application directly.",
        "demo_title": "Results Preview",
        "download_button": "🚀 Buy/Download Stable Version (Windows EXE)",
        "privacy_note": "Data is processed locally on your PC, never uploaded to the cloud.",
        "buy_link": "https://budgetbuffoon.gumroad.com/l/background-remover"
    },
    "de": {
        "title": "Auspice AI Solution - Offline Entferner",
        "header_main": "✅ Ultimative Offline AI Lösung",
        "header_sub": "100% Privat | Unbegrenzte Batch-Verarbeitung | Keine Abos",
        "intro_text": "Streamlit Cloud ist zu schwach für unsere AI. Für Ihre Datensicherheit laden Sie bitte die stabile Windows Desktop-Anwendung direkt herunter.",
        "demo_title": "Ergebnisvorschau",
        "download_button": "🚀 Stabile Version Kaufen/Downloaden (Windows EXE)",
        "privacy_note": "Daten werden lokal auf Ihrem PC verarbeitet, niemals in die Cloud hochgeladen.",
        "buy_link": "https://budgetbuffoon.gumroad.com/l/background-remover"
    }
}

# 初始化语言状态
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
def _(key):
    return LANG_DATA[st.session_state.lang].get(key, key)
def set_lang(lang_code):
    st.session_state.lang = lang_code

st.set_page_config(page_title=_( "title"), page_icon="🎨", layout="centered")

# ==================== 页面构建 ====================
st.title(_("header_main"))
st.subheader(_("header_sub"))
st.markdown("---")


# 侧边栏 (语言选择)
with st.sidebar:
    st.write("### 🌍 " + _("lang_label"))
    lang_choice = st.selectbox(
        label=" ",
        options=["English", "中文", "Deutsch"],
        index=0,
    )
    if lang_choice == "中文": set_lang('cn')
    elif lang_choice == "Deutsch": set_lang('de')
    else: set_lang('en')

# 核心营销文案
st.markdown(f"### {_('intro_text')}")
st.warning(_('privacy_note'))

st.markdown("---")

# 下载按钮 (最终目的)
st.markdown(
    f"""
    <div style="text-align: center; margin-top: 30px; margin-bottom: 30px;">
        <a href="{_('buy_link')}" target="_blank">
            <button style="background-color: #ff4b4b; color: white; padding: 15px 30px; border-radius: 8px; font-size: 20px; font-weight: bold; border: none; cursor: pointer;">
                {_('download_button')}
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# 效果展示区 (静态图替代实时处理)
st.subheader(_('demo_title'))

col1, col2 = st.columns(2)

# 注意：这里需要替换为你自己的静态图片链接或 Base64 编码
# 客户需要看到 Before & After 对比图
with col1:
    st.image("https://images.unsplash.com/photo-1596468497914-411a7f05c48b?fit=crop&w=400&h=400", 
             caption=_('caption_original'), use_column_width=True)

with col2:
    # 假设这是抠图后的白底图效果
    st.image("https://images.unsplash.com/photo-1596468497914-411a7f05c48b?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=400&w=400",
             caption=_('caption_result'), use_column_width=True)


# --- 隐藏不必要的输入框 ---
# (为了让页面看起来更简洁)
# ...
