import streamlit as st
import time
import json
import os
from datetime import datetime
from llm_service import llm_service
from config import config

# ---------- 页面配置 ----------
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.LAYOUT
)

# ---------- 数据持久化配置 ----------
DATA_FILE = "conversations.json"

def load_conversations():
    """从文件加载对话历史"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载对话历史失败: {e}")
            return []
    return []

def save_conversations():
    """保存对话历史到文件"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.conversations, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存对话历史失败: {e}")

# ---------- 初始化会话状态 ----------
if "conversations" not in st.session_state:
    # 从文件加载对话历史
    st.session_state.conversations = load_conversations()
    st.session_state.current_conversation_id = None

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "你好！我是你的智能助手。我可以帮你解答问题、提供建议、进行对话交流。有什么我可以帮你的吗？"}
    ]

# ---------- 辅助函数 ----------
def create_new_conversation():
    """创建新对话"""
    conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    conversation = {
        "id": conversation_id,
        "title": "新对话",
        "messages": [
            {"role": "assistant", "content": "你好！我是你的智能助手。我可以帮你解答问题、提供建议、进行对话交流。有什么我可以帮你的吗？"}
        ],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    st.session_state.conversations.insert(0, conversation)
    st.session_state.current_conversation_id = conversation_id
    st.session_state.messages = conversation["messages"]
    llm_service.clear_history()
    save_conversations()  # 保存到文件
    return conversation_id

def switch_conversation(conversation_id):
    """切换对话"""
    for conv in st.session_state.conversations:
        if conv["id"] == conversation_id:
            st.session_state.current_conversation_id = conversation_id
            st.session_state.messages = conv["messages"]
            break

def delete_conversation(conversation_id):
    """删除对话"""
    st.session_state.conversations = [
        conv for conv in st.session_state.conversations 
        if conv["id"] != conversation_id
    ]
    save_conversations()  # 保存到文件
    
    # 如果删除的是当前对话，切换到第一个对话或创建新对话
    if st.session_state.current_conversation_id == conversation_id:
        if st.session_state.conversations:
            switch_conversation(st.session_state.conversations[0]["id"])
        else:
            create_new_conversation()

def update_conversation_title(conversation_id, title):
    """更新对话标题"""
    for conv in st.session_state.conversations:
        if conv["id"] == conversation_id:
            conv["title"] = title
            save_conversations()  # 保存到文件
            break

def save_current_messages():
    """保存当前消息到对话历史"""
    if st.session_state.current_conversation_id:
        for conv in st.session_state.conversations:
            if conv["id"] == st.session_state.current_conversation_id:
                conv["messages"] = st.session_state.messages
                save_conversations()  # 保存到文件
                break

# ---------- 初始化第一个对话 ----------
if not st.session_state.conversations:
    create_new_conversation()
else:
    # 加载第一个对话
    if st.session_state.current_conversation_id is None:
        switch_conversation(st.session_state.conversations[0]["id"])

# ---------- 侧边栏（对话历史管理） ----------
with st.sidebar:
    st.title("智能助手")
    
    # 新对话按钮
    if st.button("新对话", use_container_width=True):
        create_new_conversation()
        st.rerun()
    
    st.markdown("---")
    
    # 显示对话历史列表
    st.subheader("对话历史")
    
    if st.session_state.conversations:
        for conv in st.session_state.conversations:
            # 创建对话项的容器
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # 对话按钮
                is_current = conv["id"] == st.session_state.current_conversation_id
                button_type = "primary" if is_current else "secondary"
                
                display_title = f"{'[当前] ' if is_current else ''}{conv['title'][:15]}{'...' if len(conv['title']) > 15 else ''}"
                
                if st.button(
                    display_title,
                    key=f"conv_{conv['id']}",
                    use_container_width=True,
                    type=button_type
                ):
                    switch_conversation(conv["id"])
                    st.rerun()
            
            with col2:
                # 删除按钮
                if st.button("删除", key=f"del_{conv['id']}"):
                    delete_conversation(conv["id"])
                    st.rerun()
            
            # 显示创建时间
            st.caption(f"{conv['created_at']}")
            st.markdown("---")
    
    # 系统信息
    st.subheader("系统信息")
    st.caption(f"大模型：{config.ZHIPUAI_MODEL}")
    st.caption(f"对话总数：{len(st.session_state.conversations)}")
    
    st.markdown("---")
    st.caption("当前版本：V3.1")

# ---------- 主聊天区域 ----------
# 显示所有历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 处理用户输入
if prompt := st.chat_input("例如：你好，你能帮我推荐一些好书吗？"):
    # 1. 将用户消息添加到历史并显示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. 使用流式输出显示AI回复
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 显示"正在思考"提示
        with st.spinner("正在思考..."):
            time.sleep(0.3)
        
        # 流式输出AI回复
        for chunk in llm_service.chat_stream(prompt):
            full_response += chunk
            message_placeholder.markdown(full_response)
        
        # 保存完整回复到历史
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # 保存消息到对话历史
        save_current_messages()
        
        # 如果是新对话的第一条消息，自动生成标题
        if len(st.session_state.messages) == 3:  # 欢迎消息 + 用户消息 + AI回复
            # 使用用户的第一条消息作为标题（截取前20个字符）
            title = prompt[:20] + "..." if len(prompt) > 20 else prompt
            update_conversation_title(st.session_state.current_conversation_id, title)
            st.rerun()
