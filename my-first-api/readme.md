# Steps to deploy API

## 1. Create docker images 

For each of the python apps (people-api, person-api, db-fill), you must build the image. Push these images to the repo of your choice. I used Google Cloud Build as it compiles the image remotely and automatically pushed to my GCR.

## 2. Setup the namespace and configMaps for our deployments

The env.yaml contains required configMaps which our deployments will rely on at creation.
A secret is also required to contain the DB username and password. Replace the [username] and [set_password] fields to which ever you would like to use, both the apps and the DB will use these credentials.
  
    kubectl apply -f env.yaml
    kubectl create secret db-secrets --from-literal=user=[username] --from-literal=password=[set_password] -n titanic
    
## 3. Create the MySQL database
  
    kubectl apply -f mysql.yaml
    
## 4. Populate the Database

Run the db-fill job to populate the database; **make sure to update the yaml with your db-fill image**.

    kubectl apply -f db-fill.yaml

Note that the db-fill job will clean itself up 5 minutes after completion. The 5 minute window allows you time to inspect the pod or review container logs.

## 5. Deploy the API 

Deploy the APIfrontends; **make sure to update the yaml with the people and person images**

    kubectl apply -f api.yaml

You should now have 3 deployments (2 different API frontends and the Mysql StatefulSet) as well as a few services.
You can check the status of your resources with the following:

    kubectl get po,svc,ing -n titanic

Once the Ingress has an IP assigned, test the API using the following defined methods:

- GET /people
- POST /people (this requires including json data)
- GET /people/uuid
- DELETE /people/uuid
- PUT /people/uuid (this requires including json data)

## Clean up

To clean up, you can delete the namespace and all the resources you just created will be deleted.

    kubectl delete ns titanic
