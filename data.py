import csv
import math

HEADER_ROW = """        <tr><th>Title</th><th>Savings per year</th>
    <th>Carbon reduction (kg/year)</th><th>CO2 reduction (kg/year)</th>
    <th>Average cost if intalled by a pro</th><th>Average cost if you install it yourself</th>
    <th>Number of years for the investment to pay back</th></tr>
"""

LINE_ITEM_DICT = {
    6:  'loft_full',
    7:  'loft_partial',
    8:  'cavity',
    9:  'solid_internal',
    10: 'solid_external',
    11: 'draught',
    12: 'floor',
    13: 'gaps',
    14: 'dglazing',
    15: 'dglazing_estr',
    16: 'sglazing',
    17: 'rad_installed',
    18: 'rad_diy',
    19: 'chimney',
    21: 'boiler_g',
    22: 'boiler_f',
    23: 'boiler_e',
    24: 'boiler_d',
    25: 'thermostat',
    26: 'trvs',
    28: 'tank_insulation',
    29: 'tank_thermostat',
    30: 'pipework',
    31: 'pipework_tank'
}

INPUT_SUGG_DICT = {
    'loft': {
        'no': [ 'loft_full' ],
        'yes100': [ 'loft_partial' ]
    },
    'walls': {
        'cavity': [ 'cavity' ],
        'solid': [ 'solid_internal', 'solid_external' ]
    },
    'dglazing': {
        'no': [ 'dglazing', 'dglazing_estr', 'sglazing' ]
    },
    'radiator': {
        'no': [ 'rad_installed', 'rad_diy' ]
    },
    'chimney': {
        'yes': [ 'chimney' ]
    },
    'boiler': {
        'G': [ 'boiler_g' ],
        'F': [ 'boiler_f' ],
        'E': [ 'boiler_e' ],
        'D': [ 'boiler_d' ]
    },
    'therm': {
        'no': [ 'thermostat' ]
    },
    'tank': {
        'yes': [ 'tank_insulation', 'tank_thermostat', 'pipework_tank' ],
        'no': [ 'pipework' ]
    },
    'always': [ 'draught', 'floor', 'gaps' ]
}

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
        self.__items = {}
        i = 0
        for row in dataReader:
            if i in LINE_ITEM_DICT:
                self.__items[LINE_ITEM_DICT[i]] = DataItem(row)
            i = i + 1
    
    def suggest_items(self, request):
        suggestions = []
        for f in request:
            fv = request[f][0]
            if fv in INPUT_SUGG_DICT[f]:
                suggestions.extend([self.__items[k] for k in INPUT_SUGG_DICT[f][fv]])
        suggestions.extend([self.__items[k] for k in INPUT_SUGG_DICT['always']])
        return suggestions

print """<html>
<head>
    <title>The data</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <link rel="stylesheet" type="text/css" href="main.css" />
</head>
<body>
    <h1>Suggestions for making your home more energy efficient</h1>
"""

dataReader = csv.reader(open('est-3-bed-semi-data.csv', 'rb'), delimiter=',', quotechar='"')
dataSet = DataSet(dataReader)
suggestions = dataSet.suggest_items(request)

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

