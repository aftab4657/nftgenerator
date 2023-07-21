import fs from 'fs';
import { MongoClient } from 'mongodb';
import { NFTStorage, File } from 'nft.storage';
import { getFilesFromPath } from 'web3.storage';
import path from 'path';
import axios from 'axios';
import cheerio from 'cheerio';
import { exit } from 'process';

const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweEZkNzE2NEU1MzAyNWQ1OTc5RWU5Rjg5YzRmOEE1NGQzQTM0ZDg2M0QiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY4MTkzMDIzNjg3NSwibmFtZSI6Im5mdGdlbmVyYXRvciJ9.KXjj8kDMKdTPZVVxvwoj51cu07KzggLOrxKBtTMWbl0';
const mongoURI = 'mongodb+srv://aftab4657:Y7mPlvkAL54JSGta@nftgentasks.as4m7os.mongodb.net/?retryWrites=true&w=majority'; // Replace with your MongoDB connection string

// async function getFilesInCID(cid) {
//   console.log("i m ing");
//   try {
//     var headers = {
//       Authorization: `Bearer ${token}`, // Replace with your NFT.Storage API key
//     }
//     console.log("headers");
//     console.log(headers);
//     const response = await axios.get(`https://api.nft.storage/${cid}`, {
//     headers: headers,
//     });
    
//     // The list of files can be accessed through the `files` property of the response data
//     const files = response.data.value.files;
//     console.log(files);
//     console.log("pta nih")
//   } catch (error) {
//     console.error('Error retrieving files from CID:', error.message);
//   }
// }

// // Replace 'YOUR_CID' with the actual CID you want to retrieve files from
// await getFilesInCID('bafybeicqqfdrd4nst4iuagaxk6l3fi35jcfpeobnlsrek7rsi4crqh7aqy');

// exit();


async function get_image_cid(partial, cids) {
  try {
    for (let element of cids) {
      if (element.includes(partial)) {
        const img_cid = element.split("ipfs/").pop().split("?")[0];
        return img_cid;
      }
    }
    return null;
  } catch (error) {
    console.error("Error in get_image_cid:", error);
    throw error; // Rethrow the error to be handled by the caller
  }
}


async function upload_meta_data(minthoreMetadataDir, cide_nfts, id){
  console.log("metadata 1");
  const files = await getFilesFromPath(minthoreMetadataDir, {
    pathPrefix: path.resolve(minthoreMetadataDir),
    hidden: true,
  });
  console.log("metadata 1");
  const storage = new NFTStorage({ token });
  const cid_meta = await storage.storeDirectory(files, { id });
  console.log("metadata 1");

  const status = await storage.status(cid_meta);
  console.log('Upload status:', status);
  console.log("metadata 1");

  console.log('Files uploaded successfully!');
  console.log("metadata 1");

  const newDocument = {
    id: id,
    message : "NFTs uploaded successfully",
    status: 'uploaded', // Set initial status to 'Upload'
    folder_name : id,
    cid_nfts: cide_nfts,
    cid_metadata: cid_meta
  };

  const filter = { id: id };

  // newDocument.status = 'uploaded'; // Update the status to 'Uploaded'
  // newDocument.message = 'File uploaded successfully';
  // newDocument.folder_name = minthoreMetadataDir.split("upload").pop().split("output")[0]; 
  // newDocument.cid_nfts = cide_nfts;
  // newDocument.cid_metadata = cid_meta
  console.log("metadata 1");
  const client = new MongoClient(mongoURI);
  await client.connect();

  const databaseName = 'nftgen2';
  const collectionName = 'userRegistration_task';

  const database = client.db(databaseName);
  const collection = database.collection(collectionName);

  const finalUpdateResult = await collection.replaceOne(filter, newDocument);
  console.log(' document updated:',finalUpdateResult);
  console.log("metadata 1");

}

async function main() {
  if (process.argv.length !== 4) {
    console.error(`usage:  ${process.argv[0]} ${process.argv[1]} <directoryPath> <id>`);
    return;
  }

  const directoryPath = process.argv[2];
  const id = parseInt(process.argv[3]);
  console.log(id);
  console.log("check above id");
  const files = await getFilesFromPath(directoryPath, {
    pathPrefix: path.resolve(directoryPath),
    hidden: true,
  });

  const client = new MongoClient(mongoURI);
  try {
    await client.connect();
    console.log('Connected to MongoDB');

    const databaseName = 'nftgen2';
    const collectionName = 'userRegistration_task';

    const database = client.db(databaseName);
    const collection = database.collection(collectionName);

    const newDocument = {
      id: id,
      message : "uploading nfts uploading",
      status: 'uploading', // Set initial status to 'Uploading'
      folder_name :id,
      cid_nfts: "",
      cid_metadata: ""
    };

    const filter = { id: id };
    const updateResult = await collection.replaceOne(filter, newDocument, { upsert: true });
    console.log('Document updated:', updateResult);

    const storage = new NFTStorage({ token });

    console.log(`Storing file(s) from ${directoryPath}`);



    const cid = await storage.storeDirectory(files, { id });
    console.log({ cid });




    // code for meta_data

    // const axios = require('axios');
    // const cheerio = require('cheerio');
    
    // Define the directory paths
    const minthoreMetadataDir = directoryPath.replace("images", "minthor_metadata");
    const sourceFolder = directoryPath.replace("images", "jsons");
    
    // Create the destination folder if it doesn't exist
    if (!fs.existsSync(minthoreMetadataDir)) {
      fs.mkdirSync(minthoreMetadataDir, { recursive: true });
    }
    
    // Remove all files in the minthore_metadata_dir
    fs.readdirSync(minthoreMetadataDir).forEach((file) => {
      const filePath = path.join(minthoreMetadataDir, file);
      fs.unlinkSync(filePath);
    });
    
    // Get the list of JSON files in the source folder
    const jsonFiles = fs.readdirSync(sourceFolder).filter(file => file.toLowerCase().endsWith('.json'));
    const filesCount = jsonFiles.length;
    
    // Make a GET request to the URL
    const url = `https://${cid}.ipfs.nftstorage.link/`;
    console.log(url);
    var error_in_getting_cids = false;
    axios.get(url)
      .then((res) => {
        console.log("diego00000000");
        const $ = cheerio.load(res.data);
        const links = $('a.ipfs-hash');
        var cids = {};
        links.each((index, element) => {
          console.log($(element).attr('href').split("?filename").pop());
          cids[$(element).attr('href').split("?filename").pop()] = $(element).attr('href').split("ipfs/").pop().split("?")[0];
          // cids.push($(element).attr('href'));
        });
        console.log(cids);

        console.log("ffffffffffffffffffffffffffffffffffffff");
        
       
    

    
        if (Object.keys(cids).length !== filesCount) {
          throw new Error('Invalid CID');
        }
        console.log("fffffffffffffffffffffffffffffffffffff1f2");
        
        // Process each JSON file
        for (let i = 0; i < jsonFiles.length; i++) {
          const js = jsonFiles[i];
          const jsonFilePath = path.join(sourceFolder, js);
          const data = JSON.parse(fs.readFileSync(jsonFilePath, 'utf8'));
        console.log("ffffffffffffffffffffffffffffffffffffff3");
          
          const new_data = {
            name: data.name,
          };
        console.log("ffffffffffffffffffffffffffffffffffffff4");
          
          data.attributes.forEach((atr) => {
            new_data[atr.trait_type] = atr.value;
          });
        console.log(cids["=0.png"]);
        console.log("ffffffffffffffffffffffffffffffffffffff5");

          var my_img = "=" + String(js).replace(".json", ".png");
          console.log(js, my_img);

          var find_cid = cids[my_img];
          console.log(js, my_img);


          
          console.log(js, "my_img");

          if (find_cid == null) {
            throw new Error("Invalid CID");
          }
        console.log("ffffffffffffffffffffffffffffffffffffff6");

          new_data.image = `ipfs://${find_cid}`;
          console.log("ffffffffffffffffffffffffffffffffffffff7");
    
          // Save the updated dictionary back to the file
          const newFilePath = path.join(minthoreMetadataDir, js);
        console.log("ffffffffffffffffffffffffffffffffffffff8");

          fs.writeFileSync(newFilePath, JSON.stringify(new_data, null, 4));
        console.log("ffffffffffffffffffffffffffffffffffffff9");
        }

        upload_meta_data(minthoreMetadataDir, cid, id);



      })
      .catch((error) => {
        error_in_getting_cids = true;
        console.error(error);
        throw new Error("Error while getting CID");

      });
    

      if (error_in_getting_cids){
        throw new Error("Error while getting CID");
      }
    // end code for meta_data






  } catch (err) {
    console.error('Error:', err);
    // Handle the upload error by updating the document with the error message
    const errorDocument = {
      status: 'error',
      message: err.message || 'An upload error occurred',
      folder_name : id,
      cid_nfts :"",
      cid_metadata : ""

    };
    const errorUpdateResult = await collection.replaceOne(filter, { $set: errorDocument });
    console.log('Document updated with upload error:', errorUpdateResult);
  } finally {
    client.close();
  }
}

main().catch((err) => {
  console.error('Unhandled promise rejection:', err);
});
