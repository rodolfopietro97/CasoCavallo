import { CummareClient } from './peers/CummareClient'

import { readFileSync } from 'fs';

import { RedisHandler } from './redis_handler/RedisHandler'

/**
 * CasoCavallo P2P Server.
 * 
 * This Server is a CummareClient that subscribe
 * every seconds to "random_requests" topic.
 * 
 * Wen a client publish a request for "random_requests" topic
 * it handle request and give a number (publish) in "random_responses".
 * 
 * After the client fetch the response of his request in "random_responses"
 */
function mainServer() {
  // Require NodeRSA module to encrypt and decrypt requests
  const NodeRSA = require('node-rsa');

  // Set configuration from json file
  const configuration = JSON.parse(
    readFileSync('./Config.json', 'utf-8')
  );

  // Init Redis client
  const redisHandler: RedisHandler = new RedisHandler(configuration.redis);

  // Random requests
  var random_responses: Array<string> = []

  // Init Current numbers (undefined for each queue)
  var currents: object = {}
  configuration.CasoCavalloQueues.forEach((queue) => {
    currents[queue.name] = undefined;
  });

  

  // Update current numbers
  setInterval(async () => {
    // Fetch for each queue
    configuration.CasoCavalloQueues.forEach(async (queue) => {
      
      // Set current
      currents[queue.name] = await redisHandler.getCurrentRandom(`current_${queue.name}`)
    });
  }, 100)

  /*
   * Fetch form "random_requests" topic every configuration.subscribeTimeMilliseconds.
  When a request is fetched a response is published on "random_responses" topic
   */
  setInterval(() => {

    // For each server binded send a message
    configuration.cummareServers.forEach(cummareServer => {
      // Create a client
      var cummareClient = new CummareClient(cummareServer)

      // Subscribe random requests
      let call = cummareClient.subscribeTopic(configuration.requestsTopic);
      call.on('data', async function (response) {    
        // Resolve a random request and pushes in random responses
        const requestObject = JSON.parse(response.getMessage());

        // Get resolved requests ids
        let resolvedRequestsIds = await redisHandler.getTopic("resolved_ids")
        console.log(resolvedRequestsIds)

        // Not resolved yet
        if (!resolvedRequestsIds.includes(requestObject.request_id)) {
          redisHandler.setList("resolved_ids", String(requestObject.request_id))

          // Fetch publik key from request
          const publicKey = new NodeRSA(requestObject.public_key, 'pkcs1-public-pem');

          // Create response to forward in random_responses topic
          let responseObject = requestObject
          responseObject.data = publicKey.encrypt(currents[requestObject.queue], 'base64')

          // Publish in "random_requests"
          cummareClient.publishMessage(configuration.responsesTopic, JSON.stringify(responseObject), (ack) => {
            if (ack)
              console.log(`${requestObject.queue} resolved`)
          })
        }

      });
      call.on('end', function () {
        console.log("Fetched all random requests")
      });
      console.clear()
    });
  }, 1000)

}

mainServer();