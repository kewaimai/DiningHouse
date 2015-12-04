__author__ = '祥祥'


"""
如果已经读取完  就把下面的内容注释掉吧

"""


from DiningServer.service.meal_service import addMealByScript
from DiningServer.service.meal_service import addCategory
import xlrd


def startGenerator():
    # 这里是解析的data的路径及名称
    excel = xlrd.open_workbook('E:\\CompanyWork\\DiningRoom\\DiningHouse\\DiningServer\\data.xlsx')

    table = excel.sheet_by_index(0)

    nrows = table.nrows
    ncols = table.ncols

    category_name = ''
    category_id = ''
    category_order = 0

    for index in range(nrows):
        print(table.row_values(index))
        l = table.row_values(index)
        # 如果开始新的分类
        if l[0]:
            category_name = l[0]
            tbl_category = addCategory(category_name)
            category_id = tbl_category.id
            category_order = tbl_category.show_order
        addMealByScript(category_id,category_order,l[2])
