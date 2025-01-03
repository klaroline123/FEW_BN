import csv
import pandas as pd



if __name__ == '__main__':

    file_name = 'food_FAO' # 这个是文件名称不要带后缀的，而且需要放到data目录下

    raw_df = pd.read_csv('../data/'+file_name+'.csv', header=0)
    year_set_series = raw_df['Year'].unique().tolist() # 获取年份集合
    year_set_set = set(sorted(year_set_series,reverse=False)) # 处理成升序排列，即从小到大
    raw_dict_collection={}
    clean_columns = ['Element','Item','Unit']
    clean_columns.extend(list(year_set_set))
    with open('../data/'+file_name+'.csv',encoding='utf-8',mode='r') as f :
        csv_reader = csv.reader(f)
        next(csv_reader)
        for row in csv_reader:
            if row:
                element = row[5]
                item = row[7]
                unit = row[10]
                year = int(row[9])
                value = float(row[11])
                key  = '&'.join([element,item,unit])

                # 如果没有这个id,那么就创建一个子字典
                if not key in raw_dict_collection.keys():
                    raw_dict_collection[key]={}

                raw_dict_collection[key][year]=value

        # 遍历raw_dict_collection
        for collect_key,collect_value in raw_dict_collection.items():
            c_key_set = set(collect_value.keys())
            minus_set = year_set_set - c_key_set # 求差集年份
            if minus_set:
                for minus_year in minus_set:
                    collect_value[minus_year]=None # 差年补空

        # 写到另外一个文件里边去
        with open('../data/'+file_name+'_clean'+'.csv',mode='w',encoding='utf-8',newline='') as f2:
            csv_writer = csv.writer(f2)
            csv_writer.writerow(clean_columns)
            for collect_key, collect_value in raw_dict_collection.items():
                begin_list = collect_key.split('&')
                for single_year in year_set_set:
                    begin_list.append(collect_value[single_year])
                csv_writer.writerow(begin_list)




    print('finished!')
