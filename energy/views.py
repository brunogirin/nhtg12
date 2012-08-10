# Create your views here.

from django.template import RequestContext, loader
from django.http import HttpResponse

import csv
import math

# internal methods
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

class DataSet(object):
    def __init__(self, dataReader):
        self.__items = {}
        i = 0
        for row in dataReader:
            if i in LINE_ITEM_DICT:
                self.__items[LINE_ITEM_DICT[i]] = DataItem(row)
            i = i + 1
    
    def suggest_items(self, params):
        suggestions = []
        for s, sr in INPUT_SUGG_DICT.items():
            if s in params and params[s] in sr:
                suggestions.extend(self.__items[k] for k in sr[params[s]])
        suggestions.extend([self.__items[k] for k in INPUT_SUGG_DICT['always']])
        return suggestions

# view methods
def index(request):
    t = loader.get_template('energy/index.html')
    c = RequestContext(request, {
    })
    return HttpResponse(t.render(c))

def result(request):
    dataReader = csv.reader(open('./energy/est-3-bed-semi-data.csv', 'rb'), delimiter=',', quotechar='"')
    dataSet = DataSet(dataReader)
    suggestions = dataSet.suggest_items(request.POST)
    # build the page
    t = loader.get_template('energy/result.html')
    c = RequestContext(request, {
        'suggestions': suggestions,
    })
    return HttpResponse(t.render(c))

