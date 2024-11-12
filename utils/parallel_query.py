from openai import OpenAI
import os
import json
import yaml
import requests
import time
import sys
import re
import pandas as pd
import numpy as np
import argparse
import multiprocessing
from functools import partial
from file_transform import get_df

### Golbal initialization
with open ('utils/config/model_config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
models = config['models']
prompt_template = config['prompt_template']
system_prompt = config['system_prompt']
max_tokens = config['max_tokens']
temperature = config['temperature']
columns = config['input_columns']

def get_key(model):
    with open ('utils/config/key.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    if 'deepseek' in model:
        key = config['deepseek']['key']
        url = config['deepseek']['url']
    else:
        key = config['openai']['key']
        url = config['openai']['url']
    return key, url

def get_variables(row, columns):
    variables = []
    for column in columns:
        variables.append(row[column])
    return variables

def get_messages(row):
    inputs = get_variables(row, input_columns)
    # history = get_variables(row, history_columns)
    query = prompt_template.format(*inputs)
    # history = [eval(h) for h in history]
    messages = [{'role':'system', 'content': system_prompt}] + [{'role':'user', 'content': query}]
    return messages

def query_model(model, row):
    messages = get_messages(row)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature
    )
    content = response.choices[0].message.content
    row[f"{model}_response"] = content
    return row

def multi_query(df, model): # requirement / material
    pool = multiprocessing.Pool(num_processes)
    func = partial(query_model, model=model)
    results = pool.map(func, df.iterrows())
    pool.close()
    pool.join()
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='输入文件路径', default='data/input.xlsx')
    parser.add_argument('--output', type=str, help='输出文件路径', default='data/output.xlsx')
    args = parser.parse_args()
    df = get_df(args.input)
    for model in models:
        key, url = get_key(model)
        client = OpenAI(api_key=key, base_url=url)
        df = multi_query(df, model)
    write_df(df, args.output)
    