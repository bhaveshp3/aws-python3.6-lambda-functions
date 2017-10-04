import json

import boto3
import datetime

print('Loading function')
 

ec2client = boto3.client('ec2',region_name='us-west-2')

def lambda_handler(event, context):
    #  To add Image creation date as a name and a Tag on AMI
    creationdate = datetime.datetime.now()
    creationdatetimestr =creationdate.strftime('%Y-%m-%d_%H-%M-%S')

    instanceid = 'i-0c2f14c0ab0430147'  ## project Instance Id

    newimage = ec2client.create_image(Description="production-website_created_by_Lambda_function",InstanceId=instanceid,DryRun=False,Name="production-website-"+creationdatetimestr,NoReboot=True)

    print(newimage)
    print("AMI : "+ newimage['ImageId'] + " is created...")  