# Finops Usecase 1 

Note: Automation does not make any changes to the AWS resources nor cost.


## Steps required to run the python code
* Install python3
* git clone git@github.com:BlogMedium/FinopsSeries-Usecase1.git
* Install the below library required to run the python code
```
pip3 install boto3
pip3 install json
pip3 install csv
pip3 install pandas
pip3 install matplotlib
pip3 install seaborn
```
* Makes changes to the below lines in the code
Update the webhook for micorsoft teams
```
msg = pymsteams.connectorcard("https://outlook.office.com/webhook/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
```
Update the S3 bucket name and Fileupload path for all the below lines appropriately in the code.
```
s3.Object('billing-dashboard', fileupload).upload_file(Filename='C:\\Users\\Administrator\\IdeaProjects\\billing\\'+ fileupload)
```
* Create AWS profile and replace the profiles name in 
```
    profiles = ["dev", "test", "preprod", "prod"]
```

##output
CSV file and bar chart will be created which consists for cost data for almost 6 months.





