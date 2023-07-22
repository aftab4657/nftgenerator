from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, LogInForm
from django.http import HttpResponse
from celery.result import AsyncResult
from .tasks import *
import pandas as pd
import os, uuid
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import zipfile, json
from PIL import Image, ImageDraw, ImageFilter
from .forms import UploadFileForm, GenerateNFTsForm,GenerateNFTsForm_defaul_value
from .task import long_task
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
import time
import requests
import asyncio
import subprocess
import json
from .models import Task
import re
from django.db import connections
from pathlib import Path
from django.http import HttpResponse
import datetime
import itertools
import pymongo

# Rest of your code

# from pymongo import MongoClient
# cluster = pymongo.MongoClient("mongodb+srv://aftab4657:Y7mPlvkAL54JSGta@nftgentasks.as4m7os.mongodb.net/?retryWrites=true&w=majority")
# db = cluster["nftgen2"]
# collection = db["userRegistration_task"]
# result = collection.delete_many({})  # Empty filter to match all documents
# print(f"Deleted {result.deleted_count} records from the collection.")

# tracemalloc.start()



def home(request):
    form = UploadFileForm()
    gennftForm = GenerateNFTsForm()
    return render(request, 'home.html', {'form': form, 'nftForm': gennftForm})

def layers(request):
    gennftForm = GenerateNFTsForm()
    return render(request, 'uploadsLayers.html', {'nftForm': gennftForm})

@csrf_exempt
def upload_layers(request):
    # time.sleep(10)
    try:
        where = 0
        BASE_DIR = settings.MEDIA_ROOT
        if request.method == 'POST':
            where = 1
            folderName = f"{uuid.uuid4()}"
            # Create the uploads folder if it doesn't already exist
            containsDir = os.path.join(BASE_DIR, f"{folderName}")
            containsDir = Path(containsDir)
            if not os.path.exists(containsDir):
                os.makedirs(containsDir)

            inputDir = os.path.join(BASE_DIR, f"{folderName}/input")
            inputDir = Path(inputDir)
            if not os.path.exists(inputDir):
                os.makedirs(inputDir)
            
            assetsDir = os.path.join(BASE_DIR, f"{folderName}/input/assets")
            if not os.path.exists(assetsDir):
                os.makedirs(assetsDir)

            outputDir = os.path.join(BASE_DIR, f"{folderName}/output")
            if not os.path.exists(outputDir):
                os.makedirs(outputDir)

            nfts_Dir = os.path.join(BASE_DIR, f"{folderName}/output/nfts")
            if not os.path.exists(nfts_Dir):
                os.makedirs(nfts_Dir)
            layers = [[k, v] for k, v in request.POST.items() if k.startswith('layer')]
            for layer in layers:
                print(layer)
                layer_order_number = layer[0].replace("layer", "")
                print(f'lay_img{layer_order_number}')
                rarities = [[k, v] for k, v in request.POST.items() if k.startswith(f'lay_rarity{layer_order_number}')]

                layer_order_number = str(layer_order_number).replace("-", "")
                layer_Folder = os.path.join(BASE_DIR, f"{folderName}/input/assets/{layer_order_number}-" + str(layer[1]).strip().replace(" ", "_"))
                if not os.path.exists(layer_Folder):
                    os.makedirs(layer_Folder)
                for rar in rarities:
                    index = rar[0].replace(f'lay_rarity{layer_order_number}', "")
                    rarity = request.POST.get(f'lay_rarity{layer_order_number}{index}')
                    rarity = str(rarity).split(".")[0]
                    attribute = request.POST.get(f'lay_attribute{layer_order_number}{index}')
                    attribute = str(attribute).split("-")[-1]
                    attribute = str(attribute).strip().replace("-", " ").replace(" ", "_")

                    # regex = re.compile('^[0-9]')
                    # if regex.match(attribute):
                    #     attribute = "a_" + attribute
                    file_name = f"{rarity}-{attribute}"
                    image_file = request.FILES.get(f'lay_img{layer_order_number}{index}')
                    original_name, file_extension = os.path.splitext(image_file.name)
                    with open(os.path.join(layer_Folder, f"{file_name}{file_extension}"), 'wb') as f:
                        f.write(image_file.read())
            where = "before inserting into db"
            new_task_object = Task(status="created", message="Processing...", folder_name= f"{folderName}")
            where = "inserting 1"
            new_task_object.save()

            where = "inserting 2"
            task_id = new_task_object.id
            where = "completed_success"
            

            return JsonResponse({'success': True, "input": f"{folderName}", "output": f"{folderName}/output", "task_id": task_id})
    except Exception as e:
      
        return JsonResponse({'success': True, "input": f"EOOOOORRRRR", "output": f"{BASE_DIR}", "task_id": str(e) + "----" + str(where), "exception": str(e)})

@csrf_exempt
def get_task_status(request):
        print("........................get_task_status test...............")
    # try:
        dir = request.POST.get('output_path')
        task_id = request.POST.get('task_id')
        # print(task_id)
        # print("hhhurayyyyyyy", task_id)
        if "uploads" in dir:
            dir = dir.replace("uploads", "")
        BASE_DIR = settings.MEDIA_ROOT
        folder_path = BASE_DIR + f'/{dir}/nfts/public_mint_assets'
        print(folder_path, "\n Folder path check")
        folder_path = str(Path(folder_path))

        # get task
        # print(folder_path , "000000")
        record_to_update = Task.objects.get(id=task_id)
        # print("f")
        # print(record_to_update)
        # print("/f")
        status = ""
        msg = ""
        cid = ""
        is_valid = False
        if record_to_update:
            is_valid = True
            status = record_to_update.status
            msg = record_to_update.message
            cid = record_to_update.cid_metadata
        if os.path.isdir(folder_path):
            is_valid = True
            files = os.listdir(path=folder_path)
            print(files,'files check')
            images_counter = 0
            for f in files:
                # print(f)
                if f.endswith(".png"):
                    images_counter += 1
            print("---gg---")
            return JsonResponse({'valid': is_valid, "count": images_counter, "status": status, "msg": msg, 'cid':cid })
           
        else:
            print("---gg---")

            return JsonResponse({'valid': is_valid, "dir": folder_path, "status": status, "msg": msg, "count": 0})
    # except Exception as e:
    #     print("e value")
    #     print(e)
    #     print("ndfndddd")
    #     return JsonResponse({"valid": False, 'error': f'Task with ID does not exist.'})


@csrf_exempt
def download_nfts(request):
    try:
        dir = request.POST.get('path')
        BASE_DIR = settings.MEDIA_ROOT
        folder_path = BASE_DIR + f'/{dir}'
        if 'download' in request.POST:
            # do something if button1 was clicked
            folder_path = str(folder_path).replace("output", "") + "/resources.zip"
        else:
           folder_path = str(folder_path).replace("output", "") + "/ipfs-resources.zip"
            # do something if button2 was clicked
        
        with open(folder_path, 'rb') as zip_file:
             # Create a response object with the zip file contents
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            # Set the Content-Disposition header to force the browser to download the file
            response['Content-Disposition'] = 'attachment; filename="resources.zip"'
            return response
    except Exception as e:
        return JsonResponse({"valid": False, 'error': f'Error. -> ' + str(e)})

async def make_zip_of_resources(zipPath, folder_path):
    # Loop through all the files and folders in the directory
    print("Making zip")
    print(zipPath, folder_path)
    with zipfile.ZipFile(zipPath, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(folder_path):
            rel_path = os.path.relpath(root, folder_path)
            for file in files:
                print(file)
                # Add each file to the zip archive
                zip_file.write(os.path.join(root, file), arcname=os.path.join(rel_path, file))

            for folder in dirs:
                print(folder)
                # Add each folder to the zip archive
                zip_file.write(os.path.join(root, folder), arcname=os.path.join(rel_path, folder))
    print("Done xziipping")


async def start_long_task(nfts_counters, collection_input, collection_output, zipPath, folder_path):
    if "uploads" not in collection_input:
        collection_input = "/uploads/" + collection_input
    if "uploads" not in collection_output:
        collection_output = "/uploads/" + collection_output
    status , msg = await long_task(nfts_counters, collection_input=collection_input, collection_output=collection_output)
    if status:
        await make_zip_of_resources(zipPath, folder_path)
    return status, msg

from asgiref.sync import sync_to_async
def update_task_status(task_id, status, msg):
            # record_to_update = Task.objects.get(id=task_id)
            record_to_update = Task.objects.get(id=task_id)
            # Update the fields of the record
            record_to_update.status = status
            record_to_update.message = msg
            # Save the updated record back to the database
            record_to_update.save()
            # await sync_to_async(record_to_update.save)()

async def generate_nfts_Layers_old(request):
    
    if request.method == 'POST':
        form = GenerateNFTsForm(request.POST)
        if form.is_valid():
            nftsPaths_input = request.POST.get('nfts_path_input')
            nftsPaths_output = request.POST.get('nfts_path_output')
            name = request.POST.get('name')
            symbol = request.POST.get('symbol')
            description = request.POST.get('description')
            sellerfee = request.POST.get('sellerfee')
            
            collectionname = request.POST.get('collectionname')
            collectionfamily = request.POST.get('collectionfamily')
            creatoraddress = request.POST.get('creatoraddress')
            creatorshare = request.POST.get('creatorshare')
            externalurl = request.POST.get('externalurl')
            totalnfts = request.POST.get('totalnfts')
            temps = {
                'name': name, 
                'symbol': symbol, 
                'description': description, 
                'seller_fee_basis_points': int(sellerfee) * 100, 
                'image': 'image.png', 
                'external_url': externalurl, 
                'attributes': [], 
                'collection': {
                        'name': collectionname, 
                        'family': collectionfamily
                    }, 
                'properties': {'files': [{'uri': 'image.png', 'type': 'image/png'}], 'category': 'image', 
                    'creators': [{
                        'address': creatoraddress, 
                        'share': int(creatorshare)
                        }]
                    }
            }

            BASE_DIR = settings.MEDIA_ROOT


            task_id = request.POST.get('task_id')
            update_task_status(task_id, "running", "task started")
            
                
            temp_path = BASE_DIR + f'/{nftsPaths_input}/input/template.json'
            with open(temp_path, 'w') as f:
                json.dump(temps, f)

            
            zipPath = BASE_DIR + "/" + str(nftsPaths_output).replace("output", "") + 'resources.zip'
            folder_path = BASE_DIR + f'/{nftsPaths_output}'
            # generate_nft.delay([int(totalnfts), 0, 0], collection_input=nftsPaths_input,collection_output= nftsPaths_output, zipPath=zipPath, folder_path=folder_path,task_id=task_id).get()
            # task_one.delay("taskone").get()
            task_one.apply_async(args=["tasktwo"], countdown=5)
            # status , msg = await long_task(nfts_counters, collection_input=collection_input, collection_output=collection_output)
            # apply_async(args=["taskone"], countdown=10).get()          
            task = asyncio.create_task(start_long_task([int(totalnfts), 0, 0], nftsPaths_input, nftsPaths_output, zipPath, folder_path))
            result = await asyncio.wait_for(task, timeout=2)

            if result[0]:
                await update_task_status(task_id, "completed", result[1])
            else:
                await update_task_status(task_id, "error", result[1])


            return JsonResponse({'valid': True, 'status': 'started', 'task_id': "Cronjob", 'output_dir': BASE_DIR + f'/{zipPath}'})
    return JsonResponse({'valid': False, 'status': 'Problem', 'task_id': ""})


def generate_nfts_Layers(request):
        # print("view generate nfts layers start")
        print('...........................test start...................')
        form = GenerateNFTsForm(request.POST)
        if form.is_valid():
            nftsPaths_input = request.POST.get('nfts_path_input')
            nftsPaths_output = request.POST.get('nfts_path_output')
            name = request.POST.get('name')
            symbol = request.POST.get('symbol')
            description = request.POST.get('description')
            sellerfee = request.POST.get('sellerfee')
            
            collectionname = request.POST.get('collectionname')
            collectionfamily = request.POST.get('collectionfamily')
            creatoraddress = request.POST.get('creatoraddress')
            creatorshare = request.POST.get('creatorshare')
            externalurl = request.POST.get('externalurl')
            totalnfts = request.POST.get('totalnfts')
            temps = {
                'name': name, 
                'symbol': symbol, 
                'description': description, 
                'seller_fee_basis_points': int(sellerfee) * 100, 
                'image': 'image.png', 
                'external_url': externalurl, 
                'attributes': [], 
                'collection': {
                        'name': collectionname, 
                        'family': collectionfamily
                    }, 
                'properties': {'files': [{'uri': 'image.png', 'type': 'image/png'}], 'category': 'image', 
                    'creators': [{
                        'address': creatoraddress, 
                        'share': int(creatorshare)
                        }]
                    }
            }

            BASE_DIR = settings.MEDIA_ROOT

            task_id = request.POST.get('task_id')
            # update_task_status(task_id, "running", "task started")
            # print("genetae 1")
            temp_path = BASE_DIR + f'/{nftsPaths_input}/input/template.json'
            
            with open(temp_path, 'w') as f:
                json.dump(temps, f)

            zipPath = BASE_DIR + "/" + str(nftsPaths_output).replace("output", "") + 'resources.zip'
            print(zipPath, '\n zip path check')
            folder_path = BASE_DIR + f'/{nftsPaths_output}'
            # print("before function call")
            # Call the generate_nft task asynchronously
            # number_listnf, testRarities=False, randomizedOutput=False, collection_input="", collection_output="",zipPath="", folder_path="",task_id=""

            # if "uploads" not in nftsPaths_input:
            #     nftsPaths_input = "/uploads/" + nftsPaths_input
            # if "uploads" not in nftsPaths_output:
            #     nftsPaths_output = "/uploads/" + nftsPaths_output
            # print(nftsPaths_input, "............................................ nfts path")
            # print(nftsPaths_output)
            nft_dir_path = BASE_DIR + "/" + nftsPaths_input 
            print(nft_dir_path, "\nnft dir path check")
            # print("$" * 500)
            # generate_nft.delay([int(totalnfts)],collection_input=nftsPaths_input,collection_output= nftsPaths_output,zipPath=zipPath, folder_path=folder_path,task_id= task_id)
            # subprocess.Popen(['python', 'C:\\Users\\Administrator\\Desktop\\nftGen_Arguement\\nftStart.py', '-p', '30', '-d', BASE_DIR + f'/{zipPath}'}])
            try:
                file_path = "nft_gen/nftStart.py"
                full_path_for_python_script = settings.BASE_DIR / file_path #hh
                print(full_path_for_python_script, '\n full nft path check')
                # subprocess.Popen(['python', r'C:\Users\Administrator\Desktop\djangoNftGenerator\nftgen\nft_gen\nftStart.py', '-p', totalnfts, '-d', nft_dir_path, '-i', task_id])
                subprocess.Popen(['python', full_path_for_python_script, '-p', totalnfts, '-d', nft_dir_path, '-i', task_id])
            except Exception as e:
                print(f"An error occurred: {str(e)}")






            # task_one.apply_async(args=["taskone"]).get()
            # print("view generate nfts layers ")
            print("jason resopnse start")
            print({'valid': True, 'status': 'running', 'task_id': str(task_id), 'output_dir': f'{zipPath}'})
            print("jason resopnse end")

            print("...................................test end.....................................")
            return JsonResponse({'valid': True, 'status': 'running', 'task_id': str(task_id), 'output_dir': f'{zipPath}'})
        else:
            # print("form not valid")
            return JsonResponse({'valid': False, 'status': 'Problem', 'task_id': ""})


async def generate_nfts(request):
    if request.method == 'POST':
        form = GenerateNFTsForm(request.POST)
        if form.is_valid():
            nftsPaths_input = request.POST.get('nfts_path_input')
            nftsPaths_output = request.POST.get('nfts_path_output')
            name = request.POST.get('name')
            symbol = request.POST.get('symbol')
            description = request.POST.get('description')
            sellerfee = request.POST.get('sellerfee')
            
            collectionname = request.POST.get('collectionname')
            collectionfamily = request.POST.get('collectionfamily')
            creatoraddress = request.POST.get('creatoraddress')
            creatorshare = request.POST.get('creatorshare')
            externalurl = request.POST.get('externalurl')
            totalnfts = request.POST.get('totalnfts')
            from_layers = request.POST.get('layers_as_folder')
            temps = {
                'name': name, 
                'symbol': symbol, 
                'description': description, 
                'seller_fee_basis_points': int(sellerfee) * 100, 
                'image': 'image.png', 
                'external_url': externalurl, 
                'attributes': [], 
                'collection': {
                        'name': collectionname, 
                        'family': collectionfamily
                    }, 
                'properties': {'files': [{'uri': 'image.png', 'type': 'image/png'}], 'category': 'image', 
                    'creators': [{
                        'address': creatoraddress, 
                        'share': int(creatorshare)
                        }]
                    }
            }

            # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            BASE_DIR = settings.MEDIA_ROOT

            temp_path = BASE_DIR + f'/{nftsPaths_input}/input/template.json'
            with open(temp_path, 'w') as f:
                json.dump(temps, f)

            
            zipPath = BASE_DIR + "/" + str(nftsPaths_output).replace("output", "") + 'resources.zip'
            folder_path = BASE_DIR + f'/{nftsPaths_output}'
            if from_layers is None:
                rarities_values = [[k, v] for k, v in request.POST.items() if k.startswith('rarity-')]
                print(rarities_values)

                for ren in rarities_values:
                    layer_name = ren[0].replace("rarity-", "").split("-*-")[0]
                    old_name = ren[0].replace("rarity-", "").split("-*-")[-1]
                    name_for_newname = old_name.split("-")[-1] #just for to make sure if there is already name have rarity remove that and add new rarity
                    new_file_name = str(round(int(ren[1]))) + "-" + name_for_newname
                    os.rename(BASE_DIR + f"/{nftsPaths_input}/assets/{layer_name}/" + old_name, BASE_DIR + f"/{nftsPaths_input}/assets/{layer_name}/" + new_file_name)

                directory_list = os.listdir(BASE_DIR + f"/{nftsPaths_input}/assets")
                c = 0
                for old_name in directory_list:
                    src = BASE_DIR + f"/{nftsPaths_input}/assets/{old_name}"
                    new_name = f"{c}-{old_name}"
                    dst = BASE_DIR + f"/{nftsPaths_input}/assets/{new_name}"
                    os.rename(src, dst)
                    c += 1

            
            task = asyncio.create_task(start_long_task([int(totalnfts), 0, 0], nftsPaths_input, nftsPaths_output, zipPath, folder_path))
            print(task)


            return JsonResponse({'valid': True, 'status': 'started', 'task_id': "Cronjob", 'output_dir': BASE_DIR + f'/{zipPath}'})
    return JsonResponse({'valid': False, 'status': 'Problem', 'task_id': ""})


def handle_uploaded_file(file):
    BASE_DIR = settings.MEDIA_ROOT
    print("-----------------")
    print(BASE_DIR)
    
    # UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')
    # if not os.path.exists(UPLOADS_DIR):
    #     os.makedirs(UPLOADS_DIR)

    folderName = f"{uuid.uuid4()}"
    # Create the uploads folder if it doesn't already exist
    containsDir = os.path.join(BASE_DIR, f"{folderName}")
    if not os.path.exists(containsDir):
        os.makedirs(containsDir)

    inputDir = os.path.join(BASE_DIR, f"{folderName}/input")
    if not os.path.exists(inputDir):
        os.makedirs(inputDir)
    
    assetsDir = os.path.join(BASE_DIR, f"{folderName}/input/assets")
    if not os.path.exists(assetsDir):
        os.makedirs(assetsDir)

    outputDir = os.path.join(BASE_DIR, f"{folderName}/output")
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    nfts_Dir = os.path.join(BASE_DIR, f"{folderName}/output/nfts")
    if not os.path.exists(nfts_Dir):
        os.makedirs(nfts_Dir)

    # Generate a unique filename for the uploaded file
    filename = f"{uuid.uuid4()}.{file.name.split('.')[-1]}"
    # Open the file with write binary mode
    with open(os.path.join(BASE_DIR, f"{folderName}/{filename}"), 'wb+') as destination:
        # Iterate over the chunks in the uploaded file and write them to the destination
        for chunk in file.chunks():
            destination.write(chunk)
    with zipfile.ZipFile(os.path.join(BASE_DIR, f"{folderName}/{filename}"), 'r') as zip_ref:
        # Extract all the files and folders in the zip file
        zip_ref.extractall(assetsDir)
        # Get the path to the directory containing the images

    image_dir = assetsDir
    # Create a list to hold the image files and their directories
    images = []

    # Walk through the directory tree, and add each image file and its directory to the images list
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.lower().endswith('.png') or file.lower().endswith('.jpg'):
                image_path = os.path.join(root, file)
                # print("---------------", image_path)
                images.append((image_path, os.path.relpath(root, image_dir)))

    # Pass the list of images to the template context

    data_dict = {}
    keys = []
    sample_image = []
    for d in images:
        if d[1] not in keys:
            keys.append(d[1])
            data_dict.update({d[1]: [f"uploads/{folderName}/input/assets/{d[1]}/" + d[0].split("\\")[-1]]})
            sample_image.append(d[0])
        else:
            data_dict[d[1]] += [f"uploads/{folderName}/input/assets/{d[1]}/" + d[0].split("\\")[-1]]
    
    keysList = list(data_dict.keys())

    first_img = True
    output_image = None
    for img in sample_image:
        im = Image.open(img)
        if first_img:
            output_image = im
            first_img = False
        else:
            output_image = Image.alpha_composite(output_image, im)
    if output_image:
        output_image.save(os.path.join(BASE_DIR, f"{folderName}/output/sample.png"), quality=95)



    data_list = []
    extected_nfts = 1
    for k in keysList:
        data_list.append({'layer': k, "images": data_dict[k], "rarity": round(100 / len(data_dict[k]))})
        extected_nfts = extected_nfts * len(data_dict[k])
    context = {
        'images': data_list,
        'sample': f"uploads/{folderName}/output/sample.png",
        'extected_nfts': extected_nfts,
        'collections_input':  f"{folderName}/input",
        'collections_ouput': f"{folderName}/output"
    }

    return context


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            # Save the uploaded file to a temporary file
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            print(file_path)
            data = handle_uploaded_file(file)
            # Delete the temporary file
            fs.delete(filename)
            return JsonResponse({'success': True, "context": data})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = UploadFileForm()
    return render(request, 'home.html', {'form': form})

# ipfs server upload code

async def upload_with_api(file_path):
    try:
        # Set the URL endpoint for NFT.Storage API
        url = "https://api.nft.storage/upload"

        # Set the API key for authentication
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweEZkNzE2NEU1MzAyNWQ1OTc5RWU5Rjg5YzRmOEE1NGQzQTM0ZDg2M0QiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY4MTkzMDIzNjg3NSwibmFtZSI6Im5mdGdlbmVyYXRvciJ9.KXjj8kDMKdTPZVVxvwoj51cu07KzggLOrxKBtTMWbl0"
        }

        # Set the NFT file to be uploaded
        file = open(file_path, "rb")

        # Make the HTTP POST request to upload the NFT
        response = requests.post(url, headers=headers, files={"file": file})

        # Print the response from the server

        res_obj = response.json()
        print(res_obj)
        if res_obj["ok"]:
            print(res_obj)
            print(res_obj["value"]["pin"]["cid"])
            print("Uploaded")
            return True, res_obj["value"]["pin"]["cid"]
        return False, None
    except Exception as e:
        print(e)
        return False, None
async def start_uploading_ipfs(zipPath, folder_path):
    files = os.listdir(path=folder_path)
    for file in files:
        if file.endswith(".png"):
            counter = 1
            while True:
                if counter > 6:
                    return False, " Failed Uploading"
                f_path = folder_path + f"/{file}"
                status, cid = await upload_with_api(f_path)
                if status:
                    json_file =str(file).replace(".png", ".json")
                    print(cid)
                    # Load the JSON file into a Python dictionary
                    with open(json_file, 'r') as f:
                        data = json.load(f)

                    # Update the URI value
                    data['properties']['files'][0]['uri'] = cid

                    # Save the updated dictionary back to the file
                    with open(json_file, 'w') as f:
                        json.dump(data, f, indent=4)
                    break
                else:
                    counter += 1
        await make_zip_of_resources(zipPath, folder_path)
    return True, "Uploaded success"


@csrf_exempt
def upload_on_ipfs_server(request):
    # try:
        folder = request.POST.get('resources')
        task_id =  request.POST.get('task_id')
        print(task_id, folder)
        task_id = task_id
        BASE_DIR = settings.MEDIA_ROOT

        nfts_path = BASE_DIR + f'/{folder}/output/images'
        file_path = "storedirectory/storeDirectory.mjs"
        full_path = settings.BASE_DIR / file_path
        # node_script_path = r'C:\Users\Administrator\Desktop\djangoNftGenerator\nftgen\storedirectory\storeDirectory.mjs'
        subprocess.Popen(['node', full_path, nfts_path, task_id])
        # subprocess.Popen(['node', node_script_path, nfts_path, task_id])
        print("bfore command")
        # subprocess.Popen(['python', 'C:\\Users\\Administrator\\Desktop\\nftGen_Arguement\\nftStart.py', '-z', "1", '-d', nfts_path, '-i', str(task_id)])
        # print("hellow ipfs server start")
        # subprocess.Popen(['node', 'C:\\Users\\Administrator\\Desktop\\storedirectory\\storeDirectory.mjs', "C:\\Users\\Administrator\\Desktop\\storedirectory\\imgs", task_id])
        print("hellow ipfs server start")
       


        
        return JsonResponse({'valid': True, 'msg': "uploading on ipfs server."})
    # except Exception as e:
    #     print(e)
    #     return JsonResponse({"valid": False, 'error': f'error in iPFS server upload'})


# @csrf_exempt
# def get_task_status(request):
#     try:
#         dir = request.POST.get('output_path')
#         task_id = request.POST.get('task_id')
#         print("hhhurayyyyyyy", task_id)
#         if "uploads" in dir:
#             dir = dir.replace("uploads", "")
#         BASE_DIR = settings.MEDIA_ROOT
#         folder_path = BASE_DIR + f'/{dir}/nfts/public_mint_assets'
#         folder_path = str(Path(folder_path))

#         # get task
#         record_to_update = Task.objects.get(id=task_id)
#         status = ""
#         msg = ""
#         is_valid = False
#         if record_to_update:
#             is_valid = True
#             status = record_to_update.status
#             msg = record_to_update.message
#         if os.path.isdir(folder_path):
#             is_valid = True
#             files = os.listdir(path=folder_path)
#             images_counter = 0
#             for f in files:
#                 if f.endswith(".png"):
#                     images_counter += 1
#             return JsonResponse({'valid': is_valid, "count": images_counter, "status": status, "msg": msg})
#         else:
#             return JsonResponse({'valid': is_valid, "dir": folder_path, "status": status, "msg": msg, "count": 0})
#     except:
#         return JsonResponse({"valid": False, 'error': f'Task with ID does not exist.'})






















def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
    else:
        form = LogInForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('home')
# def run_command(request):
#     import subprocess
# from django.shortcuts import render


# def run_command(request):
#     if request.method == 'POST':
#         # Execute the command using subprocess module
#         result = subprocess.run(['python', 'C:\\Users\\Administrator\\Desktop\\nftGen_Arguement\\nftStart.py', '-p', '1000', '-d', 'C:\\Users\\Administrator\\Desktop\\nftGen_Arguement\\1'], capture_output=True, text=True)
#         if result.returncode != 0:
#             # There was an error executing the command
#             print(result.stderr)  # Print the error message
#         # Get the command output
#         output = result.stdout
        
#         # Pass the output to the template for display
#         return render(request, 'output.html', {'output': output})
    
#     return render(request, 'index.html')
# async def run_ipfs_upload(folder_name):
#     # Run the IPFS upload code asynchronously
#     process = await asyncio.create_subprocess_exec(
#         'node', 'storeDirectory.mjs', folder_name
#     )
#     await process.wait()  # Wait for the subprocess to complete

# def upload_ipfs_server(request):
#     if request.method == 'POST':
#         # Execute the command using subprocess module
#         # subprocess.Popen(['python', 'C:\\Users\\Administrator\\Desktop\\nftGen_Arguement\\nftStart.py', '-p', '20', '-d', 'C:\\Users\\Administrator\\Desktop\\nftGen_Arguement\\1'])
#         folderName = f"{uuid.uuid4()}"

#         new_task_object = Task(status="to uploading", message="Processing ...", folder_name= f"{folderName}")
#         new_task_object.save() 

        
#         task_id = new_task_object.id
#         task = Task.objects.get(id=task_id)

#         # Retrieve the folder name from the task object
#         folder_name = task.folder_name
#         # print(folder_name)
#         try:
#             # subprocess.Popen(['node', 'C:\\Users\\Administrator\\Desktop\\storedirectory\\storeDirectory.mjs', 'C:\\Users\\Administrator\\Desktop\\storedirectory\\imgs'])
#             subprocess.Popen(['node', 'C:\\Users\\Administrator\\Desktop\\storedirectory\\storeDirectory.mjs', "C:\\Users\\Administrator\\Desktop\\storedirectory\\imgs", task_id])

#             return HttpResponse("Successfully uploaded")
        
#         except Exception as e:
#             return HttpResponse("Error: " + str(e))
        
        

#     # return render(request, 'index.html')
#     return HttpResponse("GET request received. Render the upload form here.")



def run_command(request):
    if request.method == 'POST':
        # Execute the command using subprocess module
        # subprocess.Popen(['python', 'C:\\Users\\Administrator\\Desktop\\nftGen_Arguement\\nftStart.py', '-p', '20', '-d', 'C:\\Users\\Administrator\\Desktop\\nftGen_Arguement\\1'])
        folderName = f"{uuid.uuid4()}"

        new_task_object = Task(status="to uploading", message="Processing ...", folder_name= f"{folderName}")
        new_task_object.save() 

        
        task_id = new_task_object.id
        task = Task.objects.get(id=task_id)

        # Retrieve the folder name from the task object
        folder_name = task.folder_name
        # print(folder_name)
        try:
            # subprocess.Popen(['node', 'C:\\Users\\Administrator\\Desktop\\storedirectory\\storeDirectory.mjs', 'C:\\Users\\Administrator\\Desktop\\storedirectory\\imgs'])
            subprocess.Popen(['node', r'C:\Users\Administrator\Desktop\djangoNftGenerator\nftgen\storedirectory\storeDirectory.mjs', "C:\\Users\\Administrator\\Desktop\\storedirectory\\imgs", task_id])

            return HttpResponse("Successfully uploaded")
        
        except Exception as e:
            return HttpResponse("Error: " + str(e))
        
        

    return render(request, 'index.html')
