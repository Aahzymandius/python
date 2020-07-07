#!/usr/bin/env python

import boto3

profile = input("aws cli profile: ")
region = input("aws region: ")

boto3.setup_default_session(profile_name=profile)
ec2_client = boto3.client('ec2', region_name=region)
ec2 = boto3.resource('ec2', region_name=region)


def list_of_instances():
    listInstances = ec2_client.describe_instances(
        Filters=[{'Name':'tag-key','Values':['role']}]
    )
    reservations = listInstances['Reservations']

    instanceIds = []
    for reservation in reservations:
        for instance in reservation['Instances']:
            instanceIds.append(instance['InstanceId'])
    return(instanceIds)

def list_amis(instanceId):
    allImages = ec2_client.describe_images(
        Filters=[{'Name':'tag:instance_id', 'Values':[instanceId]}]
    )
    sortedList = sorted(allImages['Images'], key=lambda x: x['CreationDate'])
    oldImages = sortedList[:-2]
    return(oldImages)

def delete_amis(id):
    getImage = ec2.Image(id)
    getImage.deregister()

def main():
    instanceIdList = list_of_instances()
    for id in instanceIdList:
        amis = list_amis(id)
        if not amis:
            print('no AMIs to deleted for ' + id)
        else:
            for ami in amis:
                delete_amis(ami['ImageId'])
                print('deleted ' + ami['ImageId'])

if __name__ == '__main__':
    main()
