#Steps to deploy API

##1. Create docker images 

For each of the python apps (people-api, person-api, db-fill), you must build the image. Push these images to the repo of your choice. I used Google Cloud Build as it compiles the image remotely and automatically pushed to my GCR.

##2. Setup the namespace and configMaps for our deployments
  
    kubectl apply -f env.yaml
    
##3. Create the MySQL database
  
    kubectl apply -f mysql.yaml
    
##4. Populate the Database

Run the db-fill job to populate the database (make sure to update the yaml with your db-fill image).

    kubectl apply -f db-fill.yaml

##5. Deploy the API 

Deploy the APIfrontends (make sure to update the yaml with the people and person images)

    kubectl apply -f api.yaml

You should now have 3 deployments (2 different API frontends and the Mysql StatefulSet) as well as a few services.
You can check the status of your resources with the following:

    kubectl get po,svc,ing -n titanic

Once the Ingress has an IP assigned
