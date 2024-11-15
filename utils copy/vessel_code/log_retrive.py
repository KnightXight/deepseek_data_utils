import os
from tqdm.contrib.concurrent import process_map
import json
from datetime import datetime
import os
from functools import partial
import re
def compare_dates(date1: str, date2: str) -> int:
    """
    比较两个日期字符串的大小。
    参数:
    date1 (str): 第一个日期字符串，格式为"MM-DD"
    date2 (str): 第二个日期字符串，格式为"MM-DD"
    返回:
    int: 如果date1 < date2，返回-1；如果date1 > date2，返回1；如果date1 == date2，返回0
    """
    # 将日期字符串转换为datetime对象
    date_format = "%m-%d"
    d1 = datetime.strptime(date1, date_format)
    d2 = datetime.strptime(date2, date_format)
    # 比较日期
    if d1 < d2:
        return True
    return False
# pattern = re.compile(r"小红书|抖音|快手|推特|自媒体|自媒体文案|帖子|公众号|豆瓣|口播|种草|微博|知乎|微信|热点标题|推文|图文|Twitter|朋友圈|评论|短视频文案|博主|emoji|视频解说|梗|爆文")
# delete_pattern = re.compile(r"扩写|阅读下面材料|阅读下面文字|JSON|总结以下内容|翻译|ranslate")
# pattern = re.compile(r"小红书|抖音|快手|帖子|微博|知乎|微信|公众号|直播|推文|口播")
# delete_pattern = re.compile(r"=|```") # 一般有很多数据都可以直接过滤掉，比如翻译、包含= ``` $$的代码数学等
pattern = re.compile(r"你会怎么办|你会怎么做|老板|领导|老婆|老公|伴侣|男友|女友|女生")
print(pattern)
def process_file(path, output_base_path):
    file_name = path.split("/")[-1]
    output_path = os.path.join(output_base_path, file_name)
    with open(path) as f:
        for row, line in enumerate(f):
            # 一些捞数据的条件，可依据需求修改
            try:
                line = json.loads(line)
                answer = "\n".join([str(msg["content"]) for msg in line["messages"] if msg["role"] != "assistant"])
                match_pattern = pattern.search(answer)
                if match_pattern:
                    # if delete_pattern.search(answer):
                    #     continue
                    matched = match_pattern.group(0)
                    line["match"] = matched
                    with open(output_path, "a") as fout:
                        line["yangxy_file"] = path
                        fout.write(json.dumps(line, ensure_ascii=False) + '\n')
            except:
                pass
base_path = "/hf3fs-jd/prod/deepseek/shared/luxuan/jsonl"
save_path = "/weka-jd/prod/deepseek/permanent/shared/xuebing/general_sft/data/tmp_data/ambiguity"
to_traverse = []
for file_name in os.listdir(base_path):
    # 选择哪些原文件来捞，一般只遍历.sample.jsonl就行，主要看要捞web端还是api端
    if "sample" not in file_name:
        continue
    if ".tempxxx" in file_name:
        continue
    if "web" not in file_name:
        continue
    date = file_name.split("2024")[-1][1:].replace(".sample.jsonl", "")
    # 选择时间范围
    if compare_dates(date, "10-14") and compare_dates("10-10", date):
        to_traverse.append(os.path.join(base_path, file_name))
print(len(to_traverse))
process_map(partial(process_file, output_base_path=save_path), to_traverse, max_workers=40)
# process_file(to_traverse[0], save_path)