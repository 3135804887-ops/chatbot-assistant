# Streamlit Cloud 部署指南

## 前置准备

### 1. 创建GitHub账号
如果还没有GitHub账号，请先注册：https://github.com/

### 2. 安装Git
下载并安装Git：https://git-scm.com/downloads

## 部署步骤

### 第一步：初始化Git仓库

在项目目录下打开终端，执行以下命令：

```bash
# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit: 智能对话助手"
```

### 第二步：创建GitHub仓库

1. 登录GitHub
2. 点击右上角的"+"号，选择"New repository"
3. 填写仓库信息：
   - Repository name: `chatbot-assistant`
   - Description: `基于智谱AI的智能对话助手`
   - 选择"Public"（公开）
   - 不要勾选"Add a README file"（我们已经有了）
4. 点击"Create repository"

### 第三步：推送到GitHub

按照GitHub页面上的提示，执行以下命令：

```bash
# 添加远程仓库（替换YOUR_USERNAME为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/chatbot-assistant.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

### 第四步：部署到Streamlit Cloud

1. 访问Streamlit Cloud：https://share.streamlit.io/
2. 使用GitHub账号登录
3. 点击"New app"
4. 填写部署信息：
   - Repository: 选择你的仓库 `YOUR_USERNAME/chatbot-assistant`
   - Branch: `main`
   - Main file path: `streamlit前端.py`
   - App name: `chatbot-assistant`（或你喜欢的名字）
5. 点击"Deploy"

### 第五步：配置环境变量

在Streamlit Cloud上配置API密钥：

1. 在应用页面点击"Settings"
2. 点击"Secrets"
3. 添加以下内容：

```toml
ZHIPUAI_API_KEY = "你的智谱AI API密钥"
```

4. 点击"Save"
5. 应用会自动重启

## 访问应用

部署成功后，你会获得一个URL，格式如下：
```
https://chatbot-assistant-xxxxx.streamlit.app
```

这个URL可以：
- 分享给其他人使用
- 放在简历上
- 嵌入到个人网站

## 更新应用

当你修改代码后，只需：

```bash
# 添加修改的文件
git add .

# 提交更改
git commit -m "更新功能描述"

# 推送到GitHub
git push
```

Streamlit Cloud会自动检测更新并重新部署。

## 常见问题

### Q: 部署失败怎么办？
A: 检查以下几点：
1. `requirements.txt` 是否正确
2. 主文件路径是否正确
3. 环境变量是否配置
4. 查看部署日志排查错误

### Q: 如何查看部署日志？
A: 在Streamlit Cloud应用页面，点击右上角的"Manage app"，可以查看实时日志。

### Q: 如何修改应用名称？
A: 在Streamlit Cloud的Settings中修改App name，然后重新部署。

### Q: 如何删除应用？
A: 在Streamlit Cloud的Settings中点击"Delete app"。

## 性能优化建议

1. **减少依赖包**：只保留必要的依赖
2. **优化代码**：减少不必要的计算
3. **使用缓存**：Streamlit提供了`@st.cache_data`装饰器
4. **异步处理**：对于耗时操作使用异步

## 成本说明

Streamlit Cloud免费版限制：
- 每月200小时运行时间
- 1GB内存
- 公开仓库

对于个人项目和简历展示完全够用！

## 下一步

部署成功后，你可以：
1. 在简历上添加项目链接
2. 分享给朋友使用
3. 继续开发新功能
4. 收集用户反馈

祝你部署顺利！🎉
