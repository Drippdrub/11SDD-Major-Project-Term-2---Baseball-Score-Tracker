import xlsxwriter as xl
import openpyxl as openpx

fileName = "xlTempTest"
xlfile = f"{fileName}.xlsx"
bsbTrack = xl.Workbook(xlfile)
playerScores = bsbTrack.add_worksheet()
bsbTrack.close()

table = openpx.load_workbook(xlfile)
sheet = table.active
sheet.title = "playerScores"
tableTemplate = [
    ["Home Team", "", "", "", "", "", "", "Away Team"],
    ["Player ID", "Player Name", "Runs", "Strikes", "Foul Balls", "Balls", "", "Player ID", "Player Name", "Runs", "Strikes", "Foul Balls", "Balls"],
    [1, "", "", "", "", "", "", 1],
    [2, "", "", "", "", "", "", 2],
    [3, "", "", "", "", "", "", 3],
    [4, "", "", "", "", "", "", 4],
    [5, "", "", "", "", "", "", 5],
    [6, "", "", "", "", "", "", 6],
    [7, "", "", "", "", "", "", 7],
    [8, "", "", "", "", "", "", 8],
    [9, "", "", "", "", "", "", 9],
    ["Team Total", "", "", "", "", "", "", "Team Total"],
]

for column in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]:
    sheet.column_dimensions[column].width = 15

for row in tableTemplate:
    sheet.append(row)
table.save(xlfile)