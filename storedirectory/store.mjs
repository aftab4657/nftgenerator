import fs from 'fs';
import { MongoClient } from 'mongodb';
import { NFTStorage, File } from 'nft.storage';
import { getFilesFromPath } from 'web3.storage';
import path from 'path';

const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweEZkNzE2NEU1MzAyNWQ1OTc5RWU5Rjg5YzRmOEE1NGQzQTM0ZDg2M0QiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY4MTkzMDIzNjg3NSwibmFtZSI6Im5mdGdlbmVyYXRvciJ9.KXjj8kDMKdTPZVVxvwoj51cu07KzggLOrxKBtTMWbl0';
const mongoURI = 'mongodb+srv://aftab4657:Y7mPlvkAL54JSGta@nftgentasks.as4m7os.mongodb.net/?retryWrites=true&w=majority'; // Replace with your MongoDB connection string
const dbName = 'nftgeneration';
const collectionName = 'userRegistration_task';

async function main() {
  if (process.argv.length !== 4) {
    console.error(`usage: node ${path.basename(process.argv[1])} <directoryPath> <id>`);
    return;
  }

  const directoryPath = process.argv[2];
  const id = process.argv[3];
  const files = await getFilesFromPath(directoryPath, {
    pathPrefix: path.resolve(directoryPath),
    hidden: true,
  });

  const storage = new NFTStorage({ token });

  console.log(`Storing file(s) from ${directoryPath}`);
  try {
    const client = await MongoClient.connect(mongoURI);
    const db = client.db(dbName);
    const collection = db.collection(collectionName);

    const cid = await storage.storeDirectory(files, { id });
    console.log({ cid });

    const status = await storage.status(cid);
    console.log('Upload status:', status);

    console.log('Files uploaded successfully!');

    // Update the MongoDB document with the uploaded file information
    const successStatus = 'completed';
    const successMessage = 'File uploaded successfully';
    const successFilter = { id };
    const successDocument = { id, status: successStatus, message: successMessage, folder_name: directoryPath };
    const successUpdateResult = await collection.replaceOne(successFilter, successDocument, { upsert: true });
    console.log('Document saved in the database:', successUpdateResult);

    client.close();
  } catch (error) {
    console.error('Upload error:', error.message);

    // Update the MongoDB document with the error message
    const errorStatus = 'uploadError';
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
    const errorFilter = { id };
    const errorDocument = { id, status: errorStatus, message: errorMessage, folder_name: directoryPath };
    const errorUpdateResult = await collection.replaceOne(errorFilter, errorDocument, { upsert: true });
    console.log('Error document saved in the database:', errorUpdateResult);
  }
}

main();