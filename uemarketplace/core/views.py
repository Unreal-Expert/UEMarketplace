from django.shortcuts import render
from django.http import JsonResponse
from io import StringIO
import paramiko
from django.http import HttpResponse
import requests
import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

# Create your views here.


def frontpage(request):
    return render(request, 'core/frontpage.html')


def htmx_rocks(request):
    return render(request, 'core/partials/htmx_rocks.html')


def pixel_streaming(request):
    return render(request, 'core/partials/pixel_streaming.html')


def generate_ssh_key(request):
    private_key = paramiko.RSAKey.generate(bits=2048)
    public_key = f'ssh-rsa {private_key.get_base64()}'
    private_key_str = StringIO()
    private_key.write_private_key(private_key_str)
    private_key_str.seek(0) 
        
    try:
        token = get_secret()
    except ClientError as e:
        return HttpResponse(f"Failed to fetch secret: {e}", status=400)

    repo = "EveryGoodWork/TwitchChat__UE5.2"
    title = f"Deploy Key_{datetime.now().strftime('%Y%m%d_%H:%M:%S')}"
    
    try:
        add_deploy_key(token, repo, title, public_key)
    except requests.exceptions.RequestException as e:    
        return HttpResponse(f"Failed to add deploy key: {e}", status=400)    
    response = HttpResponse(private_key_str.getvalue(), content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=githubdeploy_key'    
    return response


def add_deploy_key(token, repo, title, public_key):
    url = f"https://api.github.com/repos/{repo}/keys"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "title": title,
        "key": public_key.strip(),
        "read_only": True,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()

def get_secret():
    secret_name = "TwitchChat__UE5.2_DevToken"
    region_name = "us-east-2"
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e
    
    secret_string = get_secret_value_response['SecretString']
    secret_dict = json.loads(secret_string)
    return secret_dict.get('GitHubToken', '')