
from common import *
from handy_functions import bins
from handy_functions import tech_to_rssi_map, rssi_map
#from combined_statistics import group_prediction_stats

from format_barchart import format_barchart
from format_excel_file import format_excel_file


class dt_barchart:

    def __init__(self):
        pass



    def get_technology(self, combobox_var):
        #self.combobox_var = combobox_var
        #return self.combobox_var.get()
        pass
    


    def create_barchart(self, input_file=None, pdf=None, cdf=None, column_header=None, optional_bin_values=None):

        #print(technology_var)
        

        if input_file is None:

            get_input_file = browseFile()

            if get_input_file:
                if get_input_file.endswith('.xlsx'):
                    
                    chart_data = pd.read_excel(get_input_file)
                    
                else:
                    chart_data = pd.read_csv(get_input_file)
        
        else:
			#meaning a workbook sheet was passed as input file

			#read the data in the sheet
            #data = input_file.values
            #print(data)
            #cols = next(data)
            #print(cols)
            #rows = list(data)

            #convert the data into a dataframe
            #chart_data = pd.DataFrame(rows, columns=cols)
            chart_data = pd.DataFrame(input_file.values)
            h = chart_data.iloc[0]

            chart_data = chart_data[1:]
            chart_data.columns=h
            
            chart_data.reset_index(inplace=True)
            chart_data.drop('index', axis=1, inplace=True)
            
            self.useful_chart_data = chart_data.copy()


        
        if chart_data is not None:
            for val in tech_to_rssi_map.values():
                if val in chart_data.columns.tolist():
                    rssi = val
                    bin_column = rssi_map[rssi]
                    break
            
            #print(rssi)

            clean_chart_data = chart_data.copy()

            clean_chart_data = clean_chart_data[clean_chart_data[rssi] < 0]
            rssi_list = (-1 * clean_chart_data[rssi]).tolist()


            chart_bin = bins()

            clean_chart_data[bin_column] = chart_bin.make_bins_method(rssi_list, optional_bin_values)

            #gotten from the new ranges in bin
            self.new_bin_values = chart_bin.bin_values

            clean_chart_data = clean_chart_data[clean_chart_data[bin_column] != chart_bin.outside_bin]

            barchart_dataframe = pd.DataFrame(self.new_bin_values, columns=[bin_column])
            barchart_dataframe = barchart_dataframe.set_index(bin_column)


            if pdf:
                rssi_count_pdf = clean_chart_data.groupby(bin_column)[bin_column].count().to_frame()
                barchart_dataframe['PDF'] = rssi_count_pdf[bin_column]
                #print(barchart_dataframe)
                print('Done with PDF')

                rssi_count_pdf_age = clean_chart_data.groupby(bin_column)[bin_column].count().to_frame().apply(lambda x: x*100/sum(x))
                barchart_dataframe['%PDF'] = rssi_count_pdf_age[bin_column].round(1)
                

            if cdf:
                rssi_count_cdf = clean_chart_data.groupby(bin_column)[bin_column].count().cumsum().to_frame()
                barchart_dataframe['CDF'] = rssi_count_cdf[bin_column]
                print('Done with CDF')
                
                rssi_count_cdf_age = clean_chart_data.groupby(bin_column)[bin_column].count().cumsum().to_frame().apply(lambda x: x*100/max(x))
                barchart_dataframe['%CDF'] = rssi_count_cdf_age[bin_column].round(1)



            
            if column_header is not None:
                column_header = str(column_header) + ' '
                new_column_header = [column_header+i for i in barchart_dataframe.columns]

                barchart_dataframe.columns = new_column_header
            
            return barchart_dataframe


    
    def format_barchart(self, pdf=None, cdf=None):

        output_dataframe = self.create_barchart(pdf=pdf, cdf=cdf)
        
        output_filename = easygui.filesavebox()
        
        if not output_filename.endswith('.xlsx'):
            output_filename = output_filename + '.xlsx'
            
        output_dataframe.to_excel(output_filename, sheet_name='Bar Chart', index = True)
        
        format_barchart(output_filename)

        return format_excel_file(output_filename, use_comma=False)



            




        








