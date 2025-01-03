import pandas as pd
import numpy as np
import copy
import json

# 常量定义
DATA_PATH = './data/'
RESULT_PATH = './result/'
FILE_EXTEND = '.xlsx'
JSON_NAME = 'prcessed.json'
nation_field_binname_binrange_dict = {}  # 国家-变量-分桶名称-分桶范围字典

# 桶-分级名称映射关系
level_dict = {
    2: ['low',  'high'],
    3: ['low', 'medium', 'high'],
    4: ['very_low', 'low', 'medium', 'high'],
    5: ['very_low', 'low', 'medium', 'high', 'very_high']
}

# 所有国家，用于快速参考 TODO
all_nations = ['Albania', 'Armenia', 'Azerbaijan', 'Belarus', 'Bulgaria', 'China','Croatia','Cyprus',
               'Czech Republic','Egypt','Estonia','Georgia','Greece','Hungary','India','Indonesia',
               'Iran','Israel','Jordan','Kazakhstan','Kyrgyzstan','Latvia','Lithuania','Malaysia',
               'Pakistan','Philippines','Poland','Romania','Russia','Saudi Arabia','Slovakia','Slovenia',
               'Sri Lanka','Tajikistan','Turkey','Turkmenistan','Ukraine','Vietnam','Yemen'
               ]
# 可被批量分桶处理的国家
enable_nations = ['Albania', 'Armenia', 'Azerbaijan', 'Belarus', 'Bulgaria', 'China','Croatia','Cyprus',
               'Czech Republic','Egypt','Estonia','Georgia','Greece','Hungary','India','Indonesia',
               'Iran','Israel','Jordan','Kazakhstan','Kyrgyzstan','Latvia','Lithuania','Malaysia',
               'Pakistan','Philippines','Poland','Romania','Russia','Saudi Arabia','Slovakia','Slovenia',
               'Sri Lanka','Tajikistan','Turkey','Turkmenistan','Ukraine','Vietnam','Yemen'
               ]

# 分桶处理函数
def convert_value_to_bin(row):
    bin_num = bin_level_mapping_dict.get(row.name)
    print("这个字段 %s 的桶数是 %s." % (row.name, str(bin_num)))
    if np.isnan(np.array([bin_num], dtype=np.float32)):
        print("这个字段 %s 的桶数是nan，跳出分桶操作." % row.name)
        return row

    bin_num = int(bin_num)
    bin_level_names = level_dict.get(bin_num)
    print("这个字段 %s 的分桶后的名称是 %s." % (row.name, str(bin_level_names)))

    row = pd.cut(row, bins=bin_num, labels=bin_level_names)

    return row


# json汇总函数

def json_group(row, field_binname_binrange_dict):
    bin_num = bin_level_mapping_dict.get(row.name)
    print("这个字段 %s 的桶数是 %s." % (row.name, str(bin_num)))
    if np.isnan(np.array([bin_num], dtype=np.float32)):
        print("这个字段 %s 的桶数是nan，塞入空串." % row.name)
        field_binname_binrange_dict[row.name] = ''
        return row

    bin_num = int(bin_num)
    bin_level_names = level_dict.get(bin_num)
    print("这个字段 %s 的分桶后的名称是 %s." % (row.name, str(bin_level_names)))

    # 整理并保存分桶信息
    categorys = sorted(list(pd.cut(row, bin_num).unique()), key=lambda x: x.left)  # 低->高排序
    categorys = [str(cate) for cate in categorys]
    field_binname_binrange_dict[row.name] = dict(zip(bin_level_names, categorys))

    return row


if __name__ == '__main__':
    print("begin!")

    bin_nation_mapping_df = pd.read_excel(''.join([DATA_PATH, 'bin_nation_mapping', FILE_EXTEND]), index_col='NATION')
    bin_nation_mapping_dict = bin_nation_mapping_df.to_dict(orient='index')
    print("已获取桶数-国家的映射关系。")

    print("需要批量处理的国家为： %s" % str(enable_nations))
    for nation_index, enable_nation in enumerate(enable_nations):
        field_binname_binrange_dict = {}
        nation_field_binname_binrange_dict[enable_nation] = field_binname_binrange_dict

        excel_name = ''.join([enable_nation, FILE_EXTEND])
        raw_nation_df = pd.read_excel(DATA_PATH + excel_name).astype(float)
        print("获取国家名称为：%s 的数据信息。" % enable_nation)

        bin_level_mapping_dict = bin_nation_mapping_dict.get(enable_nation)
        print("获取国家名称为：%s 的桶-级别映射关系： %s" % (enable_nation, str(bin_level_mapping_dict)))

        print("分桶处理国家名称为：%s 的数据中...." % enable_nation)

        # 先分桶
        process_df = copy.deepcopy(raw_nation_df)  # 拷贝一份不会影响json汇总
        new_df = process_df.iloc[:, 1:].apply(lambda row: convert_value_to_bin(row), axis=0)
        new_df.to_excel(''.join([RESULT_PATH, enable_nation, '_processed', FILE_EXTEND]))

        # 再汇总json

        json_df = copy.deepcopy(raw_nation_df)
        json_df.apply(lambda x: x.fillna(x.mean(), inplace=True), axis=0)
        json_df = json_df.iloc[:, 1:].apply(lambda row: json_group(row, field_binname_binrange_dict), axis=0)

        print("分桶处理国家名称为：%s 的数据完毕...." % enable_nation)
        print("=================================")
        print("\n\n\n")

    # 保存json

    print("保存json中...")
    with open(''.join([RESULT_PATH, JSON_NAME]), "w") as f:
        f.write(json.dumps(nation_field_binname_binrange_dict, ensure_ascii=False, indent=4, separators=(',', ':')))
    print("保存json完毕.")
    print("finished!")

