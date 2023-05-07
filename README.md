# audioConversation-ChatGLM

该项目是基于ChatGLM实现的一个语音对话工具（英语），其中涉及到的AI工具基本都是开源的，整个过程不需要翻墙，不需要使用openAI的key，只需要本地GPU大于等于12G即可。

### 环境安装

首先需要使用以下命令安装ffmpeg工具
```shell
sudo apt install ffmpeg
```

使用 pip 安装依赖：`pip install -r requirements.txt`，其中 `transformers` 库版本推荐为 `4.27.1`，但理论上不低于 `4.23.1` 即可。

此外，如果需要在 cpu 上运行量化后的模型，还需要安装 `gcc` 与 `openmp`。多数 Linux 发行版默认已安装。对于 Windows ，可在安装 [TDM-GCC](https://jmeubank.github.io/tdm-gcc/) 时勾选 `openmp`。 Windows 测试环境 `gcc` 版本为 `TDM-GCC 10.3.0`， Linux 为 `gcc 11.3.0`。

如果你的内存不足，可以直接加载量化后的模型：

```python
# INT8 量化的模型将"THUDM/chatglm-6b-int4"改为"THUDM/chatglm-6b-int8"
model = AutoModel.from_pretrained("THUDM/chatglm-6b-int4",trust_remote_code=True).float()
```

如果遇到了报错 `Could not find module 'nvcuda.dll'` 或者 `RuntimeError: Unknown platform: darwin` (MacOS) ，请[从本地加载模型](README.md#从本地加载模型)

### Mac 上的 GPU 加速
对于搭载了Apple Silicon的Mac（以及MacBook），可以使用 MPS 后端来在 GPU 上运行 ChatGLM-6B。需要参考 Apple 的 [官方说明](https://developer.apple.com/metal/pytorch) 安装 PyTorch-Nightly。

目前在 MacOS 上只支持[从本地加载模型](README.md#从本地加载模型)。将代码中的模型加载改为从本地加载，并使用 mps 后端
```python
model = AutoModel.from_pretrained("your local path", trust_remote_code=True).half().to('mps')
```
即可使用在 Mac 上使用 GPU 加速模型推理。


### 本地启动
在Linux环境下运行start.sh脚本即可，然后使用chrome浏览器或者MicroSoft EDGE浏览器打开web_index.html，给予语音权限，即可开始对话。

### 未来规划
当前项目并不完善，前端页面很简陋，后续会优化页面展示以及功能，包括对话历史等。同时，也会增加其他模型的接入（主要是各类小模型），最终希望能够在不使用GPU或者使用低性能GPU的情况下依旧能够实现流畅对话的能力。

## 协议

本仓库的代码依照 [Apache-2.0](LICENSE) 协议开源，ChatGLM-6B 模型的权重的使用则需要遵循 [Model License](MODEL_LICENSE)。


