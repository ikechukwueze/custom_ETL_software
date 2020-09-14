

from common import *
from common import browseFile
from handy_functions import filter_items_from_dataframe, cleanup, bins

from format_excel_file import format_excel_file



class compute_pop_stats:

	def __init__(self):
		pass



	def compute_pop_stats(self, input_file=None, optional_ranges=None):

		#this allows for the method to 
		#be called with an optional input file
		if input_file is None:
			input_file = browseFile('Select Population stats file')

			self.pop_stats = input_file
			
			#check file extension and create dataframe
			if self.pop_stats.endswith('.csv'):
				self.pop_stats = pd.read_csv(self.pop_stats)
			else:
				self.pop_stats = pd.read_excel(self.pop_stats)
		else:
			#meaning a workbook sheet was passed as input file
			data = input_file.values 
			cols = next(data)
			rows = list(data)

			self.pop_stats = pd.DataFrame(rows, columns=cols)
		

		if input_file:
			


			#dictionary mapping column headers names to data type
			column_headers = {"<class 'str'>":'Sites', "<class 'numpy.float64'>":'Rssi'}

			#check the 2nd and 3rd columns in population dataframe, find out the data type
			#if 'str', header should be sectors; if 'float', header should be RSSI
			#as mapped in the dictionary
			a = type(self.pop_stats[self.pop_stats.columns[1]][2])
			a = str(a)
			b = type(self.pop_stats[self.pop_stats.columns[2]][2])
			b = str(b)

			
			#change column headers to dictionary mapping
			self.pop_stats.columns = ['Population', column_headers[a], column_headers[b]]


			#filter sectors of 'Off grid' and 'Null'
			self.pop_stats = filter_items_from_dataframe(self.pop_stats, ['Sites', 'Sites'], ["Off Grid", "Null"])


			#sort dataframe by sectors
			self.pop_stats = self.pop_stats.sort_values(by='Sites')
			
			
			#splice sectors column at the last underscore
			sectors_splice = [ row[:row.rfind("_")] for row in self.pop_stats['Sites'].tolist() ]


			#clean up sites to remove any other underscore
			sectors_splice = cleanup(sectors_splice)


			#replace sectors column with cleaned spliced values
			self.pop_stats['Sites'] = sectors_splice


			#multiply Rssi by -1 to make it positive 
			#(so that the pivot table can be in ascending order e.g from 75 to 105
			# instead of -105 to -75)
			self.pop_stats['Rssi'] = self.pop_stats['Rssi'] * -1
			

			#round up population values to whole numbers
			#self.pop_stats['Population'] = self.pop_stats['Population'].round(0)


			#instantiate bins class
			bin_object = bins()



			#add an additional column an group RSSI by bins
			self.pop_stats['Rssi_bins'] = bin_object.make_bins_method(self.pop_stats['Rssi'].tolist(), optional_ranges)


			## remove unwanted range
			#had to get variable - outside_bin - from make_bins function
			self.pop_stats = self.pop_stats[self.pop_stats['Rssi_bins'] != bin_object.outside_bin]
			

			#create pivot table, values == sum of population
			pop_stats_pivot = pd.pivot_table(self.pop_stats, index='Sites', columns='Rssi_bins', values='Population', fill_value=0, aggfunc='sum')

			
			#do a cumulative sum on the column values
			pop_stats_pivot = pop_stats_pivot.cumsum(axis=1)



			return pop_stats_pivot.round(0)






	def format_pop_stats(self):

		output_dataframe = self.compute_pop_stats()
		
		#add totals of each column
		output_dataframe.loc['Total']= output_dataframe.sum(numeric_only=True, axis=0)

		output_filename = easygui.filesavebox()
		
		if not output_filename.endswith('.xlsx'):
			output_filename = output_filename + '.xlsx'

		output_dataframe.to_excel(output_filename, index = True)

		return format_excel_file(output_filename, use_comma=True)
