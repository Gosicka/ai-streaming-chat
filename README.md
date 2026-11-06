# AI 流式聊天助手

基于 Streamlit 的单进程对话应用。界面和模型调用放在同一个进程里，通过 OpenAI SDK 以兼容接口调用 DeepSeek（`deepseek-chat`）。模型按流式返回，回复随生成过程逐段显示。

## 功能

- **流式输出**：请求使用 `stream=True`，逐块读取增量文本，再交给 `st.write_stream` 渲染。
- **多轮会话**：界面保留当前会话的历史消息，后续请求会带上这些消息，模型可以延续上文。
- **用量控制**：单次输入不超过 1000 字，单次回复不超过 1024 token，单个会话累计不超过 30000 字。达到上限后停止发送，避免连续请求放大接口调用量。
- **密钥管理**：API Key 只从环境变量 `DEEPSEEK_API_KEY` 读取，不写入代码。

## 技术栈

| 组件 | 用途 |
| --- | --- |
| Python 3.10+ | 运行环境 |
| Streamlit | 对话界面与会话状态 |
| OpenAI SDK | 以 OpenAI 兼容格式调用 DeepSeek |
| python-dotenv | 从本地 `.env` 加载配置 |

## 项目结构

```text
.
├── app.py                  # 界面、会话状态与模型调用
├── requirements.txt        # 依赖
├── .streamlit/config.toml  # 关闭使用统计与邮箱提示
├── .env.example            # 环境变量示例
└── .gitignore
```

## 本地运行

需要 Python 3.10 及以上。在项目根目录执行，以下命令以 Windows PowerShell 为例。

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

macOS / Linux 将激活命令换为 `source venv/bin/activate`，复制示例配置使用 `cp .env.example .env`。

在 `.env` 中填入从 [DeepSeek 开放平台](https://platform.deepseek.com/) 获取的密钥：

```text
DEEPSEEK_API_KEY=your_api_key
```

启动应用：

```powershell
streamlit run app.py
```

浏览器打开 http://127.0.0.1:8501 ，在输入框发送消息即可。结束进程使用 `Ctrl+C`。

安装依赖时如果访问 PyPI 较慢，可以改用镜像：

```powershell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 60
```

## 说明

应用不单独启动后端服务，部署时只需运行一个 Streamlit 进程。`.env` 已在 `.gitignore` 中忽略，请勿将密钥提交到仓库。
