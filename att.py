from datetime import date,datetime
import pandas as pd
import os.path
import time

src_file_path = r"D:\vscode_projects\python\attendance\meetingAttendanceList.csv"

today_date=date.today().strftime("%d/%m/%Y")

end_time=pd.Timestamp(year = 2020,  month = 10, day = 27, hour = 13, minute=00, second = 00)
data = pd.read_csv(src_file_path,encoding='utf-16',delimiter='\t')

data['Timestamp'] = pd.to_datetime(data['Timestamp'])


student_login_status={'Full Name':[],today_date:[],'temp':[],'state':[]}

start_time=0

for i in data.index:
   
    name= data['Full Name'][i]
    action = data['User Action'][i]
    time_stamp = data['Timestamp'][i]
    if i==0:
        start_time=time_stamp
        
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
      

out_data=pd.DataFrame(student_login_status)


out_data=out_data.drop(columns=['state','temp'])

total_time=(end_time-start_time).seconds



out_data=pd.DataFrame(student_login_status)

out_data['status'] = ["P" if (((student_login_status[today_date])[j])*100)/total_time > 50.0 else "A" for j in range(len(student_login_status[today_date]))]
        

out_data=out_data.drop(columns=['state','temp'])
print(out_data)
out_data.to_csv(r"D:\vscode_projects\python\attendance\general.csv")
