"""
从这个txt中提取数据。
可通过‘Sensitivity of’来作为每个Excel的名称
每个Excel的标题都是 Node、MutualInfo、Percent、Variance of Beliefs。共计四个

从Sensitivity of 往下数到第四行时，为数据行，用以提取数据。
一直读，读到空行时，认为Excel结束，可以阶段性保存。

空行是\n
re.findall('[a-zA-Z]+',aaa[75].rstrip()) 用来拼接
"""

import xlwt
import re


def is_number(s):
    try:    # 如果能运⾏ float(s) 语句，返回 True（字符串 s 是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError 为 Python 的⼀种标准异常，表⽰"传⼊⽆效的参数"
        pass  # 如果引发了 ValueError 这种异常，不做任何事情（pass：不做任何事情，⼀般⽤做占位语句）
    try:
        import unicodedata  # 处理 ASCII 码的包
        unicodedata.numeric(s)  # 把⼀个表⽰数字的字符串转换为浮点数返回的函数
        return True
    except (TypeError, ValueError):
        pass
        return False


if __name__ == '__main__':
    RAW_TXT = './data/tajikistanS1.5-7.txt'
    SAVE_EXCEL = './result/tajikistanS1.5-7.xls'


    # 0.创建一个 EXCEL 用于输出规整后的数据,以UTF-8编码来读写
    workbook = xlwt.Workbook(encoding='UTF-8')

    # 1.这个EXCEL创建一个工作表叫Regular,先写入标题行，如下所示。
    worksheet = workbook.add_sheet('Regular')
    worksheet.write(0,0,'Sensitivity') # 先y,后x
    worksheet.write(0,1,'Node')
    worksheet.write(0,2,'MutualInfo')
    worksheet.write(0,3,'Percent')
    worksheet.write(0,4,'Variance of Beliefs')

    # 2.定义一个行计数器，这个地方应该是从第一行开始（注意计算机里边通常认为0是第一位，所以这里的1是第二位）
    row_count = 1

    # 3.打开文件，因为这个文件是xx程序导出的，是GBK格式，所以我们也必须通过GBK打开，不然乱码。
    with open(RAW_TXT,encoding='GBK',mode='r') as raw_data:

        # 这里开始搞每个‘表格’
        while True:

            # 4.先找到‘表格’的开始位置，想办法搞到Sensitivity
            # 4.1 读取每一行数据
            excel_name_row_data = raw_data.readline()
            # 4.2 如果这行数据是以Save File As开头的，意味着这个文件已经到最后了，不要在搞了！
            if excel_name_row_data.startswith('Save File As'):
                break

            # 4.3 如果这行数据不是以Sensitivity of开头的，意味着此行数据无效。
            if not excel_name_row_data.startswith('Sensitivity of'):
                continue

            # 4.4 走到这里意味着，我们已经找到了‘表格’的开始位置，这里就开始搞Sensitivity了,也就是下面的这个excel_name
            excel_name = re.findall("'.*'", excel_name_row_data)[0].rstrip().replace("'", "").rstrip()

            # 4.5 忽略三行
            raw_data.readline()
            raw_data.readline()
            raw_data.readline()

            # 4.6 这里开始搞'表格'的每一条数据了！
            while True:

                info_single_row = raw_data.readline()
                # 4.7 如果这个数据行是\n开头，就意味着'表格'已经读完了，不要再搞了
                if info_single_row.startswith("\n"):
                    break

                # 4.8 走到这里，这个数据行还是有用滴，定义一个临时数组，用来装数据的
                info_collection = []

                # 4.9 搞到Node,塞到临时数组
                node = ' '.join(re.findall('[a-zA-Z]+', info_single_row.rstrip()))
                info_collection.append(node)

                # 4.10 搞到MutualInfo、Percent、Variance of Beliefs,塞到临时数组
                info_list = info_single_row.split(" ")
                for index,info in enumerate(info_list):
                    if is_number(info):
                        info_collection.append(float(info))

                # 4.11 这条数据都准备好了，那么我们就搞到工作表里边去，并且更新行计数器。
                worksheet.write(row_count,0,excel_name)
                worksheet.write(row_count,1,info_collection[0])
                worksheet.write(row_count,2,info_collection[1])
                worksheet.write(row_count,3,info_collection[2])
                worksheet.write(row_count,4,info_collection[3])
                row_count = row_count + 1

        # 所有的'表格'都写到了EXCEL里边，那我们最后落地保存一下就OJBK。
        workbook.save(SAVE_EXCEL)