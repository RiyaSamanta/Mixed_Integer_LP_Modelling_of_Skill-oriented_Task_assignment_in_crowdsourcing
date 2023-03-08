import csv
import random

class Task:
    def __init__(self, id,skill,budget):
        self.Id = id
        self.Skills = skill
        # self.skillCount=len(self.Skills)
        # self.remainingSkillCount=len(self.Skills)
        self.Budget = budget
        self.RemaningBudget = budget
        self.assignments = {}
        self.isComplete = False
        for skill in self.Skills :
            self.assignments[skill] = 0    # 0 means it does not assigned with any volunteers
                                           # if it is assigned with any other volunteers then its id 
                                           # will be shown here, and that will be start from 1 
        

    def __repr__(self):
        return "[" + str(self.Id) +  ":"  +  str(self.Skills) + ":" + str(self.Budget) + ":" + str(self.RemaningBudget) + "]"

    def update_task_complete_status(self):
        completed = True
        for ele in self.assignments.values():
            if ele == 0 :
                completed = False
        self.isComplete = completed
        if self.isComplete :
            print("************************** Task Completed!" , self.Id)
            
    def get_budget(self,id):
        for ele in self.Id:
            if ele==id:
                return self.Budget
        

    def get_task_completion_status(self):
        completed = 0
        total = 0
        for ele in self.assignments.values():
            if ele == 0 :
                completed = completed + 0
            else :
                completed = completed + 1
            total = total + 1
        return (completed/total)*100,completed,total

def get_all_tasks_and_skills(filename,t_size):
    Unique_skills = set()
    records = []
    content=open(filename,'r').readlines()
    content=content[1:]
    random.shuffle(content)
    content=content[:t_size]
    i=0
    for line in content:
        line=line.replace("\"","")
        row=line.split(",")
        # id=int(row[0])
        id=i
        i=i+1
        budget=float(row[-1])
        skills=row[1:-1]
        # skills=set(skills)
        # skills=list(skills)
        records.append(Task(id,skills,budget))
        for skill in skills:
              Unique_skills.add(skill)     
    return records, Unique_skills

def generate_G_ST(tasks, unique_skills):
   
    mapper = {}
    task_N = len(tasks)
    for skill in unique_skills:
        row = []
        for i in range(0,task_N):
            task = tasks[i]
            if task.Id == i+1 :
                
                if skill in task.Skills:
                    row.append(1)
                else:
                    row.append(0)
            else :
                print("****************** Error in generating GST")
        mapper[skill]=row
        # print("---------------------", skill,sum(row))
    # print(mapper)
    return mapper

#

# if __name__ == '__main__':
#     tasks,skills = get_all_tasks_and_skills("tasks.csv")
    # print(skills)
    # generate_G_ST(tasks,skills)
    # for i in tasks:
    #         print(i)
