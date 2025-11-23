import streamlit as st
from anthropic import Anthropic
from modules.chat_manager import ChatManager
from modules.thought_processor import ThoughtProcessor
from modules.content_processor import ContentProcessor
from modules.knowledge_manager import KnowledgeManager

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'chat_manager' not in st.session_state:
        st.session_state.chat_manager = None
    if 'current_mode' not in st.session_state:
        st.session_state.current_mode = "chat"
    if 'thought_processor' not in st.session_state:
        st.session_state.thought_processor = ThoughtProcessor()

def render_thought_mode():
    st.subheader("思維發想模式")
    
    # 思維模式選擇
    thought_mode = st.selectbox(
        "選擇思維模式",
        ["概念延伸", "架構整理", "腦力激盪"]
    )
    
    # 思維工具選擇
    thought_tool = st.selectbox(
        "選擇思維工具",
        ["一般模式", "心智圖", "SWOT分析", "五個為什麼"]
    )
    
    # 輸入區域
    col1, col2 = st.columns([3, 1])
    with col1:
        user_input = st.text_area("輸入內容", height=150)
    with col2:
        st.write("提示：")
        if thought_mode == "概念延伸":
            st.info("輸入核心概念，AI將幫助您延伸相關想法")
        elif thought_mode == "架構整理":
            st.info("輸入內容，AI將幫助您整理邏輯架構")
        else:
            st.info("輸入主題，AI將協助您進行腦力激盪")
    
    # 處理按鈕
    if st.button("開始思考"):
        if user_input:
            with st.spinner("正在思考中..."):
                # 準備提示詞
                template = None
                if thought_tool == "心智圖":
                    prompt = st.session_state.thought_processor.generate_mind_map(user_input)
                elif thought_tool == "SWOT分析":
                    template = "swot"
                elif thought_tool == "五個為什麼":
                    template = "five_why"
                else:
                    prompt = st.session_state.thought_processor.process_thought(thought_mode, user_input)
                
                if template:
                    prompt = st.session_state.thought_processor.process_thought(
                        thought_mode, user_input, template=template
                    )
                
                # 獲取 AI 回應
                response = st.session_state.chat_manager.get_response(prompt)
                
                # 顯示結果
                st.markdown("### 思考結果")
                st.markdown(response)
                
                # 保存到對話歷史
                st.session_state.messages.extend([
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": response}
                ])
        else:
            st.warning("請輸入內容後再開始思考")

def render_content_mode():
    st.subheader("內容整理模式")
    
    # 初始化 content processor
    if 'content_processor' not in st.session_state:
        st.session_state.content_processor = ContentProcessor()
    
    # 內容處理模式選擇
    content_mode = st.selectbox(
        "選擇處理模式",
        ["重點摘要", "結構化整理", "格式轉換", "關鍵詞提取"]
    )
    
    # 根據模式顯示不同的選項
    if content_mode == "重點摘要":
        col1, col2 = st.columns(2)
        with col1:
            summary_length = st.select_slider(
                "摘要長度",
                options=["short", "medium", "long"],
                value="medium",
                format_func=lambda x: {"short": "簡短", "medium": "中等", "long": "詳細"}[x]
            )
        with col2:
            summary_style = st.selectbox(
                "摘要風格",
                ["標準摘要", "重點條列", "分段摘要"],
                help="選擇不同的摘要呈現方式"
            )
        
        st.info("💡 提示：較長文本建議使用「分段摘要」，可以更好地組織內容結構")
    elif content_mode == "結構化整理":
        format_type = st.selectbox(
            "輸出格式",
            ["outline", "table", "list", "hierarchy"],
            format_func=lambda x: {
                "outline": "大綱格式",
                "table": "表格格式",
                "list": "列表格式",
                "hierarchy": "層級結構"
            }[x]
        )
    elif content_mode == "格式轉換":
        target_format = st.selectbox(
            "目標格式",
            ["markdown", "json", "csv", "html"]
        )
    
    # 輸入區域
    col1, col2 = st.columns([3, 1])
    with col1:
        user_input = st.text_area("輸入內容", height=200)
        if user_input:
            st.caption(f"當前文本長度：{len(user_input)} 字")
    with col2:
        st.write("提示：")
        if content_mode == "重點摘要":
            st.info("輸入要摘要的文本，AI將提取重要內容")
        elif content_mode == "結構化整理":
            st.info("輸入要整理的內容，AI將進行結構化處理")
        elif content_mode == "格式轉換":
            st.info("輸入要轉換的內容，AI將轉換為目標格式")
        else:
            st.info("輸入文本，AI將提取關鍵詞和重要概念")
    
    # 處理按鈕
    if st.button("開始處理"):
        if user_input:
            with st.spinner("處理中..."):
                # 根據不同模式處理內容
                if content_mode == "重點摘要":
                    prompt = st.session_state.content_processor.generate_summary(
                        user_input, length=summary_length
                    )
                elif content_mode == "結構化整理":
                    prompt = st.session_state.content_processor.structure_content(
                        user_input, format_type=format_type
                    )
                elif content_mode == "格式轉換":
                    prompt = st.session_state.content_processor.format_converter(
                        user_input, target_format=target_format
                    )
                else:  # 關鍵詞提取
                    prompt = st.session_state.content_processor.extract_keywords(user_input)
                
                # 獲取 AI 回應
                response = st.session_state.chat_manager.get_response(prompt)
                
                # 顯示結果
                st.markdown("### 處理結果")
                if content_mode == "格式轉換":
                    st.code(response, language=target_format)
                else:
                    st.markdown(response)
                
                # 保存到對話歷史
                st.session_state.messages.extend([
                    {"role": "user", "content": f"[{content_mode}] " + user_input},
                    {"role": "assistant", "content": response}
                ])
                
                # 添加下載按鈕（對於格式轉換）
                if content_mode == "格式轉換":
                    st.download_button(
                        label="下載結果",
                        data=response,
                        file_name=f"converted.{target_format}",
                        mime=f"text/{target_format}"
                    )
        else:
            st.warning("請輸入內容後再開始處理")

def main():
    st.title("AI 智能助手")
    
    # 初始化 session state
    initialize_session_state()
    
    # Sidebar - API 設定
    with st.sidebar:
        st.header("設定")
        api_key = st.text_input("輸入 Anthropic API Key", type="password")
        
        # Temperature 控制
        temperature = st.slider(
            "回應創意性",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="0.0 = 更確定性和專注, 1.0 = 更有創意和多樣性"
        )
        
        st.header("功能模式")
        mode = st.radio(
            "選擇模式",
            ["一般對話", "思維發想", "內容整理", "知識管理"],
            key="mode_selection"
        )
        
        if api_key:
            if st.session_state.chat_manager is None:
                st.session_state.chat_manager = ChatManager(api_key, temperature=temperature)
                st.success("API 連接成功！")
            else:
                # 更新 temperature
                st.session_state.chat_manager.set_temperature(temperature)
    
    # 主要內容區域
    if not api_key:
        st.warning("請先在側邊欄輸入 API Key")
        return
    
    # 更新當前模式
    st.session_state.current_mode = mode
    
    # 根據模式渲染不同介面
    if mode == "思維發想":
        render_thought_mode()
    elif mode == "內容整理":
        render_content_mode()
    else:
        # 對話區域
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # 使用者輸入
        if prompt := st.chat_input("輸入訊息..."):
            # 添加使用者訊息
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            # 處理回應
            with st.chat_message("assistant"):
                with st.spinner("思考中..."):
                    response = st.session_state.chat_manager.get_response(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main() 