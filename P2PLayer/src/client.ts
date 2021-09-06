/** 
 * Simple "client" instance
 */

import { createNode } from "./nodes";
const { fromString: uint8ArrayFromString } = require('uint8arrays/from-string')
const { toString: uint8ArrayToString } = require('uint8arrays/to-string')

const topic = 'news'


const main = async () => {
    // Init node
    let p2pNode = await createNode(
        [
            '/ip4/127.0.0.1/tcp/33055'
        ]
    );

    // Start node
    await p2pNode.start();

    console.log('listening on addresses:')

    p2pNode.multiaddrs.forEach(addr => {
        console.log(`${addr.toString()}/p2p/${p2pNode.peerId.toB58String()}`)
    })

    p2pNode.connectionManager.on('peer:connect', (connection) => {
        console.log('Connection established to:', connection.remotePeer.toB58String())	// Emitted when a new connection has been created
    })

    p2pNode.on('peer:discovery', (peerId) => {
        // No need to dial, autoDial is on
        console.log('Discovered:', peerId.toB58String())
    })

    // setInterval(() => {
        p2pNode.pubsub.publish(topic, uint8ArrayFromString('Bird bird bird, bird is the word!'))
    // }, 1000)


    // await p2pNode.stop()
}

main();