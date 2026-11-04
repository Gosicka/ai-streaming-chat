# 基于 FastAPI 和 Streamlit 的本地 AI 流式聊天助手

在本机运行的聊天应用。Streamlit 负责对话界面，FastAPI 负责调用 DeepSeek。模型每生成一段文本，界面就立刻追加显示，不必等整段回复结束。

## 核心特性

- **DeepSeek 接入**：后端通过 OpenAI SDK 调用 DeepSeek 的兼容接口，模型为 `deepseek-chat`，服务地址为 `https://api.deepseek.com`。
- **流式打字机输出**：后端用 `StreamingResponse` 逐块返回文本；前端用 `requests` 的 `stream=True` 读取，再用 `st.write_stream` 渲染。
- **前后端分离**：界面与模型调用分开。前端只请求本地接口，API Key 只留在后端。

## 技术栈

| 组件 | 用途 |
| --- | --- |
| Python | 运行环境 |
| FastAPI | 后端 HTTP 服务，提供 `POST /chat` |
| Uvicorn | 运行 FastAPI |
| Streamlit | 聊天界面，展示历史记录和输入框 |
| OpenAI SDK | 以 OpenAI 兼容格式调用 DeepSeek |
| python-dotenv | 从 `.env` 读取 API Key |
| requests | 前端以流式方式请求后端 |

## 项目结构

```text
.
├── main.py            # FastAPI 后端
├── app.py             # Streamlit 前端
├── requirements.txt   # 依赖
├── .env               # 本地密钥，不要提交
└── .gitignore
```

`POST /chat` 接收 JSON：

```json
{"message": "你好"}
```

响应是 `text/plain; charset=utf-8` 的文本流，内容为模型陆续生成的文本片段。

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

### 4. 启动后端

保持虚拟环境处于激活状态，在第一个终端执行：

```powershell
uvicorn main:app --reload
```

看到 `Uvicorn running on http://127.0.0.1:8000` 后，后端即可访问。接口文档在 http://127.0.0.1:8000/docs 。这个终端需要一直开着。

### 5. 启动前端

另开一个终端，进入项目根目录，激活同一个虚拟环境后执行：

```powershell
.\venv\Scripts\Activate.ps1
streamlit run app.py
```

浏览器打开 http://127.0.0.1:8501 。在底部输入框发送消息，回复会逐段出现在上方的历史记录中。

关闭服务时，在对应终端按 `Ctrl+C`。
