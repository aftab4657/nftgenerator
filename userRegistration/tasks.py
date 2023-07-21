from celery import shared_task

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from nftgen import settings
import time
from .includes.nft_creator import NftCreator
from .includes.utils import Args
from .includes.rarity_calculator import RarityCalculator
import zipfile
import os
from .models import Task

@shared_task

def generate_nft(number_listnf, testRarities=False, randomizedOutput=False, collection_input="", collection_output="",zipPath="", folder_path="",task_id=""):
        print("w" * 100)
        print(collection_input)
        print(collection_output)
        print("w" * 100)
    
    

    # try:
        #Folders names that will store ur uniques nfts, u can add more!
        folderPaths = ['public_mint_assets','whitelist_mint_assets','giveaway_assets']
        # numberNFTs, testRarities, randomizedOutput = Args([0 for i in folderPaths], False, False)

        #Rarities categories and color associated (can be modified adding/deleting) DONT USE (#000000)
        colors = {
            'Legendary':'#ff8000',
            'Epic':'#a335ee',
            'Rare': '#0070dd',
            'Uncommon': '#6bca06',
            'Common': '#a0a0a0'
        }

        #Rarities that will be stored on ur json rarity displayer, this will have the same lenght as len(colors)
        rarities = list(colors.keys())

        #Percentage cut value to an item be considered with an rarity
        #(legendary_percentage, epic_percentage,...,uncommon_percentage). Has to be the len(rarities)-1
        percentages = [3.0, 6.5, 10.0, 17.0] 
        #Any item with less than 3% will be considered as LEGENDARY, any item with less than 17.0 will be considered as UNCOMMON 
        #and any item with greater-equal than 17 will be considered as COMMON


        nfts = NftCreator(number_listnf, folderPaths, testRarities, randomizedOutput, collection_input, collection_output)

        print()
        print('-------------------------------------------------------------------------')
        print()


        rarities = RarityCalculator(nfts, colors, rarities, percentages, collection_output)
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
        record_to_update = Task.objects.get(id=task_id)
            # Update the fields of the record
        record_to_update.status = "completed"
        record_to_update.message = "Task completed successfully"
            # Save the updated record back to the database
        record_to_update.save()
            # await sync_to_async(record_to_update.save)()
        return True, "Success"
        
    # except Exception as e:
    #     print("oh God")
    #     print(e)
    #     print("oh God...")
    #     # logger.error('An error occurred: %s', e, exc_info=True)
    #     record_to_update = Task.objects.get(id=task_id)
    #         # Update the fields of the record
    #     record_to_update.status = "error"
    #     record_to_update.message = str(e)
    #         # Save the updated record back to the database
    #     record_to_update.save()
    #         # await sync_to_async(record_to_update.save)()
    #     return False, str(e)
        
       





# @shared_task(bind=True)
# def test(self):
#     for i in range(10):
#         print(i)
#     return "Done"

@shared_task(bind=True)
def send_email_func(self):
    users = get_user_model().objects.all()
    for user in users:
        subject="Hello celery"
        message="Hello world"
        to_email= user.email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True
        )
    return "Task successfull"


@shared_task
def task_one(x):
    print(f" hello {x}")
    # time.sleep(30)
    print(f"hello world {x}")
    return "Task completed"

@shared_task
def task_two():
    return "Task two completed"

@shared_task
def task_three():
    return "Task three completed"
@shared_task
def processFiles(file_path):
     time.sleep(20)
     return "File processing  completed"
