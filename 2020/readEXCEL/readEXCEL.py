import clr
clr.AddReferenceByName('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel

ex = Excel.ApplicationClass()   
ex.Visible = False
ex.DisplayAlerts = False

#open EXCEL file
wb = ex.Workbooks.Open('d:/demo/example.xlsx')

#get worksheet
ws=wb.Worksheets[1]

#read cell Text
total_score = 0
for i in [1, 2, 3, 4]:
    course=ws.Range['A'+str(i)].Text
    score=ws.Range['B'+str(i)].Text
    total_score += float(score)
    AddWarningMessage('{}: {}'.format(course, score))

AddWarningMessage('Total: {}'.format(total_score))