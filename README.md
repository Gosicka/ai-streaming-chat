# 基于 Streamlit 的本地 AI 流式聊天助手

在本机运行的单进程聊天应用。Streamlit 同时负责对话界面和调用 DeepSeek。模型每生成一段文本，界面就立刻追加显示，不必等整段回复结束。

## 核心特性

- **DeepSeek 接入**：通过 OpenAI SDK 调用 DeepSeek 的兼容接口，模型为 `deepseek-chat`，服务地址为 `https://api.deepseek.com`。
- **流式打字机输出**：请求使用 `stream=True`，生成器逐块 `yield` 文本，再交给 `st.write_stream` 渲染。
- **单进程部署**：界面与模型调用在同一个 Streamlit 进程里，适合不支持多进程的免费云平台。API Key 从环境变量读取。

## 技术栈

| 组件 | 用途 |
| --- | --- |
| Python | 运行环境 |
| Streamlit | 聊天界面，展示历史记录和输入框，并直接调用模型 |
| OpenAI SDK | 以 OpenAI 兼容格式流式调用 DeepSeek |
| python-dotenv | 从 `.env` 读取 API Key |

## 项目结构

```text
.
├── app.py             # Streamlit 应用（界面 + 模型调用）
├── requirements.txt   # 依赖
├── .env               # 本地密钥，不要提交
└── .gitignore
```

## 本地运行指南

需要 Python 3.10 及以上。下面的命令在 Windows PowerShell 中执行，并假设当前目录是项目根目录。

### 1. 配置虚拟环境

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

激活成功后，提示符前会出现 `(venv)`。

### 2. 安装依赖

```powershell
pip install -r requirements.txt
```

如果访问官方 PyPI 超时，可以改用镜像：

```powershell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 60
```

### 3. 配置 API Key

在项目根目录创建 `.env`：

```text
DEEPSEEK_API_KEY=你的 DeepSeek API Key
```

密钥从 [DeepSeek 开放平台](https://platform.deepseek.com/) 获取。`.env` 已被 `.gitignore` 忽略，不要把密钥写进代码或提交到仓库。

### 4. 启动应用

保持虚拟环境处于激活状态，执行：

```powershell
streamlit run app.py
```

浏览器打开 http://127.0.0.1:8501 。在底部输入框发送消息，回复会逐段出现在上方的历史记录中。

关闭服务时，在终端按 `Ctrl+C`。
