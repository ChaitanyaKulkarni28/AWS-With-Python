import boto3

client = boto3.client('cloudwatch')

#end = datetime.datetime.utcnow().strftime('%Y-%m-%d')
#start = (datetime.datetime.utcnow()-datetime.timedelta(days=14)).strftime('%Y-%m-%d')

id = 'i-xxxx'
response = client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                'Name': 'InstanceId',
                'Value': 'i-xxxx'
                },
            ],
            StartTime='2018-10-3',
            EndTime='2018-10-17',
            Period=86400,
            Statistics=[
                'Average','Maximum',
            ],
            Unit='Percent'
        )

response1 = client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='NetworkIn',
            Dimensions=[
                {
                'Name': 'InstanceId',
                'Value': id
                },
            ],
            StartTime='2018-10-3',
            EndTime='2018-10-17',
            Period=86400,
            Statistics=[
                'Average','Maximum',
            ],
            Unit='Bytes'
        )

print("Network I/P")

print("         Average           Maximum")

for cpu in response1['Datapoints']:
  if 'Average' in cpu:
    print(cpu['Timestamp'].strftime('%Y-%m-%d')," ",cpu['Average']," ",cpu['Maximum'])

print("")
print("CPU utilization")

print("         Average           Maximum")
#print(response)

for cpu in response['Datapoints']:
  if 'Average' in cpu:
    print(cpu["Timestamp"].strftime('%Y-%m-%d')," ",cpu['Average']," ",cpu['Maximum'])
