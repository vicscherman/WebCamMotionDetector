from motion_detector import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

#converting our start and end times into strings and formatting them for later
df["Start_string"]= df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"]= df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")

# definining our column as a data source for our hover tooltip
cds=ColumnDataSource(df)

# formatting our output graph
p=figure(x_axis_type='datetime', height= 100, width =500, sizing_mode= 'scale_width',  title='Motion Events')
p.yaxis.minor_tick_line_color= None
p.yaxis.ticker.desired_num_ticks = 1
p.xaxis.axis_label = "Motion Detected"

#defining what our hover tool tip shows
hover= HoverTool(tooltips=[("Start", "@Start_string"), ("End", "@End_string")])
p.add_tools(hover)

#creating our rectangles on the graph for motion events
q=p.quad(left="Start", right="End", bottom=0, top=1, color = "blue", source= cds)

output_file("Motion.html")

show(p)