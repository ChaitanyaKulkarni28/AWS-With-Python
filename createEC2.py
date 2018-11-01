
import boto3
import os
import stat

ec2 = boto3.resource('ec2')

key_name = 'automationKey'
key_ext = key_name+'.pem'

key = ec2.create_key_pair(KeyName = key_name)
#key.key_material will show you private key

with open(key_ext,'w') as key_file:
	key_file.write(key.key_material)
	
#Changing file permission to read write for user only.
os.chmod(key_ext, stat.S_IRUSR | stat.S_IWUSR)

#AMI IDs are region specific so may not work cross region so better way is to use AMI name

#Get image name from imageid
img = ec2.Image('ami-xxxxx')
name = img.name

instances = ec2.create_instances(ImageId = img.id, MinCount = 1, MaxCount = 1, InstanceType = 't2.micro', KeyName = key.key_name)

inst = instances[0]

inst.wait_until_running()

public_dns_name = inst.public_dns_name

#Authorize incoming connections from our public IP on ssh port (22)
sg = ec2.SecurityGroup(inst.security_groups[0]['GroupId'])

sg.authorize_ingress(IpPermissions=[{'FromPort':22,'ToPort':22, 'IpProtocol': 'TCP', 'IpRanges':[{'CidrIp':'your_public_ip/32'}]}])

#Allow all http connections
sg.authorize_ingress(IpPermissions=[{'FromPort':80,'ToPort':80, 'IpProtocol': 'TCP', 'IpRanges':[{'CidrIp':'0.0.0.0/0'}]}])
