import xlwt
import xlsxwriter
import openpyxl
from openpyxl.chart import LineChart, Reference


def read_number(line, i, end):
    nb = ""
    while line[i] != end:
        nb = nb + line[i]
        i = i + 1
    nb = float(nb)
    return nb


def reading_files(namefile):
    runs = []
    filin = open(namefile, "r")
    lignes = filin.readlines()
    r = []
    for ligne in lignes:
        if 'K' in ligne:
            r.append(read_number(ligne, ligne.index('=') + 2, '\t'))
            r.append(read_number(ligne, ligne.index(':') + 2, '\n'))

        if 'min' in ligne:
            r.append(read_number(ligne, ligne.index('\t') + 2, '\n'))
        if 'avg MSD' in ligne:
            r.append(read_number(ligne, ligne.index('\t') + 2, '\n'))
        if 'max' in ligne:
            r.append(read_number(ligne, ligne.index('\t') + 2, '\n'))
        if '__' in ligne:
            print(r)
            runs.append(r)
            r = []

    filin.close()
    return runs


def tab_MSD(sheet, cell_format, result, algo, start):
    i = 0
    for res in result:
        alg = algo[i]
        for j in range(0, 5):
            sheet.write_number(start + i, j, alg[j])
        for j in range(5, 8):
            sheet.write_number(start + i, j, res[j - 3])
        i = i + 1
    column = ['I', 'J', 'K', 'L']
    cell = ''
    formula = ''
    end = len(result) + start + 1
    for i in column:
        for j in range(start + 1, end + 1):
            if i == 'L':
                formula = '=AVERAGE({}{}:{}{})'.format('I', j, 'K', j)
                cell = "{}{}".format(i, j)
                sheet.write_formula(cell, formula, cell_format)
                continue
            if i == 'I':
                formula = '=C{}-F{}'.format(j, j)
                cell = "{}{}".format(i, j)
            if i == 'J':
                formula = '=D{}-G{}'.format(j, j)
                cell = "{}{}".format(i, j)
            if i == 'K':
                formula = '=E{}-H{}'.format(j, j)
                cell = "{}{}".format(i, j)
            if j == end:
                formula = '=AVERAGE({}{}:{}{})'.format(i, start + 1, i, end - 1)
                sheet.write_formula(cell, formula, cell_format)
                continue
            sheet.write_formula(cell, formula)


def create_MSD(sheet, workbook, result1, result2, Lloyd, PG):
    header1 = ['k', 'nb points', ' ', 'our Lloyd', ' ', ' ', 'article Lloyd', ' ', ' ', 'difference']
    header2 = ['k', 'nb points', ' ', 'our PG', ' ', ' ', 'article PG', ' ', ' ', 'difference']
    subheader = ['', '', 'min', 'avg', 'max', 'min', 'avg', 'max', 'min', 'avg', 'max', 'average of the difference']
    cell_format = workbook.add_format({'bold': True, 'bg_color': '#00FF00'})
    sheet.write_row(0, 0, header1)
    sheet.write_row(1, 0, subheader)
    sheet.write_row(len(result2) + 6, 0, header2)
    sheet.write_row(len(result1) + 7, 0, subheader)
    tab_MSD(sheet, cell_format, result1, Lloyd, 2)
    tab_MSD(sheet, cell_format, result2, PG, len(result1) + 8)


def create_graph_sheet(workbook, sheet, name, lloyd, pg):
    nbpts = [50, 100, 500, 1000, 5000, 10000]
    header = ['nb points', 'Lloyd', 'PG']
    sheet.write_row(0, 0, header)
    sheet.write_column(1, 0, nbpts)
    sheet.write_column(1, 1, lloyd)
    sheet.write_column(1, 2, pg)

    chart1 = workbook.add_chart({'type': 'line'})
    chart1.add_series({
        'name': [name, 0, 1],
        'categories': [name, 1, 0, 6, 0],
        'values': [name, 1, 1, 6, 1],
        'marker': {'type': 'diamond', 'size,': 5, 'border': {'color': 'red'}, 'fill': {'color': 'pink'}},
        'data_labels': {'value': True, 'position': 'above'}
    })

    chart1.add_series({
        'name': [name, 0, 2],
        'categories': [name, 1, 0, 6, 0],
        'values': [name, 1, 2, 6, 2],
        'marker': {'type': 'diamond', 'size,': 5, 'border': {'color': 'red'}, 'fill': {'color': 'pink'}},
        'data_labels': {'value': True}
    })

    chart1.set_title({'name': name})

    chart1.set_x_axis({'name': 'number of points'})

    chart1.set_y_axis({'name': 'time in seconds'})

    chart1.set_style(11)

    # add chart to the worksheet with given
    # offset values at the top-left corner of
    # a chart is anchored to cell D2 .
    sheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})


def create_excel(lloyd_times, pg_times):
    result1 = reading_files('resultat_article_Lloyd.txt')
    result2 = reading_files('resultat_article_PG.txt')
    lloydrun = reading_files('resultat_Lloyd.txt')
    pgrun = reading_files('resultat_PG.txt')
    workbook = xlsxwriter.Workbook('tabs.xls')
    sheets = ['MSD', 'time k=3', 'time k=4', 'time k=5', 'time k=10']
    i = 0
    for sheet in sheets:
        worksheet = workbook.add_worksheet(sheet)
        if sheet == 'MSD':
            create_MSD(worksheet, workbook, result1, result2, lloydrun, pgrun)
        else:
            create_graph_sheet(workbook, worksheet, sheet, lloyd_times[i], pg_times[i])
            i = i + 1

    workbook.close()
