import pandas as pd
import os
import argparse

def get_df(file_path):
    file_extension = file_path.split('.')[-1].lower()
    if file_extension == 'jsonl':
        return pd.read_json(file_path, lines=True)
    if file_extension == 'xlsx':
        return pd.read_excel(file_path)
    try:
        read_func = getattr(pd, f'read_{file_extension}')
        df = read_func(file_path)
        return df
    except AttributeError:
        raise ValueError(f"不支持的文件格式: {file_extension}")
    
def write_df(df, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    end = output_path.split('.')[-1].lower()
    if end == 'jsonl':
        df.to_json(output_path, orient='records', lines=True, force_ascii=False)
    elif end == 'xlsx':
        df.to_excel(output_path, index=False)
    else:
        try:
            write_func = getattr(df, f'to_{end}')
            write_func(output_path, index=False)
        except AttributeError:
            raise ValueError(f"不支持的文件格式: {end}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='输入文件路径')
    parser.add_argument('--output', type=str, help='输出文件路径')
    args = parser.parse_args()
    df = get_df(args.input)
    write_df(df, args.output)