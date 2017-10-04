import json
import urllib.parse
import boto3
import datetime
import dateutil.parser

print('Loading function')


imageclient= boto3.client('ec2',region_name='us-west-2')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    
    current_date= datetime.datetime.now()
    image_removal_date = current_date + datetime.timedelta(days=-15)		## AMI retension period is 15 days
    #print(image_removal_date)
    response = imageclient.describe_images(DryRun=False,Owners=['self'], Filters=[{'Name': 'state','Values':['available']}, {'Name':'name','Values':['production-website-*']}])
    if response is None:
        print("Images does not exists")
    else:
        for image_desc in response['Images']:
            image_name=image_desc['ImageId']           
            print("AMI "+ image_name+ " is deleting...")
            image_creation_date_str = image_desc['CreationDate']	## Obtain Image_creation_date from AMI Attributes
        
            image_creation_date = dateutil.parser.parse(image_creation_date_str)	## Convert Timezone format date to normal date
        
            image_creation_date_object = datetime.datetime.strptime(image_creation_date.strftime('%Y-%m-%d'),'%Y-%m-%d') ## Converting date object to yyyy-mm-dd format	 
        
            if 	image_creation_date_object < image_removal_date :
                print("Image Creation Date was : "+ image_creation_date_object.strftime('%Y-%m-%d'))
                image_deregistration_response= imageclient.deregister_image(ImageId=image_name,DryRun=False)
                print(image_deregistration_response)
            
                for blockdevicemappings in image_desc['BlockDeviceMappings']:
                    ebslist = blockdevicemappings['Ebs']
                    my_snapshot_id=ebslist['SnapshotId']
                    print("Snapshot Id : "+ my_snapshot_id + " is deleting...")
                    delete_snapshot_response = imageclient.delete_snapshot(SnapshotId=my_snapshot_id,DryRun=False)
                    print(delete_snapshot_response)