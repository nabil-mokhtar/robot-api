import requests,json
from datetime import datetime


BASE="http://127.0.0.1:5000/"


# Add New Mission
#mission = {'start_time':str(datetime.now().replace(second=0, microsecond=0)), "#tasks": "2","tasks":[{'id':'1','taskname':'bring form pharmacy','param':[{'arg1':'congistal','arg2':'panadol'},{'patient':'2'}] }] }
mission = {'start_time':str(datetime.now().replace(second=0, microsecond=0)), "#tasks": "2","tasks":[{'id':'1','taskname':'bring form pharmacy','param':[{'arg1':'congistal'},{}] }] }


# mission = {"id": "1",'start_time':'',
#  "#tasks": "2",
# "tasks":[{'id':'1','taskname':'bring form pharmacy','param':[{'arg1':'congistal','arg2':'panadol'},{'paint':'2'}] }] }



response = requests.post(BASE+'/api/PostMission',json= mission)
print(response.json())
#response = requests.get(BASE+'api/InvestigateCorona',json= [{'MainName':'Person','ApiName':'PatientAPI','id':'1'}])
#print(response.json())
#Get Current Mission
#responseGet = requests.get(BASE+'/api/GetMission')
#print(responseGet.json())

#add New Task
#response = requests.post(BASE+'/api/AddTask',json= {'taskName':'Charge','parameters':[{'MainName':'Items','ApiName':'AnchorAPI','id':'1'}]})
#print(response.json())
#response = requests.post(BASE+'/api/AddTask',json= {'taskName':'GuidToLocation','parameters':[{'MainName':'Person','ApiName':'PatientAPI','id':'1'}]})
#print(response.json())

#response = requests.get('https://robohub.pythonanywhere.com/swagger/Items/AnchorAPI/ '+ 'Authorization: Token 9054f7aa9305e012b3c2300408c3dfdf390fcddf')
#print(response.json())
