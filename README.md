# 简要说明

## 1. utils结构

```shell
.
+-- README.md
+-- test.py
+-- file_transform.py
+-- model_query.py
+-- show_line.py
+-- vessel_code
\   +-- log_retrive.py
+-- config
\   +-- key.yaml # 请放私人key
\   +-- model_config.yaml
```

## 2. 文件说明

- `README.md`：本文件
- `file_transform.py`：文件格式转换
- `model_query.py`：调用模型（们）
- `show_line.py`：借助MD展示任意DataFrame
- `config/key.yaml`：存放API key等敏感信息
- `config/model_config.yaml`：存放模型配置信息

## 3. 使用说明

### 3.1 `file_transform.py`

- 文件格式转换
- 自动检测文件编码
- 两个函数
  - `get_df` 从任意文件获取DataFrame
  - `write_df` 将获取到的DataFrame写入指定格式文件

```shell
python file_transform.py -h
pyhton file_transform.py --input input_file --output output_file
```

### 3.2 `show_line.py`

- 展示文件第n行
- 输出到markdown文件
- 一个函数
  - `show_line` 展示文件第n行

```shell
python show_line.py -h
python show_line.py --input input_file --index line_index
```

### 3.3 `parallel_query.py`

> 暂时放弃多轮的调用，如有需要请自行更改代码，建议预处理数据将需要的历史数据放到一个key/value的字典中。

- 配套`/config/key.yaml`和`/config/model_config.yaml`文件
- 请务必更改`/config/key.yaml`中的`api_key`为自己的API key
- 请务必更改`/config/model_config.yaml`中的各项参数为自己所需
- 并行调用模型

### issue

- 多轮数据函数
- 真实jsonl messages处理方法
