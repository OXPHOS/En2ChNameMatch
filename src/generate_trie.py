import pygtrie
import pickle
import pandas as pd
import os
from src import input_path, dict_path


def generate_trie(df, f):
    trie = pygtrie.CharTrie(df.to_dict('index'))

    if not os.path.exists(dict_path):
        os.makedirs(dict_path)
    file = open(f, 'wb')
    pickle.dump(trie, file)
    file.close()

    return trie


def parse_person_file(suffix=None):
    df1 = pd.read_excel(os.path.join(input_path, '世界人名翻译大辞典.xlsx'), sheet_name=0, skiprows=[0, 1],
                        header=None, index_col=0, encoding='utf-8')
    df2 = pd.read_excel(os.path.join(input_path, '世界人名翻译大辞典.xlsx'), sheet_name=1, skiprows=[0, 1],
                        header=None, index_col=0, encoding='utf-8')
    df = pd.concat([df1, df2], axis=0).applymap(str)
    df.columns = ['Name', 'Region', 'CH']
    df = df[~(df['CH']=='nan')]
    if suffix:
        df['Region:CH'] = '(' + df.Region + ')' + df.CH + '(%s)' %suffix
    else:
        df['Region:CH'] = '(' + df.Region + ')' + df.CH
    df = df[['Name', 'Region:CH']]

    df.Name = df.Name.str.replace('<sup>′</sup>', '′')
    df.Name = df.Name.str.replace('&#211；', 'Ó')
    df.Name = df.Name.str.replace('&#272；', 'Đ')
    df.Name = df.Name.str.lower()

    df = df.groupby('Name').agg({'Region:CH': lambda x:' | '.join(x)})
    return df


def parse_place_file(suffix=None):
    df = pd.read_excel(os.path.join(input_path, '世界地名翻译大辞典.xlsx'), sheet_name=0, skiprows=[0, 1],
                       header=None, index_col=0, encoding='utf-8').applymap(str)
    df.columns = ['Name', 'Region', 'CH']
    df = df[~(df['CH']=='nan')]
    if suffix:
        df['Region:CH'] = '(' + df.Region + ')' + df.CH + '(%s)' %suffix
    else:
        df['Region:CH'] = '(' + df.Region + ')' + df.CH
    df = df[['Name', 'Region:CH']]

    # alias = df.Name.str.split('见')
    # new_entry = []
    # for i in alias.index:
    #     if len(alias[i]) > 1:
    #         for j in range(1, len(alias[i])):
    #             new_entry.append([alias[i][j], df['Region:CH'][i]])
    #         df.Name[i] = alias[i][0]
    # df =  pd.concat([df, pd.DataFrame(new_entry, columns=['Name', 'Region:CH'])], axis=0).reset_index(drop=True)
    df.Name = list(map(lambda x:x[0], df.Name.str.split(' 见')))
    df.Name = list(map(lambda x: x[0], df.Name.str.split('见')))
    df.Name = df.Name.str.replace('&#272；', 'Đ')
    df.Name = df.Name.str.lower()

    df = df.groupby('Name').agg({'Region:CH': lambda x:' | '.join(x)})
    return df


def generate_person_trie(f):
    df = parse_person_file()
    trie = generate_trie(df, f)
    return trie


def generate_place_trie(f):
    df = parse_place_file()
    trie = generate_trie(df, f)
    return trie


def generate_merge_trie(f):
    df1 = parse_person_file(suffix='人物')
    df2 = parse_place_file(suffix='地点')
    df = pd.concat([df1.reset_index(), df2.reset_index()], axis=0)
    df = df.groupby('Name').agg({'Region:CH': lambda x:' | '.join(x)})

    trie = generate_trie(df, f)
    return trie

if __name__=='__main__':
    generate_person_trie(os.path.join(dict_path, '人名词典'))
    generate_place_trie(os.path.join(dict_path, '地名词典'))
    generate_merge_trie(os.path.join(dict_path, '人名+地名词典'))
