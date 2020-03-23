from flask import Flask,render_template, redirect, url_for, request
# from flask_uploads import UploadSet, configure_uploads, IMAGES
#from flask.ext.images import resized_img_src
import os
import pandas as pd
from sklearn import preprocessing
import h2o as h
import numpy as np
import seaborn as sns
h.init(port=8000)
from h2o.estimators.gbm import H2OGradientBoostingEstimator
from h2o.estimators.random_forest import H2ORandomForestEstimator
def smart_fav_processing(service_usage,hard_key_usage):

	df=service_usage
	df3=hard_key_usage
	df=df[df.bench_mode==False]
	df3=df3[df3.bench_mode==False]

	df_clean=df[['anonymized_id','date','driver_type','make','model','serial','service_category','service_name','total_duration','total_launches']]
	#df4_clean=df4[['anonymized_id','date','driver_type','make','model','serial','time_active']]
	df3_clean=df3[['anonymized_id','date','driver_type','make','model','serial','hard_key_name','hard_key_source','total_key_presses']]


	temp=pd.merge(df_clean,df3_clean, how='left',on=['anonymized_id','date','driver_type','make','model','serial'])

	# (temp.isnull().sum())
	# len(temp.serial.unique())

	dff=temp.dropna(subset=['make'])

	dfb=dff

	dfb=pd.concat([dfb,pd.get_dummies(dfb.driver_type),pd.get_dummies(dfb.hard_key_source)],axis=1)

	#Milliseconds to seconds
	dfb['total_duration']=dfb['total_duration']*.001

	####Label Encoder
	le = preprocessing.LabelEncoder()
	le.fit(dfb['model'])
	dfb['model']=le.transform(dfb['model'])
	le.fit(dfb['make'])
	dfb['make']=le.transform(dfb['make'])
	dfb['total_key_presses']=dfb['total_key_presses'].fillna(0)
	## Macth columns with the training Data
	list_of_col=('anonymized_id', 'date', 'driver_type', 'make', 'model', 'serial',
	   'service_category', 'service_name', 'total_duration',
	   'total_launches', 'hard_key_name', 'hard_key_source',
	   'total_key_presses', 'Commuter', 'ErrandRunnder', 'GarageOrnament',
	   'Other', 'Weekender', 'faceplate', 'frontHBC', 'hu', 'ics',
	   'rearPC', 'swc')
	missing_cols = set(list_of_col) - set(dfb.columns)
	# Add a missing column in test set with default value equal to 0
	for i in missing_cols:
			dfb[i]=0

	# Ensure the order of column in the test set is in the same order than in train set
		#dfb = dfb[train.columns]
	return h.H2OFrame(dfb)
#app = Flask (__name__,template_folder='templates')
app = Flask (__name__,template_folder='static')
#@app.route('/hello', methods=['GET', 'POST'])
@app.route('/')
def index():
	# df=pd.read_csv("D:/AI/AI_Hub/Head Unit Data/data/vw_service_usage_test.txt",sep='\\t',engine='python')
	# df3=pd.read_csv("D:/AI/AI_Hub/Head Unit Data/data/vw_hard_key_usage.txt",sep='\\t',engine='python')
	# model = h.load_model('D:/AI/AI_Hub/Head Unit Data/rf_covType_v1')
	# test= smart_fav_processing(df,df3)
	# predictions = model.predict(test[:-7])
	# pred_df= predictions.as_data_frame()
	# sort_pred = np.argsort(pred_df.iloc[0:,1:8], axis=1)
	# top3=[(sort_pred.columns[(sort_pred == 0).iloc[0]])[0],(sort_pred.columns[(sort_pred == 1).iloc[0]])[0],(sort_pred.columns[(sort_pred == 2).iloc[0]])[0]]
	# for i in range(0,len(top3)):
	# 	if top3[i]=='sat':
	# 		top3[i]='Satellite Radio'
	# 	if top3[i]=='fm':
	# 		top3[i]='FM Radio'
	# 	if top3[i]=='usb1':
	# 		top3[i]='USB Device'
	#return render_template('new.html',output=top3[2])
	return render_template('packages.html')

# @app.route('/index', methods=['GET', 'POST'])
# def show_index():
#     return render_template("new.html")
df=pd.read_csv("D:/AI/AI_Hub/Head Unit Data/data/vw_service_usage_test.txt",sep='\\t',engine='python')
df3=pd.read_csv("D:/AI/AI_Hub/Head Unit Data/data/vw_hard_key_usage_test.txt",sep='\\t',engine='python')
def readFiles():
	service_usage=pd.read_csv("D:/AI/AI_Hub/Head Unit Data/data/vw_service_usage_test.txt",sep='\\t',engine='python')
	hard_key_usage=pd.read_csv("D:/AI/AI_Hub/Head Unit Data/data/vw_hard_key_usage.txt",sep='\\t',engine='python')
	return
	# return service_usage.to_html(), hard_key_usage.to_html()

@app.route('/home/')
def data():
	return render_template('new.html')

# @app.route('/home/Data_List/')
# def data():
# 	# ---- view data sources ---
# 	return 'a'
@app.route('/home/Work_Packages/')
def packages():

	return render_template('packages.html')

@app.route('/home/my-link/')
def my_link():
    service_usage=pd.read_csv("D:/AI/AI_Hub/Head Unit Data/data/vw_service_usage_test.txt",sep='\\t',engine='python')
    hard_key_usage=pd.read_csv("D:/AI/AI_Hub/Head Unit Data/data/vw_hard_key_usage_test.txt",sep='\\t',engine='python')
    return  render_template('view_data_read.html',tables=[service_usage.to_html(), hard_key_usage.to_html()],
    titles = [ 'na','service_usage', 'hard_key_usage']) 
# def my_link():
# 	service_usage,hard_key_usage= readFiles()
#     	return  service_usage.to_html()

# def my_link():
#   	df=pd.read_csv("D:/AI/AI_Hub/Head Unit Data/data/vw_service_usage_test.txt",sep='\\t',engine='python')
# 	df3=pd.read_csv("D:/AI/AI_Hub/Head Unit Data/data/vw_hard_key_usage.txt",sep='\\t',engine='python')
# 	#model = h.load_model('D:/AI/AI_Hub/Head Unit Data/rf_covType_v1')
# 	# test= smart_fav_processing(df,df3)

# 	# predictions = model.predict(test[:-7])
# 	# pred_df= predictions.as_data_frame()
# 	# sort_pred = np.argsort(pred_df.iloc[0:,1:8], axis=1)
# 	# top3=[(sort_pred.columns[(sort_pred == 0).iloc[0]])[0],(sort_pred.columns[(sort_pred == 1).iloc[0]])[0],(sort_pred.columns[(sort_pred == 2).iloc[0]])[0]]
# 	# for i in range(0,len(top3)):
# 	# 	if top3[i]=='sat':
# 	# 		top3[i]='Satellite Radio'
# 	# 	if top3[i]=='fm':
# 	# 		top3[i]='FM Radio'
# 	# 	if top3[i]=='usb1':
# 	# 		top3[i]='USB Device'
# 	return df.head(n=3), df3.head(n=3)
@app.route('/home/my-link2/')
def my_link2():
	test= (smart_fav_processing(df,df3)).as_data_frame()
	test=test[['make','model','total_launches','total_duration', 'total_key_presses', 'Commuter', 'ErrandRunnder', 'GarageOrnament',
       'Other', 'Weekender', 'faceplate', 'frontHBC', 'hu','ics','rearPC', 'swc']]
	return render_template('view.html',tables=[test.to_html()],
    titles = ['na','Feature Engineered Data',])
	#return ( test.to_html())

@app.route('/home/link3/')
def link3():
	model = h.load_model('D:/AI/AI_Hub/Head Unit Data/rf_covType_v1')
	test= smart_fav_processing(df,df3)

	predictions = model.predict(test[:-7])
	pred_df= predictions.as_data_frame()
	sort_pred = np.argsort(pred_df.iloc[0:,1:8], axis=1)
	top3=[(sort_pred.columns[(sort_pred == 0).iloc[0]])[0],(sort_pred.columns[(sort_pred == 1).iloc[0]])[0],(sort_pred.columns[(sort_pred == 2).iloc[0]])[0]]
	for i in range(0,len(top3)):
		if top3[i]=='sat':
			top3[i]='Satellite Radio'
		if top3[i]=='fm':
			top3[i]='FM Radio'
		if top3[i]=='usb1':
			top3[i]='USB Device'
	return render_template('pred.html', your_list=[top3[0], top3[1], top3[2]])

@app.route('/home/link4/')
def plot():
	model = h.load_model('D:/AI/AI_Hub/Head Unit Data/rf_covType_v1')
	var_im=(model.varimp(1))
	var_im=var_im[:5]
	sns_plot=sns.barplot(x=var_im.variable, y=var_im.percentage,palette="Blues_d")
	sns_plot.set_xticklabels(sns_plot.get_xticklabels(), rotation = 15, fontsize = 8)
	sns_plot.set(xlabel='Features', ylabel='Variable Importance')
	fig = sns_plot.get_figure()
	fig.savefig("D:/AI/static/plot.jpg")
	return render_template('plot.html') 
if __name__ == "__main__":
	app.run(port=8080)


######SPYRE

# from spyre import server
# import pandas as pd
# import h2o as h

# class UserUploadApp(server.App):

#     title = "Custom File Upload Example"
#     results = [{
#         "type": "text",
#         "key": "words",
#         "label": "prediction",
#         "value": '',
#         "action_id": "simple_html_output"
#     }]

#     controls = [{
#         "type": "upload",
#         "id": "ubutton",

#     }, 
#     {
#         "type": "button",
#         "label": "Upload1",
#         "id": "update_data1"
#     },
#         {"type": "upload",
#         "id": "ubutton"
#         },
#       {
#         "type": "button",
#         "label": "Upload2",
#         "id": "update_data2"
#     }]

#     tabs = ["Text", "Table1", "Table2","Plot"]

#     outputs = [{
#         "type": "plot",
#         "id": "plot",
#         "control_id": "update_data",
#         "tab": "Plot",
#         "on_page_load": True
#     }, {
#         "type": "table",
#         "id": "table_id",
#         "control_id": "update_data1",
#         "tab": "Table1",
#         "on_page_load": True
#     }, {
#         "type": "table",
#         "id": "table_id2",
#         "control_id": "update_data2",
#         "tab": "Table2",
#         "on_page_load": True
#     }, {
#         "type": "html",
#         "id": "html2",
#        #"control_id": "update_data",
#         "tab": "Text"
#     }]

#     def __init__(self):
#         self.upload_data = None
#         self.upload_file = None

#     def html1(self, params):
#         text = (
#             "Upload a CSV and press refresh. There's a sample csv in "
#             "the examples directory that you could try."
#         )
#         if self.upload_data is not None:
#             text = self.upload_data
#         return text
#     def html2(self,params):
		
#     	text = (
			
#             "df.columns[1]"
#         )
#         if self.upload_data is not None:
#             text = self.upload_data
#         return text

#     def storeUpload(self, file):
#         self.upload_file = file
#         self.upload_data = file.read()
#         #self.update_data2 = file.read()

	
#     def getData(self, params):
#         df = None
#         #h.init(strict_version_check = False)
# 		#model=h.load_model('D:/AI/AI_Hub/Head Unit Data/rf_covType_v1')
#         #df3=None
#         if self.upload_file is not None:
#             self.upload_file.seek(0)
#             df = pd.read_csv(self.upload_file,sep='\\t',engine='python')

#             #df3 = pd.read_csv(self.upload_file,sep='\\t',engine='python')
#         return df.driver_type.value_counts()
#         return df
#     def modell(df):
#     	df = pd.read_csv(self.upload_file,sep='\\t',engine='python')
#     	return df.columns[1]
# if __name__ == '__main__':
#     app = UserUploadApp()
#     app.launch()