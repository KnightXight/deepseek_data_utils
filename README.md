# 简要说明

> 所有函数和代码的借鉴价值远大于实际使用，可以直接import函数，也可以直接运行脚本，可以借鉴思路，也可以自行调整内容。
> 请记得调整config文件夹下的配置文件为自己所需，也可以在代码内部直接更改变量，看你喜好和需求。

## 0.To do

- [ ] 想要改一下一些代码的使用逻辑，yaml感觉并不适合每个人。
- [ ] 代码更为便捷的使用方法，命令行或者jupyter？

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
  - `write_df` 将获取到的DataFrame写入指定格式文件，一定是pandas可处理的DataFrame！

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

> 放弃多轮的迭代调用，如有需要请自行更改代码，
> 将config放到了外部文件便于代码管理

- 请预处理数据将需要的历史数据放到一对key/value的字典中。
- 配套`/config/key.yaml`和`/config/model_config.yaml`文件
- 请务必更改`/config/key.yaml`中的`api_key`为自己的API key
- 请务必更改`/config/model_config.yaml`中的各项参数为自己所需
- 并行调用模型

### issue

- 多轮数据函数
- 真实jsonl messages处理方法
