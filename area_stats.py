


from common import *
from common import browseFile
from openpyxl import load_workbook
from handy_functions import cleanup, filter_items_from_dataframe

from format_excel_file import format_excel_file




class compute_area_stats:

	def __init__(self):
		#self.area_stats = area_stats
		pass


	def compute_area_stats(self, input_file=None):

		#this allows for the method to 
		#be called with an optional input file
		#this is utilized in the combined_stats module where this
		#method is called on a sheet

		#if input file is None, then request for a workbook
		if input_file is None:

			input_file = browseFile('Select Area stats file')
			self.area_stats = input_file

			#check file extension and create dataframe
			if self.area_stats.endswith('.csv'):
				self.area_stats = pd.read_csv(self.area_stats)
			else:
				self.area_stats = pd.read_excel(self.area_stats)
		
		else:
			#meaning a workbook sheet was passed as input file

			#read the data in the sheet
			data = input_file.values 
			cols = next(data)
			rows = list(data)

			#convert the data into a dataframe
			self.area_stats = pd.DataFrame(rows, columns=cols)
			


		if input_file:
			#print(self.area_stats.head())
			#change column headers 
			self.area_stats.columns = ['Sites', 'Ranges', 'Area_kmsq']

			
			#splice sites column at the last underscore
			sites_splice = [ row[:row.rfind("_")] if row != "No clutter" else row for row in self.area_stats['Sites'].tolist() ]

			
			#clean up sites to remove any other underscore 
			sites_splice_cleaned = cleanup(sites_splice)

			
			#splice ranges column at the ' ~' and remove the '-' at the start of each value
			ranges_splice = [ int(row[1:row.find(" ~")]) if " ~" in row else row for row in self.area_stats['Ranges'].tolist() ]


			
			#replace sites and ranges column with cleaned spliced values
			self.area_stats['Sites'] = sites_splice_cleaned
			self.area_stats['Ranges'] = ranges_splice

			
			#filter sites and ranges columns of 'No clutter', 'outside range', 200
			self.area_stats = filter_items_from_dataframe(self.area_stats, ['Sites', 'Ranges', 'Ranges'], ["No clutter", "Outside range", 200])


			#get unique range to use elsewhere
			area_ranges_list = self.area_stats['Ranges'].tolist()
			self.area_ranges = list(set(area_ranges_list))
			self.area_ranges.sort()

			
			#create pivot table, values == sum of area
			self.area_stats_pivot = pd.pivot_table(self.area_stats, index='Sites', columns='Ranges', values='Area_kmsq', aggfunc='sum')

			
			#do a cumulative sum on the column values
			self.area_stats_pivot = self.area_stats_pivot.cumsum(axis=1)

			#round up the values in the dataframe
			return self.area_stats_pivot.round(0)





	def format_area_stats(self):

		output_dataframe = self.compute_area_stats()
		
		#add totals of each column
		output_dataframe.loc['Total']= output_dataframe.sum(numeric_only=True, axis=0)

		#save data to xlsx
		output_filename = easygui.filesavebox()

		#if output filename doesnt end with .xlsx, add the extenstion
		if not output_filename.endswith('.xlsx'):
			output_filename = output_filename + '.xlsx'

		output_dataframe.to_excel(output_filename, index = True)

		return format_excel_file(output_filename, use_comma=True)