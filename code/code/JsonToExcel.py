import json
import xlwt

if __name__ == '__main__':

    raw_json_file = './prcessed1.json'
    should_save_excel_file ='./prcessed1.xls'
    with open(raw_json_file,'r') as json1:
        content = json1.read()
        prcessed_dict = json.loads(content)

        book = xlwt.Workbook()  # 新建工作簿
        sheet1 = book.add_sheet('sheet1',
                               cell_overwrite_ok=True)  # 如果对同一单元格重复操作会发生overwrite Exception，cell_overwrite_ok为可覆盖

        sheet1.write(0,0,'Country')
        sheet1.write(0,1,'Factor')
        sheet1.write(0,2,'Class')
        sheet1.write(0,3,'Min')
        sheet1.write(0,4,'Max')

        count = 1
        for country in prcessed_dict.keys():
            factors_dict = prcessed_dict.get(country)
            for factor in factors_dict.keys():
                classes = factors_dict.get(factor)
                if not isinstance(classes,dict):
                    sheet1.write(count,0,country)
                    sheet1.write(count,1,factor)
                    count =count +1
                else:
                    for class_ in classes.keys():
                        value = classes.get(class_)
                        value = value[1:-2].split(',')
                        sheet1.write(count, 0, country)
                        sheet1.write(count, 1, factor)
                        sheet1.write(count, 2, class_)
                        sheet1.write(count, 3, float(value[0]))
                        sheet1.write(count, 4, float(value[1]))
                        count = count + 1
        book.save(filename_or_stream=should_save_excel_file)  # 一定要保存