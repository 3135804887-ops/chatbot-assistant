import streamlit as st
import time
from datetime import datetime
from llm_service import llm_service
from auth_service import auth_service
from config import config

# ---------- 页面配置 ----------
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.LAYOUT
)

# ---------- 初始化会话状态 ----------
if "user" not in st.session_state:
    st.session_state.user = None

if "current_conversation_id" not in st.session_state:
    st.session_state.current_conversation_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- 辅助函数 ----------
def create_new_conversation():
    """创建新对话"""
    if not st.session_state.user:
        return
    
    result = auth_service.create_conversation(
        st.session_state.user["id"],
        "新对话"
    )
    
    if result["success"]:
        st.session_state.current_conversation_id = result["conversation_id"]
        # 加载欢迎消息
        messages = auth_service.get_conversation_messages(
            result["conversation_id"],
            st.session_state.user["id"]
        )
        st.session_state.messages = messages
        llm_service.clear_history()

def switch_conversation(conversation_id):
    """切换对话"""
    if not st.session_state.user:
        return
    
    messages = auth_service.get_conversation_messages(
        conversation_id,
        st.session_state.user["id"]
    )
    
    if messages:
        st.session_state.current_conversation_id = conversation_id
        st.session_state.messages = messages

def delete_conversation(conversation_id):
    """删除对话"""
    if not st.session_state.user:
        return
    
    result = auth_service.delete_conversation(
        conversation_id,
        st.session_state.user["id"]
    )
    
    if result["success"]:
        # 如果删除的是当前对话，切换到其他对话或创建新对话
        if st.session_state.current_conversation_id == conversation_id:
            conversations = auth_service.get_user_conversations(st.session_state.user["id"])
            if conversations:
                switch_conversation(conversations[0]["id"])
            else:
                create_new_conversation()

def update_conversation_title(conversation_id, title):
    """更新对话标题"""
    if not st.session_state.user:
        return
    
    auth_service.update_conversation_title(
        conversation_id,
        st.session_state.user["id"],
        title
    )

def save_message(role, content):
    """保存消息到数据库"""
    if not st.session_state.user or not st.session_state.current_conversation_id:
        return
    
    auth_service.add_message(
        st.session_state.current_conversation_id,
        st.session_state.user["id"],
        role,
        content
    )

# ---------- 登录注册页面 ----------
def show_login_page():
    """显示登录注册页面"""
    st.title("智能对话助手")
    
    tab1, tab2 = st.tabs(["登录", "注册"])
    
    with tab1:
        st.subheader("用户登录")
        
        username = st.text_input("用户名", key="login_username")
        password = st.text_input("密码", type="password", key="login_password")
        
        if st.button("登录", use_container_width=True):
            if not username or not password:
                st.error("请输入用户名和密码")
            else:
                result = auth_service.login(username, password)
                
                if result["success"]:
                    st.session_state.user = result["user"]
                    
                    # 加载用户的对话
                    conversations = auth_service.get_user_conversations(st.session_state.user["id"])
                    if conversations:
                        switch_conversation(conversations[0]["id"])
                    else:
                        create_new_conversation()
                    
                    st.rerun()
                else:
                    st.error(result["message"])
    
    with tab2:
        st.subheader("用户注册")
        
        username = st.text_input("用户名", key="register_username")
        email = st.text_input("邮箱", key="register_email")
        password = st.text_input("密码", type="password", key="register_password")
        confirm_password = st.text_input("确认密码", type="password", key="register_confirm_password")
        
        if st.button("注册", use_container_width=True):
            if not username or not email or not password:
                st.error("请填写所有字段")
            elif password != confirm_password:
                st.error("两次密码不一致")
            elif len(password) < 6:
                st.error("密码长度至少6位")
            else:
                result = auth_service.register(username, email, password)
                
                if result["success"]:
                    st.success("注册成功！请登录")
                else:
                    st.error(result["message"])

# ---------- 主聊天页面 ----------
def show_chat_page():
    """显示主聊天页面"""
    
    # ---------- 侧边栏 ----------
    with st.sidebar:
        st.title("智能助手")
        
        # 用户信息
        st.write(f"欢迎，{st.session_state.user['username']}")
        
        if st.button("退出登录", use_container_width=True):
            st.session_state.user = None
            st.session_state.current_conversation_id = None
            st.session_state.messages = []
            st.rerun()
        
        if st.button("新对话", use_container_width=True):
            create_new_conversation()
            st.rerun()
        
        st.markdown("---")
        
        # 显示对话历史
        st.subheader("对话历史")
        
        conversations = auth_service.get_user_conversations(st.session_state.user["id"])
        
        if conversations:
            for conv in conversations:
                col1, col2 = st.columns([4, 1])
                
                with col1:
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
                    if st.button("删除", key=f"del_{conv['id']}"):
                        delete_conversation(conv["id"])
                        st.rerun()
                
                st.caption(f"{conv['created_at']}")
                st.markdown("---")
        
        # 系统信息
        st.subheader("系统信息")
        st.caption(f"大模型：{config.ZHIPUAI_MODEL}")
        st.caption(f"对话总数：{len(conversations)}")
        
        st.markdown("---")
        st.caption("当前版本：V4.0")
    
    # ---------- 主聊天区域 ----------
    # 显示所有历史消息
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # 处理用户输入
    if prompt := st.chat_input("例如：你好，你能帮我推荐一些好书吗？"):
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        save_message("user", prompt)
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 流式输出AI回复
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            with st.spinner("正在思考..."):
                time.sleep(0.3)
            
            for chunk in llm_service.chat_stream(prompt):
                full_response += chunk
                message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            save_message("assistant", full_response)
            
            # 自动生成标题
            if len(st.session_state.messages) == 3:
                title = prompt[:20] + "..." if len(prompt) > 20 else prompt
                update_conversation_title(st.session_state.current_conversation_id, title)
                st.rerun()

# ---------- 主程序 ----------
def main():
    """主程序"""
    if not st.session_state.user:
        show_login_page()
    else:
        show_chat_page()

if __name__ == "__main__":
    main()
