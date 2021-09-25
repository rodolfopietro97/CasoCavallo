import { CummareClient } from './peers/CummareClient'

import { readFileSync } from 'fs';

/**
 * Simple client.
 * 
 * It sends message in "random_requests" topic
 * and wait a response in "random_responses"
 */
function mainClient() {
  // Require NodeRSA module to encrypt and decrypt requests
  const NodeRSA = require('node-rsa');

  // Set configuration from json file
  const configuration = JSON.parse(
    readFileSync('./Config.json', 'utf-8')
  );

  // For each server binded send a message
  configuration.cummareServers.forEach(cummareServer => {

    // Create a client
    var cummareClient = new CummareClient(cummareServer)

    // Create public key to use for encrypt random numbers
    const myKey = new NodeRSA({b: 512});

    // Subscribe random requests
    let randomRequest = {
      // Queue
      queue: "random_numbers_between_0_1",
      
      // User public key
      public_key: myKey.exportKey("pkcs1-public-pem"),

      // Reques id
      request_id: 1010101,
    }

    // Publish 1 message
    cummareClient.publishMessage(configuration.requestsTopic, JSON.stringify(randomRequest), (ack) => {
      if (ack) {
        console.log(`${cummareServer} has received message`)
      }
      else
        console.log(`${cummareServer} has NOT received message`)
    })

    // Subscribe and fetch every second
    setInterval(() => {
      // Subscribe random responses
      let call = cummareClient.subscribeTopic(configuration.responsesTopic);

      call.on('data', function (response) {
        const responseObject = JSON.parse(response.getMessage());

        // My message!
        if(randomRequest.request_id == responseObject.request_id)
          console.log(myKey.decrypt(responseObject.data, 'json'))

      });
      call.on('end', function () {
      });
    }, 1000)
  });

}

mainClient();