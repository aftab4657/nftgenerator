from includes.nft_creator import NftCreator
from includes.utils import Args
from includes.rarity_calculator import RarityCalculator
from datetime import datetime
import pymongo, zipfile, os, shutil, subprocess
from pymongo import MongoClient

cluster = pymongo.MongoClient("mongodb+srv://aftab4657:Y7mPlvkAL54JSGta@nftgentasks.as4m7os.mongodb.net/?retryWrites=true&w=majority")
db = cluster["nftgen2"]
collection = db["userRegistration_task"]

def copy_images_json():
        source_folder = dir_path + f"/output/nfts/public_mint_assets"
        destination_json = dir_path + f"/output/jsons/"
        destination_images = dir_path + f"/output/images"
        # Create the destination folder if it doesn't exist
        if not os.path.exists(destination_json):
            os.makedirs(destination_json)

        if not os.path.exists(destination_images):
            os.makedirs(destination_images)

        for root, dirs, files in os.walk(destination_images, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir in dirs:
                d_path = os.path.join(root, dir)
                os.rmdir(d_path)
        for root, dirs, files in os.walk(destination_json, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir in dirs:
                d_path = os.path.join(root, dir)
                os.rmdir(d_path)

        # Get a list of files in the source folder
        files = os.listdir(source_folder)

        # Filter only the image files
        image_files = [file for file in files if file.lower().endswith(('.png'))]
        json_files = [file for file in files if file.lower().endswith(('.json'))]

        # Copy each image file to the destination folder
        for file in image_files:
            source_path = os.path.join(source_folder, file)
            destination_path = os.path.join(destination_images, file)
            shutil.copyfile(source_path, destination_path)
            # print(f"Copied: {source_path} to {destination_path}")

        for file in json_files:
            source_path = os.path.join(source_folder, file)
            destination_path = os.path.join(destination_json, file)
            shutil.copyfile(source_path, destination_path)
            # print(f"Copied: {source_path} to {destination_path}")
try:
    folderPaths = ['public_mint_assets', 'whitelist_mint_assets', 'giveaway_assets']
    numberNFTs, testRarities, randomizedOutput, dir_path, task_id,  script_uploading = Args([0 for i in folderPaths], False, False, None, None, None)
    unique_folder_name = str(dir_path).replace("\\", "/").split("/")[-3]
    ww = ""
    if script_uploading:
        print("Uploading nftssssss")
        node_script_path = r'C:\Users\Administrator\Desktop\nftGen_Arguement\storeDirectory.mjs'
        # status = "uploading"
        # message = "NFTs uploading python start node"
        # nft_cid = ""
        # nft_metadata = ""

        # filter = {"id": task_id}
        # print(filter)
        # new_document = {"id": task_id, "status": status, "message": message, "folder_name": unique_folder_name, "cid_nfts": nft_cid, "cid_metadata":nft_metadata}

        # error_result = collection.replace_one(filter, new_document, upsert=True)

        # if error_result.modified_count > 0:
        #     print("status updated successfully.")
        # else:
        #     print("No document matched the filter for replacement.")
        print(dir_path, task_id)
        ww = " before"
        subprocess.Popen([r'C:\Program Files\nodejs\node.exe', node_script_path, dir_path, str(task_id)])
        ww = "after"
        print("uploading end")
    else:
        status = "running"
        message = "NFTs Generatnig"
        nft_cid = ""
        nft_metadata = ""

        filter = {"id": task_id}
        print(filter)
        new_document = {"id": task_id, "status": status, "message": message, "folder_name": unique_folder_name, "cid_nfts": nft_cid, "cid_metadata":nft_metadata}

        error_result = collection.replace_one(filter, new_document, upsert=True)

        if error_result.modified_count > 0:
            print("status updated successfully.")
        else:
            print("No document matched the filter for replacement.")


        print(dir_path)

        colors = {
            'Legendary': '#ff8000',
            'Epic': '#a335ee',
            'Rare': '#0070dd',
            'Uncommon': '#6bca06',
            'Common': '#a0a0a0'
        }

        rarities = list(colors.keys())

        percentages = [3.0, 6.5, 10.0, 17.0]

        nfts = NftCreator(numberNFTs, folderPaths, testRarities, randomizedOutput, dir_path)

        print()
        print('-------------------------------------------------------------------------')
        print()

        rarities = RarityCalculator(nfts, colors, rarities, percentages, dir_path)
        zipPath = dir_path + '/resources.zip'
        with zipfile.ZipFile(zipPath, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(dir_path + "/output"):
                rel_path = os.path.relpath(root, dir_path + "/output")
                for file in files:
                    print(file)
                    # Add each file to the zip archive
                    zip_file.write(os.path.join(root, file), arcname=os.path.join(rel_path, file))

                for folder in dirs:
                    print(folder)
                    # Add each folder to the zip archive
                    zip_file.write(os.path.join(root, folder), arcname=os.path.join(rel_path, folder))
        copy_images_json()
        status = "completed"
        message = "NFTs generated successfully"
        nft_cid = ""
        nft_metadata = ""

        filter = {"id": task_id}
        print(filter)
        new_document = {"id": task_id, "status": status, "message": message, "folder_name": unique_folder_name, "cid_nfts": nft_cid, "cid_metadata":nft_metadata}

        error_result = collection.replace_one(filter, new_document)

        if error_result.modified_count > 0:
            print("status updated successfully.")
        else:
            print("No document matched the filter for replacement.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
    # Handle the error
    error_status = "error"
    nft_cid = ""
    nft_metadata = ""
    message = f"python {ww}: {str(e)}"

    error_filter = {"id": task_id}

    new_document = {"id": task_id, "status": error_status, "message": message, "folder_name": unique_folder_name, "cid_nfts":nft_cid, "cid_metadata": nft_metadata}

    error_result = collection.replace_one(error_filter, new_document, upsert=True)

    if error_result.modified_count > 0:
        print("status updated successfully.")
    else:
        print("No document matched the filter for replacement.")
