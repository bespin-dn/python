import os
import boto3

from fastapi import FastAPI

app = FastAPI()

# AWS S3 Client 생성
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

# AWS KMS Client 생성
kms_client = boto3.client(
    'kms',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)


## Abount S3
@app.get("/s3/buckets")
def list_s3_buckets():
    response = s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    return {"buckets": buckets}


## About KMS
@app.get("/kms/keys")
def list_kms_keys():
    # 모든 키 ID를 가져옴
    response = kms_client.list_keys()
    cmk_keys = []
    aliases = {}

    # 별칭 가져오기
    alias_response = kms_client.list_aliases()
    for alias in alias_response['Aliases']:
        if 'TargetKeyId' in alias:  # TargetKeyId가 있는 경우
            aliases[alias['TargetKeyId']] = alias['AliasName']

    # CMK 키만 필터링
    for key in response['Keys']:
        key_id = key['KeyId']
        key_info = kms_client.describe_key(KeyId=key_id)
        if key_info['KeyMetadata']['KeyManager'] == 'CUSTOMER':  # 고객 관리형 키
            key_alias = aliases.get(key_id, "No Alias")  # 별칭이 없을 경우 "No Alias"
            cmk_keys.append({"KeyId": key_id, "Alias": key_alias})

    return {"keys": cmk_keys}





#async def root():
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/home")
async def home():
    return {"message": "Home"}

@app.get("/home/{name}")
async def read_name(name: str):
    return {'name' : name}

@app.get("/home_err/{name}")
async def read_name_err(name: int):
    return {'name' : name}

## POST Method
@app.post("/")
async def home_post(msg: str):
    return {"Hello" : "POST", "msg": msg}