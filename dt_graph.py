
from common import *

from handy_functions import tech_to_rssi_map
from handy_functions import rssi_map
from handy_functions import addDummyValues
from handy_functions import modifiedMovingAverage

import math, statistics, re

from format_graph import format_graph
from format_excel_file import format_excel_file




class dt_graph:

    def __init__(self):
        pass

    


    def create_graph(self, input_file=None, data_from_barchart=None, column_header=None):
        

        if input_file is None:

            get_input_file = browseFile()

            if get_input_file:
                if get_input_file.endswith('.xlsx'):
                    
                    chart_data = pd.read_excel(get_input_file)
                    print(chart_data.head())
                else:
                    chart_data = pd.read_csv(get_input_file)
        
        elif data_from_barchart is not None:
            chart_data = data_from_barchart
        
        else:
			
            #meaning a workbook sheet was passed as input file

			#read the data in the sheet
            data = input_file.values
            #print(data)
            cols = next(data)
            rows = list(data)
            #print(rows)

            #convert the data into a dataframe
            chart_data = pd.DataFrame(rows, columns=cols)
            


        
        if chart_data is not None:
            for val in tech_to_rssi_map.values():
                if val in chart_data.columns.tolist():
                    rssi = val
                    rssi_header = rssi_map[rssi]
                    break


            clean_chart_data = chart_data.copy()

            clean_chart_data = clean_chart_data[clean_chart_data[rssi] < 0]

            clean_chart_data['Rssi_in_watts'] = (10**((clean_chart_data[rssi])/10.0))/1000.0

            longitude_column = latitude_column = None
            pattern_long = re.compile('longitude' + r'.*')
            pattern_lat = re.compile('latitude' + r'.*')

            for column in clean_chart_data.columns.tolist():

                if pattern_long.findall(column.lower()):
                    longitude_column = column

                elif pattern_lat.findall(column.lower()):
                    latitude_column = column
 
                elif longitude_column and latitude_column:
                    break
                
                #else:
                #    print('No longitude or latitude columns found.')
                #    return

            clean_chart_data.rename(columns = {longitude_column:'Longitude_radians', latitude_column:'Latitude_radians'}, inplace=True)


            clean_chart_data['Longitude_radians'] = clean_chart_data['Longitude_radians'].apply(lambda x: math.radians(x))
            clean_chart_data['Latitude_radians'] = clean_chart_data['Latitude_radians'].apply(lambda x: math.radians(x))

            lon = clean_chart_data['Longitude_radians'].tolist()
            lat = clean_chart_data['Latitude_radians'].tolist()
            distance = [0.00]

            start_lon = lon[0]
            start_lat = lat[0]

            for i in range(1, len(lon)):
                dlon = lon[i] - start_lon
                dlat = lat[i] - start_lat
                
                a = math.sin(dlat / 2)**2 + math.cos(start_lat) * math.cos(lat[i]) * math.sin(dlon / 2)**2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                distance.append(c*6373)

            clean_chart_data['Distance'] = distance

            clean_chart_data.sort_values(by=['Distance'], inplace=True)

            distanceList = clean_chart_data['Distance'].tolist()
            rssiList = clean_chart_data['Rssi_in_watts'].tolist()

            
            
            
            dist_rssi_data = addDummyValues(distanceList, rssiList)

            plot_data = pd.DataFrame(dist_rssi_data, columns=['Distance', 'Rssi_Watts'])

            plot_data = plot_data.groupby('Distance')['Rssi_Watts'].apply(lambda x: statistics.median(x)).to_frame()

            rssi_watts_50 = modifiedMovingAverage(plot_data['Rssi_Watts'].tolist(), 51)
            rssi_watts_100 = modifiedMovingAverage(plot_data['Rssi_Watts'].tolist(), 101)

            plot_data[rssi_header + '_dBm'] = 10 * np.log10(plot_data['Rssi_Watts']) + 30

            rssi_header_50 = rssi_header + '_dBm_50'
            rssi_header_100 = rssi_header + '_dBm_100'

            plot_data[rssi_header_50] = rssi_watts_50
            plot_data[rssi_header_100] = rssi_watts_100

            plot_data[rssi_header_50] = 10 * np.log10(plot_data[rssi_header_50]) + 30
            plot_data[rssi_header_100] = 10 * np.log10(plot_data[rssi_header_100]) + 30

            plot_data.drop('Rssi_Watts', axis=1, inplace=True)

            if column_header is not None:
                column_header = str(column_header) + ' '
                new_column_header = [column_header+i for i in plot_data.columns]

                plot_data.columns = new_column_header

            plot_data.reset_index(inplace=True)
            print('Done with Graph')
            
            return plot_data



    def format_graph(self):

        output_dataframe = self.create_graph()
        
        output_filename = easygui.filesavebox()
        
        if not output_filename.endswith('.xlsx'):
            output_filename = output_filename + '.xlsx'
            
        output_dataframe.to_excel(output_filename, sheet_name = 'Graph', index = True)
        
        format_graph(output_filename)

        return format_excel_file(output_filename, use_comma=False)