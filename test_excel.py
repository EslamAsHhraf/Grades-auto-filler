# Writing to an excel 
# sheet using Python
import xlwt
from xlwt import Workbook
  
# Workbook is created
wb = Workbook()
  
# add_sheet is used to create sheet.
answer_sheet = wb.add_sheet('Answer Sheet')
answer_sheet.write(0, 0, 'wite') 
  
wb.save('xlwt example.xls')