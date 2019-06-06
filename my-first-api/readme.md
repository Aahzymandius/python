Steps to deploy API

    1. Create docker images for each of the python apps (people-api, person-api, db-fill). Push these images to the repo of your   choice

    2. Setup the namespace and configMaps for our deployments:
        kubectl apply -f env.yaml
    
    3. Create the MySQL database:
        kubectl apply -f mysql.yaml
    
    4. Run the db-fill job to populate the database (make sure to update the yaml with your db-fill image)
        kubectl apply -f db-fill.yaml

    5. Deploy the API frontends (make sure to (make sure to update the yaml with the people and person images)
           kubectl apply -f api.yaml

