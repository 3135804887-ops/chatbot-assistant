"""
用户认证服务
提供用户注册、登录、密码加密等功能
"""

import sqlite3
import hashlib
import secrets
from datetime import datetime
from typing import Optional, Dict, List
import os


class AuthService:
    """
    用户认证服务类
    """
    
    def __init__(self, db_path: str = "data/users.db"):
        """
        初始化认证服务
        
        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        self._ensure_data_dir()
        self._init_database()
    
    def _ensure_data_dir(self):
        """
        确保data目录存在
        """
        import os
        data_dir = os.path.dirname(self.db_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _init_database(self):
        """
        初始化数据库
        创建用户表、对话表和消息表
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建用户表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # 创建对话表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # 创建消息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _hash_password(self, password: str, salt: str) -> str:
        """
        密码加密
        
        Args:
            password: 原始密码
            salt: 盐值
        
        Returns:
            str: 加密后的密码
        """
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
    
    def register(self, username: str, email: str, password: str) -> Dict:
        """
        用户注册
        
        Args:
            username: 用户名
            email: 邮箱
            password: 密码
        
        Returns:
            Dict: 注册结果
        """
        try:
            # 生成盐值
            salt = secrets.token_hex(16)
            
            # 加密密码
            password_hash = self._hash_password(password, salt)
            
            # 插入数据库
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, salt)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, salt))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "message": "注册成功"
            }
        
        except sqlite3.IntegrityError as e:
            if "username" in str(e):
                return {
                    "success": False,
                    "message": "用户名已存在"
                }
            elif "email" in str(e):
                return {
                    "success": False,
                    "message": "邮箱已被注册"
                }
            else:
                return {
                    "success": False,
                    "message": "注册失败"
                }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"注册失败：{str(e)}"
            }
    
    def login(self, username: str, password: str) -> Dict:
        """
        用户登录
        
        Args:
            username: 用户名
            password: 密码
        
        Returns:
            Dict: 登录结果
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 查询用户
            cursor.execute('''
                SELECT id, username, email, password_hash, salt
                FROM users
                WHERE username = ?
            ''', (username,))
            
            user = cursor.fetchone()
            
            if not user:
                conn.close()
                return {
                    "success": False,
                    "message": "用户名或密码错误"
                }
            
            user_id, username, email, password_hash, salt = user
            
            # 验证密码
            if self._hash_password(password, salt) != password_hash:
                conn.close()
                return {
                    "success": False,
                    "message": "用户名或密码错误"
                }
            
            # 更新最后登录时间
            cursor.execute('''
                UPDATE users
                SET last_login = ?
                WHERE id = ?
            ''', (datetime.now(), user_id))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "message": "登录成功",
                "user": {
                    "id": user_id,
                    "username": username,
                    "email": email
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"登录失败：{str(e)}"
            }
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """
        获取用户信息
        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[Dict]: 用户信息
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, username, email, created_at, last_login
                FROM users
                WHERE id = ?
            ''', (user_id,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "created_at": user[3],
                    "last_login": user[4]
                }
            
            return None
        
        except Exception as e:
            print(f"获取用户信息失败：{e}")
            return None
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> Dict:
        """
        修改密码
        
        Args:
            user_id: 用户ID
            old_password: 旧密码
            new_password: 新密码
        
        Returns:
            Dict: 修改结果
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 获取用户信息
            cursor.execute('''
                SELECT password_hash, salt
                FROM users
                WHERE id = ?
            ''', (user_id,))
            
            user = cursor.fetchone()
            
            if not user:
                conn.close()
                return {
                    "success": False,
                    "message": "用户不存在"
                }
            
            password_hash, salt = user
            
            # 验证旧密码
            if self._hash_password(old_password, salt) != password_hash:
                conn.close()
                return {
                    "success": False,
                    "message": "旧密码错误"
                }
            
            # 生成新盐值和密码
            new_salt = secrets.token_hex(16)
            new_password_hash = self._hash_password(new_password, new_salt)
            
            # 更新密码
            cursor.execute('''
                UPDATE users
                SET password_hash = ?, salt = ?
                WHERE id = ?
            ''', (new_password_hash, new_salt, user_id))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "message": "密码修改成功"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"密码修改失败：{str(e)}"
            }
    
    # ========== 对话管理 ==========
    
    def create_conversation(self, user_id: int, title: str = "新对话") -> Dict:
        """
        创建新对话
        
        Args:
            user_id: 用户ID
            title: 对话标题
        
        Returns:
            Dict: 创建结果
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO conversations (user_id, title)
                VALUES (?, ?)
            ''', (user_id, title))
            
            conversation_id = cursor.lastrowid
            
            # 添加欢迎消息
            cursor.execute('''
                INSERT INTO messages (conversation_id, role, content)
                VALUES (?, ?, ?)
            ''', (conversation_id, "assistant", "你好！我是你的智能助手。我可以帮你解答问题、提供建议、进行对话交流。有什么我可以帮你的吗？"))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "conversation_id": conversation_id
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"创建对话失败：{str(e)}"
            }
    
    def get_user_conversations(self, user_id: int) -> List[Dict]:
        """
        获取用户的所有对话
        
        Args:
            user_id: 用户ID
        
        Returns:
            List[Dict]: 对话列表
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, created_at, updated_at
                FROM conversations
                WHERE user_id = ?
                ORDER BY updated_at DESC
            ''', (user_id,))
            
            conversations = []
            for row in cursor.fetchall():
                conversations.append({
                    "id": row[0],
                    "title": row[1],
                    "created_at": row[2],
                    "updated_at": row[3]
                })
            
            conn.close()
            return conversations
        
        except Exception as e:
            print(f"获取对话列表失败：{e}")
            return []
    
    def get_conversation_messages(self, conversation_id: int, user_id: int) -> List[Dict]:
        """
        获取对话的所有消息
        
        Args:
            conversation_id: 对话ID
            user_id: 用户ID（用于权限验证）
        
        Returns:
            List[Dict]: 消息列表
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 验证对话是否属于该用户
            cursor.execute('''
                SELECT id FROM conversations
                WHERE id = ? AND user_id = ?
            ''', (conversation_id, user_id))
            
            if not cursor.fetchone():
                conn.close()
                return []
            
            # 获取消息
            cursor.execute('''
                SELECT role, content, created_at
                FROM messages
                WHERE conversation_id = ?
                ORDER BY created_at ASC
            ''', (conversation_id,))
            
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    "role": row[0],
                    "content": row[1],
                    "created_at": row[2]
                })
            
            conn.close()
            return messages
        
        except Exception as e:
            print(f"获取消息失败：{e}")
            return []
    
    def add_message(self, conversation_id: int, user_id: int, role: str, content: str) -> Dict:
        """
        添加消息到对话
        
        Args:
            conversation_id: 对话ID
            user_id: 用户ID（用于权限验证）
            role: 角色（user/assistant）
            content: 消息内容
        
        Returns:
            Dict: 添加结果
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 验证对话是否属于该用户
            cursor.execute('''
                SELECT id FROM conversations
                WHERE id = ? AND user_id = ?
            ''', (conversation_id, user_id))
            
            if not cursor.fetchone():
                conn.close()
                return {
                    "success": False,
                    "message": "对话不存在或无权限"
                }
            
            # 添加消息
            cursor.execute('''
                INSERT INTO messages (conversation_id, role, content)
                VALUES (?, ?, ?)
            ''', (conversation_id, role, content))
            
            # 更新对话的更新时间
            cursor.execute('''
                UPDATE conversations
                SET updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (conversation_id,))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"添加消息失败：{str(e)}"
            }
    
    def update_conversation_title(self, conversation_id: int, user_id: int, title: str) -> Dict:
        """
        更新对话标题
        
        Args:
            conversation_id: 对话ID
            user_id: 用户ID（用于权限验证）
            title: 新标题
        
        Returns:
            Dict: 更新结果
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 验证对话是否属于该用户
            cursor.execute('''
                SELECT id FROM conversations
                WHERE id = ? AND user_id = ?
            ''', (conversation_id, user_id))
            
            if not cursor.fetchone():
                conn.close()
                return {
                    "success": False,
                    "message": "对话不存在或无权限"
                }
            
            # 更新标题
            cursor.execute('''
                UPDATE conversations
                SET title = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (title, conversation_id))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"更新标题失败：{str(e)}"
            }
    
    def delete_conversation(self, conversation_id: int, user_id: int) -> Dict:
        """
        删除对话
        
        Args:
            conversation_id: 对话ID
            user_id: 用户ID（用于权限验证）
        
        Returns:
            Dict: 删除结果
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 验证对话是否属于该用户
            cursor.execute('''
                SELECT id FROM conversations
                WHERE id = ? AND user_id = ?
            ''', (conversation_id, user_id))
            
            if not cursor.fetchone():
                conn.close()
                return {
                    "success": False,
                    "message": "对话不存在或无权限"
                }
            
            # 删除消息
            cursor.execute('''
                DELETE FROM messages
                WHERE conversation_id = ?
            ''', (conversation_id,))
            
            # 删除对话
            cursor.execute('''
                DELETE FROM conversations
                WHERE id = ?
            ''', (conversation_id,))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"删除对话失败：{str(e)}"
            }


# 创建全局认证服务实例
auth_service = AuthService()
