from flask import Flask, request, jsonify
from flask_restful import Api ,Resource
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from ConfigDatabase import Mission,Task
import pandas as pd
import json
from requests.auth import HTTPDigestAuth
from apscheduler.schedulers.background import BackgroundScheduler as scheduler
import requests
from Tasks import TaskShooter
from werkzeug.datastructures import ImmutableMultiDict


DjangoProject='http://127.0.0.1:8000/'
auth='http://127.0.0.1:8000/api-token-auth/'

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///MissionControlDB.db'
db = SQLAlchemy(app)
shooter=TaskShooter()

@app.route("/api/critcal", methods=['POST'])
def Critical_msg():
    cmmand=request.form
    msg=cmmand.to_dict()
    shooter.Critical_msg(msg)

@app.route("/api/GetMission", methods=['POST'])
def mission_req():
    routeMission= dict()
    current_mission=request.form
    currentMisssion=current_mission.to_dict()
    routeMission=currentMisssion
    routeMission['tasks']=PrepareTasksInfo(currentMisssion.tasks)
    if len(routeMission) != 0:
        shooter.Fire(routeMission)   
        UpdateMissionStatus(routeMission[id])      
    return {'status':"Success"},201
  
def Stored_Missions():
    routeMissions = dict()
    now = datetime.now().replace(second=0, microsecond=0)
    currentMisssions = Mission.query.filter((Mission.startTime == now) & (Mission.State == 'Pending')).all()
    for mission in currentMisssions:
        routeMissions['id']=mission.id
        routeMissions['#tasks']=mission.tasksNumber
        routeMissions['tasksInfo']=PrepareTasksInfo(mission.tasksInfo)
        UpdateMissionStatus(mission.id)
    if len(routeMissions) != 0:
        shooter.Fire(routeMissions)  
    return routeMissions
  
def PrepareTasksInfo(tasks):
    tasksInfo=[]
    parameters=[]
    for task in tasks:
        parameters.append(task['param'][0])   
        paramNeedAnchor=task['param'][1]
        if len(paramNeedAnchor) != 0:
            anchorXY=GoToLocation(paramNeedAnchor)
            parameters.append(anchorXY)
        tasksInfo.append({"id":task['id'] , "taskname":task['taskname'],'param':parameters})
    return tasksInfo

def GetToken():
    result=requests.post(auth, data={'username': 'admin', 'password': '1234'})
    return result.json()

def GoToLocation(parameters):
    token = GetToken()
    headers = {'Authorization': 'token {}'.format(str(token['token']))}
    for param in parameters:
        try : 
                if  "patient" in param :
                    patientResult=requests.get(DjangoProject +'Person/PatientAPI/'+str(parameters[param]),headers=headers)
                    patientObject=patientResult.json()
                    roomResult=requests.get(DjangoProject+'Places/RoomAPI/'+str(patientObject['stay_room']),headers=headers)
                    roomObj=roomResult.json()
                    print(roomObj)
                    anchorId=roomObj['main_anchor']
                else :
                    print(param)
                    url=DjangoProject +'Places/'+param+'API/'+str(parameters[param])
                    print(url)
                    placeResult=requests.get(url,headers=headers)
                    placeObject=placeResult.json()
                    print(placeObject)
                    anchorId= placeObject['main_anchor']
        except :
            print('error')
            return {}
    anchorResult=requests.get(DjangoProject+'Items/AnchorAPI/'+str(anchorId),headers=headers)
    anchorObj=anchorResult.json()    
    return {'anchorId': anchorObj['id'],
             'X_location': anchorObj['X_location'], 
             'Y_location': anchorObj['Y_location'], 
             'anchorDescription': anchorObj['description']
             }

@app.route("/api/PostMission", methods=['POST'])
def PostMission():
    data = request.get_json()
    startTime = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')
    missionObject= Mission(startTime,'Pending',data['#tasks'],data['tasks'])
    db.session.add(missionObject)
    db.session.commit()
    return {'status':"Added Successfully"},201

def UpdateMissionStatus(id):
  mission = Mission.query.filter(Mission.id == id).update(dict({'State': 'Sent'}))
  db.session.commit()



# automatic infoke after 5 sec
sch = scheduler()
sch.add_job(Stored_Missions, 'interval', seconds=5)  #10 min => 600 sec
sch.start()


#mission Format
# mission = {"id": "1",'start_time':'', "#tasks": "2","tasks":[{'id':'1','taskname':'bring form pharmacy','param':[{'arg1':'congistal','arg2':'panadol'},{'paint':'2'}] }] }

if __name__ == "__main__":
    app.run(debug=True)