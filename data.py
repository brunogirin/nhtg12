import csv
import math

HEADER_ROW = """        <tr><th>Title</th><th>Savings per year</th>
    <th>Carbon reduction (kg/year)</th><th>CO2 reduction (kg/year)</th>
    <th>Average cost if intalled by a pro</th><th>Average cost if you install it yourself</th>
    <th>Number of years for the investment to pay back</th></tr>
"""

class DataItem(object):
    def __init__(self, row):
        self.title = row[1]
        self.kwh_yr = row[2]
        self.price_yr = row[3]
        self.saving_min = self.convert(row[6])
        self.saving_max = self.convert(row[8])
        self.kgc_yr = self.convert(row[10])
        self.kgco2_yr = self.convert(row[11])
        self.cost_pro = row[14]
        self.payback_min = self.convert(row[15])
        self.payback_max = self.convert(row[16])
        self.cost_diy = row[18]
    
    def convert(self, val):
        try:
            return int(math.ceil(float(val)))
        except ValueError:
            return val
    
    def table_row(self):
        return "<tr>{0}</tr>".format(self.table_cells())
        
    def table_cells(self):
        return "<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td><td>{6}</td>".format(
            self.title, self.format_range(self.saving_min, self.saving_max),
            self.kgc_yr, self.kgco2_yr, self.cost_pro, self.cost_diy,
            self.format_range(self.payback_min, self.payback_max)
        )
    
    def format_range(self, min_val, max_val):
        if min_val == "" and max_val == "":
            return ""
        elif max_val == "":
            return min_val
        else:
            return "{0} to {1}".format(min_val, max_val)

class DataSet(object):
    def __init__(self, dataReader):
        i = 0
        for row in dataReader:
            if i == 6:
                self.loft_full = DataItem(row)
            elif i == 7:
                self.loft_partial = DataItem(row)
            elif i == 8:
                self.cavity = DataItem(row)
            elif i == 9:
                self.solid_internal = DataItem(row)
            elif i == 10:
                self.solid_external = DataItem(row)
            elif i == 11:
                self.draught = DataItem(row)
            elif i == 12:
                self.floor = DataItem(row)
            elif i == 13:
                self.gaps = DataItem(row)
            elif i == 14:
                self.dglazing = DataItem(row)
            elif i == 15:
                self.dglazing_estr = DataItem(row)
            elif i == 16:
                self.sglazing = DataItem(row)
            elif i == 17:
                self.rad_installed = DataItem(row)
            elif i == 18:
                self.rad_diy = DataItem(row)
            elif i == 19:
                self.chimney = DataItem(row)
            elif i == 21:
                self.boiler_g = DataItem(row)
            elif i == 22:
                self.boiler_f = DataItem(row)
            elif i == 23:
                self.boiler_e = DataItem(row)
            elif i == 24:
                self.boiler_d = DataItem(row)
            elif i == 25:
                self.thermostat = DataItem(row)
            elif i == 26:
                self.trvs = DataItem(row)
            elif i == 28:
                self.tank_insulation = DataItem(row)
            elif i == 29:
                self.tank_thermostat = DataItem(row)
            elif i == 30:
                self.pipework = DataItem(row)
            elif i == 31:
                self.pipework_tank = DataItem(row)
            i = i + 1
    
    def suggest_items(self, formInput):
        items = []
        if formInput.loft == "no":
            items.append(self.loft_full)
        elif formInput.loft == "yes100":
            items.append(self.loft_partial)
        if formInput.walls == "cavity":
            items.append(self.cavity)
        elif formInput.walls == "solid":
            items.append(self.solid_internal)
            items.append(self.solid_external)
        items.append(self.draught)
        items.append(self.floor)
        items.append(self.gaps)
        if formInput.dglazing == "no":
            items.append(self.dglazing)
            items.append(self.dglazing_estr)
            items.append(self.sglazing)
        if formInput.radiator == "no":
            items.append(self.rad_installed)
            items.append(self.rad_diy)
        if formInput.chimney == "yes":
            items.append(self.chimney)
        if formInput.boiler == "G":
            items.append(self.boiler_g)
        elif formInput.boiler == "F":
            items.append(self.boiler_f)
        elif formInput.boiler == "E":
            items.append(self.boiler_e)
        elif formInput.boiler == "D":
            items.append(self.boiler_d)
        if formInput.therm == "no":
            items.append(self.thermostat)
        if formInput.tank == "yes":
            items.append(self.tank_insulation)
            items.append(self.tank_thermostat)
            items.append(self.pipework_tank)
        else:
            items.append(self.pipework)
        return items

class FormInput(object):
    def __init__(self, request):
        self.loft = self.get_field('loft', request)
        self.walls = self.get_field('walls', request)
        self.dglazing = self.get_field('dglazing', request)
        self.radiator = self.get_field('radiator', request)
        self.chimney = self.get_field('chimney', request)
        self.boiler = self.get_field('boiler', request)
        self.therm = self.get_field('therm', request)
        self.tank = self.get_field('tank', request)
    
    def get_field(self, field, request):
        if field in request:
            return request[field][0]
        else:
            return ""

print """<html>
<head>
    <title>The data</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>
    <h1>Suggestions for making your home more energy efficient</h1>
"""

dataReader = csv.reader(open('est-3-bed-semi-data.csv', 'rb'), delimiter=',', quotechar='"')
dataSet = DataSet(dataReader)
formInput = FormInput(request)
suggestions = dataSet.suggest_items(formInput)

if len(suggestions) == 0:
    print """<p>Unfortunately, based on your input, we have found no suggestions for you.</p>
    """
else:
    print """
    <p>Based on your input, here is a list of things you could do to improve your
    home's energy efficiency:</p>
    <table>{0}
    """.format(HEADER_ROW)
    for row in suggestions:
        print row.table_row()
    print """    </table>"""

print """
    <p><a href="./index.html">Start again</a></p>
    <p>Data supplied by the <a href="http://www.energysavingtrust.org.uk/">Energy Saving Trust</a>.</p>
</body>
</html>"""

