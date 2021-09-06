/**
 * Simple "server" instance
 */

import { createNode } from "./nodes";
const { fromString: uint8ArrayFromString } = require('uint8arrays/from-string')
const { toString: uint8ArrayToString } = require('uint8arrays/to-string')


const topic = 'news'


const main = async () => {
    // Init node
    let p2pNode = await createNode(
        [
            '/ip4/0.0.0.0/tcp/33055'
        ]
    );

    // Start node
    await p2pNode.start();

    // Listen on pubsub events
    p2pNode.pubsub.on('fruit', (data) => {
        console.log(data)
    })
    p2pNode.pubsub.subscribe('fruit')

    // Starting log
    console.log('listening on addresses:')
    p2pNode.multiaddrs.forEach(addr => {
        console.log(`${addr.toString()}/p2p/${p2pNode.peerId.toB58String()}`)
    })

    // When connection is established
    p2pNode.connectionManager.on('peer:connect', (connection) => {
        console.log('Connection established to:', connection.remotePeer.toB58String())	// Emitted when a new connection has been created
    })

    // When a new peer is discovered
    p2pNode.on('peer:discovery', (peerId) => {
        console.log('Discovered:', peerId.toB58String())
    })
}

main();