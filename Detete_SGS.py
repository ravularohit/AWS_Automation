import boto3

r=input("enter the Region which you want to go through: ")
ec2 = boto3.resource('ec2',region_name=r)
delete= boto3.client('ec2',region_name=r)
sgs = list(ec2.security_groups.all())
insts = list(ec2.instances.all())

all_sgs = [{sg.group_id:sg.group_name} for sg in sgs]
all_inst_sgs = [{sg['GroupId']:sg['GroupName']} for inst in insts for sg in inst.security_groups]
unused_sgs = [x for x in all_sgs if x not in all_inst_sgs]
print("all_security_groups :")
for i in all_sgs:
    print(i,end="\n")
print("Used_Security_groups:")
for i in all_inst_sgs:
    print(i,end="\n")
print("UnUsed_Security_groups:")
for i in unused_sgs:
    print(i,end="\n")
y=input("do you want to delete selective sgs(S) / do you want to delete all groups at a time (all):ENTER (S/All): ")
if(y.lower()=='s'):
    for i in unused_sgs:
        gid,name=zip(*i.items())
        if(name[0]=="default"):
            pass
        else:
            d=input("Do you want to delete this group{0}:(Y/N)".format(i))
            if(d.lower()=="y"):
                delete.delete_security_group(GroupName=name[0])
                print("Successful deleted {0}!!".format(name[0]))
            elif(d.lower=='n'):
                print("Aborting...")

elif(y.lower()=='all'):
    d=input("Are you sure you want to delete all the unused groups (Y/N):")
    if(d.lower()=='y'):
        for i in unused_sgs:
            gid,name=zip(*i.items())
            if(name[0]=="default"):
                pass
            else:
                delete.delete_security_group(GroupName=name[0])
                print("Successful deleted {0}!!".format(name[0]))
    elif(d.lower()=='n'):
        print("Aborting...")
#print(unused_sgs)


#delete.delete_security_group(GroupName='test-sg')
