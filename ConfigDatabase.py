from flask import Flask, request, jsonify
from flask_restful import Api ,Resource
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///MissionControlDB.db'
db = SQLAlchemy(app)





class Mission(db.Model):
    __tablename__ = 'Mission'

    id = db.Column(db.Integer, primary_key=True)
    startTime =db.Column(db.DateTime, nullable=False)
    State = db.Column(db.String(256))
    tasksNumber =db.Column(db.Integer, nullable=True)
    tasksInfo = db.Column(JSON, nullable=False)
    
    def __init__(self, startTime,State,tasksNumber, tasksInfo):
        self.startTime = startTime
        self.State = State
        self.tasksInfo = tasksInfo
        self.tasksNumber=tasksNumber

    def __repr__(self):
        return f"Mission(id={self.id},starttime={self.startTime},tasksNumber={self.tasksNumber},State={self.State},tasksInfo={self.tasksInfo})" 

    @property
    def serialize(self):
        return {
            'startTime': self.startTime,
            'State': self.State,
            'tasksNumber':self.tasksNumber,
            'tasksInfo': self.tasksInfo,
            'id': self.id,
        }



class MisssionTasksLog(db.Model):
    __tablename__ = 'MisssionTasksLog'
    id =db.Column(db.Integer, primary_key=True)
    MissionId =db.Column(db.Integer,db.ForeignKey('Mission.id') ,nullable=False)
    mission =db.relationship('Mission') 
    TaskId=db.Column(db.Integer,db.ForeignKey('Task.id'),nullable=False) 
    task = db.relationship('Task') 
    StartTimeTask= db.Column(db.DateTime, nullable=False)
    TaskInfo=db.Column(JSON, nullable=False)


    def __init__(self, id,MissionId, TaskId,StartTimeTask,TaskInfo):
        self.id =id
        self.MissionId = MissionId
        self.TaskId = TaskId
        self.StartTimeTask=StartTimeTask
        self.TaskInfo=TaskInfo


    def __repr__(self):
        return f"MissionTask(id={self.id},MissionId={self.MissionId},TaskId={self.TaskId},StartTimeTask={self.StartTimeTask},TaskInfo={self.TaskInfo})" 

    @property
    def serialize(self):
        return {
            'MissionId': self.MissionId,
            'TaskId': self.TaskId,
            'StartTimeTask':self.StartTimeTask,
            'TaskInfo':self.TaskInfo,
            'id': self.id,
        }


class Task(db.Model):
    __tablename__ = 'Task'

    id = db.Column(db.Integer, primary_key=True)
    taskName =db.Column(db.String(256), nullable=False)
    parameters=db.Column(JSON,nullable=False) #will change
    
    def __init__(self, taskName, parameters):
        self.taskName = taskName
        self.parameters = parameters
       

    def __repr__(self):
        return f"Task(id={self.id},taskName={self.taskName},parameters={self.parameters})" 

    @property
    def serialize(self):
        return {
            'taskName': self.taskName,
            'parameters': self.parameters,
            'id': self.id,
        }





#db.drop_all()
#db.create_all()