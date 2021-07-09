from datetime import date,datetime
import pandas as pd
import os.path
import time

src_file_path = r"D:\vscode_projects\python\attendance\atd_list.csv"
end_time=time.ctime(os.path.getctime(src_file_path))

today_date=date.today().strftime("%d/%m/%Y")

data = pd.read_csv(src_file_path,encoding='utf-16',delimiter='\t')

data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# joined_data=data.loc[data['User Action']=="Joined"]
# left_data=data.loc[data['User Action']=="Left"]
# # print(joined_data)
# # print(left_data)

# dic=data.to_dict()
# print(dic)

student_login_status={'Full Name':[],today_date:[],'temp':[],'state':[]}


for i in data['Timestamp']:
    
    name= data.loc[data['Timestamp']==i,"Full Name"]
    name = name.values[0]
    action = (data.loc[data['Timestamp']==i,"User Action"]).values[0]

    if name not in student_login_status['Full Name']:
        (student_login_status['Full Name']).append(name)
        (student_login_status[today_date]).append(0)
        (student_login_status['temp']).append(i)
        (student_login_status['state']).append('Joined')
        # print(name,(student_login_status['temp']))
    
    
    elif action=='Left':
        ind = (student_login_status['Full Name']).index(name)
        cur_time = (student_login_status['temp'])[ind]
        if type(cur_time) != int:
            # print(cur_time)
            stay_time = (i-cur_time).seconds
            (student_login_status[today_date])[ind]+=stay_time
            (student_login_status['temp'])[ind] = i
            (student_login_status['state'])[ind]="Left"
            # print(name,student_login_status['temp'])
            
    elif (name in student_login_status['Full Name']) and (action=="Joined") :
        
        ind = (student_login_status['Full Name']).index(name)
        (student_login_status['temp'])[ind]=i
        (student_login_status['state'])[ind]='Joined'
    # print((student_login_status))
        
    
for j in student_login_status['state']:
    if j=='Joined':
        ind=student_login_status['state'].index(j)
        cur_time=(student_login_status['temp'])[ind]
        end_time=pd.Timestamp(year = 2021,  month = 7, day = 7, 
                  hour = 12, minute=55, second = 24)
        stay_time=(end_time-cur_time).seconds
        (student_login_status[today_date])[ind]+=stay_time


out_data=pd.DataFrame(student_login_status)

print(out_data)

