# Developer Guide
This is a chat bot web service that upload response to S3 storage

## Perquisite
install dependencies, you could refer to requirement.txt if you deploy locally.
```
python3 -m venv venv
source venv/bin/activate
pip install boto3
pip install flask
```

You need set AWS crendential properly either via env like below. It will used to upload files to S3.
eg.
```
export AWS_ACCESS_KEY_ID='your key'
export AWS_SECRET_ACCESS_KEY='your secret'
```
Also update the coresponding s3 bucket name and object path in app.py while deploy the service
```
s3_bucket='<your-s3-bucket-name>'
object_path='<object-key>'
```

## QR code
This in-place QR code is only for testing, if you need to deploy on a production env, please using your own link regenerte. Or re-use the commented code in the app.py
```
qr = qrcode.make(link)
```
 