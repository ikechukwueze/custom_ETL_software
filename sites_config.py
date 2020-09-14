


from common import *
from common import browseFile
#from openpyxl import load_workbook
#from handy_functions import cleanup, filter_items_from_dataframe

from format_excel_file import format_excel_file





class sites_config:
    def __init__(self):

        #antenna file to gain dictionary
        self.antenna_gain = {
            'default.pafx': [15, [0, 0, 0, 0, 1]],
            '80010669_GSM900.pafx': [15, [0, 0, 0, 0, 1]],
            '742214v01_1855_x_co_m45_00t.pafx': [17, [0, 0, 0, 0, 1]],

            'SEC36_1_900_65HBW_18dBi.pafx': [18, [0, 0, 0, 1, 0]],
            'SEC36_2_900_65HBW_21dBi.pafx': [21, [0, 0, 1, 0, 0]],
            'SEC36_4_900_65HBW_24dBi.pafx': [24, [0, 1, 0, 0, 0]],
            'SEC36_8_900_65HBW_27dBi.pafx': [27, [1, 0, 0, 0, 0]],
            'SEC36_1_900_V1.pafx': [21, [0, 0, 0, 1, 0]],
            'SEC36_2_900_V1.pafx': [24, [0, 0, 1, 0, 0]],
            'SEC36_4_900_V1.pafx': [27, [0, 1, 0, 0, 0]],
            'SEC36_8_900_V1.pafx': [30, [1, 0, 0, 0, 0]]
            }

        self.cols_map = {'Height (m)':'Height', 'Antenna Gain':'Antenna_gain', 'Azimuth':'Azimuth', 'Panel Config': 'Panel Config [8p, 4p, 2p, 1p, STD]'}


        #columns for new site_config dataframe
        self.site_config_col = ['Sites', 'Height', 'Panel Config [8p, 4p, 2p, 1p, STD]', 'No. of Panels', 'Antenna_gain', 'Azimuth']





    def compile_sites_config(self, input_file=None):

        #this allows for the method to 
		#be called with an optional input file
		#this is utilized in the combined_stats module where this
		#method is called on a sheet

        if input_file is None:
            
            input_file = browseFile('Select Sites config file')
            
            #check file extension and create dataframe
            if input_file.endswith('.csv'):
                self.sites_df = pd.read_csv(input_file)
            else:
                self.sites_df = pd.read_excel(input_file)
    

        else:
			#meaning a workbook sheet was passed as input file

			#read the data in the sheet
            data = input_file.values
            cols = next(data)
            rows = list(data)

			#convert the data into a dataframe
            self.sites_df = pd.DataFrame(rows, columns=cols)


        
        if input_file:

            #create new column with antenna gain
            self.sites_df['Antenna Gain'] = self.sites_df['Antenna File'].apply(lambda x: self.antenna_gain[x][0])

            #create new column with panel config
            self.sites_df['Panel Config'] = self.sites_df['Antenna File'].apply(lambda x: self.antenna_gain[x][1])

            #print(self.sites_df.head())
            
            #extract site id, convert to list, sort
            site_id_list = self.sites_df['Site ID'].tolist()
            site_id_list = list(set(site_id_list))
            site_id_list.sort()

            #columns for new site_config dataframe
            self.site_config = pd.DataFrame(columns=self.site_config_col)
            self.site_config['Sites'] = site_id_list
            self.site_config.set_index('Sites', inplace=True)


            #self.cols_map = {'Height (m)':'Height', 'Antenna Gain':'Antenna_gain', 'Azimuth':'Azimuth'}
            for col, value in self.cols_map.items():


                #group by site ID finds all unique site ID values
                #the applies a function e.g list to the corresponding rows
                #akin to how pivot table works e.g applies sum, average etc
                y = self.sites_df.groupby("Site ID")[col].apply(list).to_frame()


                if col == 'Panel Config':
                    #unpack the list of lists before zipping
                    y[col] = y[col].apply(lambda x: zip(*x))

                    #sum the values
                    y[col] = y[col].apply(lambda x: [sum(y) for y in x])

                else:
                
                    #change row values to string
                    y[col] = y[col].apply(str)
                    
                    #replace commas with slashes: "[12,13,14]" ==> "[12/13/14]"
                    y[col] = y[col].apply(lambda x: x.replace(", " , " / "))
                    
                    #slice string to remove square brackets 
                    y[col] = y[col].apply(lambda x: x[1:-1])
                
                #add the column to the site config table
                #the values of the cols_map dict correspond to headers in site_config
                self.site_config[value] = y[col]

            from operator import mul

            self.site_config['No. of Panels'] = self.site_config['Panel Config [8p, 4p, 2p, 1p, STD]']

            self.site_config['No. of Panels'] = self.site_config['No. of Panels'].apply(lambda x: zip(x, [8, 4, 2, 1, 1]))

            self.site_config['No. of Panels'] = self.site_config['No. of Panels'].apply(lambda x: sum(mul(*y) for y in x))


            return self.site_config

                



    def format_sites_config(self):
        
        output_dataframe = self.compile_sites_config()
        
        #save data to xlsx
        output_filename = easygui.filesavebox()
        
        #if output filename doesnt end with .xlsx, add the extenstion
        
        if not output_filename.endswith('.xlsx'):
            output_filename = output_filename + '.xlsx'
            
        output_dataframe.to_excel(output_filename, index = True)
        
        return format_excel_file(output_filename, use_comma=True)





