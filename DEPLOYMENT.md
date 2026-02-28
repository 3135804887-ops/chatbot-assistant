# 部署指南

## 环境要求

- Python 3.8+
- Git
- GitHub账号
- 智谱AI API密钥

## 本地部署

### 1. 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/chatbot-assistant.git
cd chatbot-assistant
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
export ZHIPUAI_API_KEY="your_api_key_here"
```

### 4. 运行应用

```bash
streamlit run streamlit前端.py
```

## 云端部署

### Streamlit Cloud部署

#### 1. 创建GitHub仓库

访问 https://github.com/new 创建新仓库

#### 2. 推送代码

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/chatbot-assistant.git
git push -u origin main
```

#### 3. 部署到Streamlit Cloud

1. 访问 https://share.streamlit.io/
2. 使用GitHub登录
3. 点击 "New app"
4. 选择仓库和分支
5. 设置主文件路径: `streamlit前端.py`
6. 点击 "Deploy"

#### 4. 配置密钥

在Streamlit Cloud的Settings → Secrets中添加：

```toml
ZHIPUAI_API_KEY = "your_api_key_here"
```

## 其他部署方式

### Docker部署

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit前端.py"]
```

### 服务器部署

```bash
# 安装依赖
pip install -r requirements.txt

# 使用nohup后台运行
nohup streamlit run streamlit前端.py --server.port 8501 &

# 使用nginx反向代理
# 配置nginx.conf
```

## 常见问题

### 部署失败

检查以下项目：
- requirements.txt格式是否正确
- 主文件路径是否正确
- Python版本是否符合要求

### API调用失败

确认：
- API密钥是否正确配置
- 网络连接是否正常
- API额度是否充足

### 性能优化

建议：
- 使用缓存减少API调用
- 优化数据库查询
- 启用CDN加速

## 更新部署

```bash
git add .
git commit -m "Update"
git push
```

Streamlit Cloud会自动重新部署。
