from file_transform import get_df
import pandas as pd
import os
import argparse

def show_line(file_path, index):
    df = get_df(file_path)
    row = df.iloc[index]
    heads = df.columns
    s = f'# The number {index} line content\n\n'
    for i, head in enumerate(heads):
        s += f'## {head}\n\n{row[head]}\n\n'
    file_path = file_path.split('.')[0]
    output_path = f'{file_path}_{index}.md'
    with open(output_path, 'w') as f:
        f.write(s)
    print(f'Output to {output_path}')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='输入文件路径', default='data/output.xlsx')
    parser.add_argument('--index', type=int, help='行数', default=0)
    args = parser.parse_args()
    show_line(args.input, args.index)
    