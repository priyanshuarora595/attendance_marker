from datetime import date,datetime
import pandas as pd
import os.path
import time
import numpy as np

src_file_path = str(input("please enter path of downloaded list."))

data = pd.read_csv(src_file_path,encoding='utf-16',delimiter='\t')

data['Timestamp'] = pd.to_datetime(data['Timestamp'])

today_date = str((((data['Timestamp'])[0]).date()).strftime("%d/%m/%Y"))


start_time = (data['Timestamp'])[0]

end_time  = start_time+ pd.to_timedelta(1, unit='h')

final_out_file_path = str(input("if you do not have an attendance list made by this software , please press enter otherwise  enter path of attendance list made by this software"))

student_login_status={'Full Name':[],today_date:[],'temp':[],'state':[]}


for i in data.index:
   
    name= data['Full Name'][i]
    if ' (Guest)' in name:
        name=name.replace(' (Guest)','')
    name = name.lower()
    action = data['User Action'][i]
    time_stamp = data['Timestamp'][i]
        
    if name not in student_login_status['Full Name']:
        (student_login_status['Full Name']).append(name)
        (student_login_status[today_date]).append(0)
        (student_login_status['temp']).append(time_stamp)
        (student_login_status['state']).append('Joined')
        
    
    
    elif ("Left" in action):
          
        ind = (student_login_status['Full Name']).index(name)
        cur_time = (student_login_status['temp'])[ind]
        stay_time = (time_stamp-cur_time).seconds
        (student_login_status[today_date])[ind]+=stay_time
        (student_login_status['temp'])[ind] = time_stamp
        (student_login_status['state'])[ind]="Left"
   
                        
    elif (name in student_login_status['Full Name']) and ("Joined" in action) :
        
        ind = (student_login_status['Full Name']).index(name)
        (student_login_status['temp'])[ind]=time_stamp
        (student_login_status['state'])[ind]='Joined'
   
    
for j in student_login_status['Full Name']:
    ind=(student_login_status['Full Name']).index(j)
  
    if (student_login_status['state'])[ind]=='Joined':
        cur_time=(student_login_status['temp'])[ind]
        
        stay_time=(end_time-cur_time).seconds
        (student_login_status[today_date])[ind]+=stay_time
        (student_login_status['state'])[ind]="Meeting over"
      
total_time=(end_time-start_time).seconds

for j in student_login_status['Full Name']:
    ind=(student_login_status['Full Name']).index(j)
    stay_time = (student_login_status[today_date])[ind]
    
    if (stay_time*100)/total_time >= 30.0 :
        (student_login_status[today_date])[ind] = "P"
    else:
        (student_login_status[today_date])[ind] = "A"
    
out_data=pd.DataFrame(student_login_status)
out_data=out_data.drop(columns=['state','temp'])
out_data=(out_data[1:]).sort_values(by='Full Name')



in_data=pd.read_csv(final_out_file_path)
in_data_dict = (in_data.to_dict()).keys()
for j in in_data_dict:
    if ("name" in j.lower()) and ('named' not in j.lower()):
        column_name=j



today_data = ["A"]*(len(in_data[column_name]))
out_data_dict = (out_data.to_dict())

out_data_dict_reverse = {v: k for k, v in (out_data_dict['Full Name']).items()}

in_data_dict = (in_data[column_name]).to_dict()

for key , value in in_data_dict.items():
    if value.lower() in (out_data_dict['Full Name']).values():
        ind = out_data_dict_reverse[value.lower()]
        
        today_data[key] = (out_data_dict[today_date])[ind]
in_data[today_date] = today_data

in_data.drop(in_data.columns[in_data.columns.str.contains('Unnamed')], axis=1, inplace=True)
in_data = in_data.set_index(column_name)


in_data.to_csv(final_out_file_path)