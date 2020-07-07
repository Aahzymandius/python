#!/usr/bin/env python

import boto3

profile = input("aws cli profile: ")
region = input("aws region: ")

boto3.setup_default_session(profile_name=profile)
ec2_client = boto3.client('ec2', region_name=region)
ec2 = boto3.resource('ec2', region_name=region)


def list_of_volumes():
    listVolumes = ec2_client.describe_volumes()

    volumeIds = []
    for volume in listVolumes['Volumes']:
        volumeIds.append(volume['VolumeId'])
    print(volumeIds)
    return(volumeIds)

def list_snapshots(volumeId):
    allSnapshots = ec2_client.describe_snapshots(
        Filters=[{'Name':'volume-id', 'Values':[volumeId]}]
    )
    sortedList = sorted(allSnapshots['Snapshots'], key=lambda x: x['StartTime'])
    oldSnapshots = sortedList[:-7]
    return(oldSnapshots)

def delete_snapshot(id):
    getSnapshot = ec2.Snapshot(id)
    getSnapshot.delete()

def main():
    volumeIdList = list_of_volumes()
    for id in volumeIdList:
        snapshots = list_snapshots(id)
        if not snapshots:
            print('no Snapshots to deleted for ' + id)
        else:
            for snapshot in snapshots:
                try:
                    delete_snapshot(snapshot['SnapshotId'])
                    print('deleted ' + snapshot['SnapshotId'])
                except:
                    print("can't delete snapshot " + snapshot['SnapshotId'] + ". It may be managed by AWS.")

if __name__ == '__main__':
    main()
