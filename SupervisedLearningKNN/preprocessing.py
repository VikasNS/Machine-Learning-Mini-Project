all_subject = ['MAT101','PHY101','CV101','EE101','HSS103','CS101','PHYL101','ME102','CSL101','MAT201','CHY201','ME201','EC201','HSS201','HSS202','AL201','CHYL201','MEL203','IS32','IS33','IS31','IS34','IS36','IS35','ISL37','ISL38','IS42','IS41','IS43','IS44','IS45','IS46','ISL47','ISL48']
gradeToPoints ={'S+':10,'S':9,'A':8,'B':7,'C':6,'D':5,'E':4,'F':2}
import csv

with open('rawDataset.txt','r') as dataset:
    studentCount = 0
    subjectCount = 0
    i=0
    arr = []
    studentsArr = []
    studentDic = {}
    c=0
    cc={}
    for row in dataset:
        c+=1
        row = [column.strip() for column in row.split(",")]

        if row[1] not in cc:
            cc[row[1]] = 1
        else :
            cc[row[1]] += 1

        studentDic[row[1]]=row[2]
        if((row[0]=='') and (i!=0)):
            i+=1
            if(len(studentDic) in (34,35)):
                studentsArr.append(studentDic)
            studentDic = {}
        else:
            i=1
        subjectCount+=1
studentVectors =[]
for student in studentsArr:
    studentVector = []
    for subject in all_subject:
        if subject not in student.keys():
            studentVector.append(8)
        else:
            studentVector.append(gradeToPoints[student[subject]])
    studentVectors.append(studentVector)
    #print(len(studentVector))

#26 + 8


with open('IS42.csv','w',newline="") as f_out:
    data = []
    writer = csv.writer(f_out)
    for studentVector in studentVectors:
        row = studentVector[:26] + [studentVector[26]]
        data.append(row)
    writer.writerows(data)

with open('IS41.csv','w',newline="") as f_out:
    data = []
    writer = csv.writer(f_out)
    for studentVector in studentVectors:
        row = studentVector[:26] + [studentVector[27]]
        data.append(row)
    writer.writerows(data)

with open('IS43.csv','w',newline="") as f_out:
    data = []
    writer = csv.writer(f_out)
    for studentVector in studentVectors:
        row = studentVector[:26] + [studentVector[28]]
        data.append(row)
    writer.writerows(data)

with open('IS44.csv','w',newline="") as f_out:
    data = []
    writer = csv.writer(f_out)
    for studentVector in studentVectors:
        row = studentVector[:26] + [studentVector[29]]
        data.append(row)
    writer.writerows(data)

with open('IS45.csv','w',newline="") as f_out:
    data = []
    writer = csv.writer(f_out)
    for studentVector in studentVectors:
        row = studentVector[:26] + [studentVector[30]]
        data.append(row)
    writer.writerows(data)

with open('IS46.csv','w',newline="") as f_out:
    data = []
    writer = csv.writer(f_out)
    for studentVector in studentVectors:
        row = studentVector[:26] + [studentVector[31]]
        data.append(row)
    writer.writerows(data)

with open('IS47.csv','w',newline="") as f_out:
    data = []
    writer = csv.writer(f_out)
    for studentVector in studentVectors:
        row = studentVector[:26] + [studentVector[32]]
        data.append(row)
    writer.writerows(data)

with open('IS48.csv','w',newline="") as f_out:
    data = []
    writer = csv.writer(f_out)
    for studentVector in studentVectors:
        row = studentVector[:26] + [studentVector[33]]
        data.append(row)
    writer.writerows(data)