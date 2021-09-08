/**
 * Simple "server" instance
 */

import { createNode } from "./nodes";


const topic = 'news'


const main = async () => {
    // Init main arguments
    let mainArguments : Array<String> = process.argv

    // We need to pass listen mode or not (Client or Server)
    console.assert(mainArguments.length == 3)

    // Set listen mode (we are server that subscribe)
    let listenMode : boolean = mainArguments[2] == '-s'

    // // Set ports on listen
    // let numberOfPorts = 10
    // let ports = Array.from(new Array(numberOfPorts), (x, i) => i)

    // let listenNodesTCP = ports.map((port : number) => {
    //     return `/ip4/0.0.0.0/tcp/${4005 + port}`
    // })
    // let listenNodesWS = ports.map((port : number) => {
    //     return `/ip4/127.0.0.1/tcp/${4005 + port + numberOfPorts}/ws`
    // })
    let allAddresses =  [
                '/ip4/0.0.0.0/tcp/0',
                '/ip4/0.0.0.0/tcp/0/ws'
            ]
            // ].concat(listenNodesTCP).concat(listenNodesWS)


    // Init node by passing listen addresses
    let p2pNode = await createNode(
        allAddresses
    );

    // Start node
    await p2pNode.start();

    // Listen on pubsub events
    if(listenMode){
        p2pNode.pubsub.on('fruit', (data) => {
            console.log(`Received ${data.data} From ${data.receivedFrom}`)
        })
        p2pNode.pubsub.subscribe('fruit')
    }

    // Publish stuffs
    if(!listenMode)
        setInterval(()=>{
            p2pNode.pubsub.publish('fruit', 'banana')
        }, 200) 

    // Starting log
    console.log('listening on addresses:')
    p2pNode.multiaddrs.forEach(addr => {
        console.log(`${addr.toString()}/p2p/${p2pNode.peerId.toB58String()}`)
    })

    // When connection is established
    p2pNode.connectionManager.on('peer:connect', async (connection) => {
        // console.log('Connection established to:', connection.remotePeer.toB58String())	// Emitted when a new connection has been created
    })

    // When a new peer is discovered
    p2pNode.on('peer:discovery', async (peerId) => {
        // console.log('Discovered:', peerId.toB58String())
    })
}

main();

// const mainForBrowser = async () => {
//     // Init node
//     let p2pNode = await createWebNode(
//         [
//             '/ip4/127.0.0.1/tcp/8000/ws',
//             '/dns4/wrtc-star1.par.dwebops.pub/tcp/443/wss/p2p-webrtc-star'
//         ]
//     );

//     // Start node
//     await p2pNode.start();

//     const advertiseAddrs = p2pNode.multiaddrs
//     console.log('libp2p is advertising the following addresses: ', advertiseAddrs)

//     // // Listen on pubsub events
//     // p2pNode.pubsub.on('fruit', (data) => {
//     //     console.log(data)
//     // })
//     // p2pNode.pubsub.subscribe('fruit')

//     // // Publish stuffs
//     // p2pNode.pubsub.publish('fruit', new TextEncoder().encode('banana'))

//     // // Starting log
//     // console.log('listening on addresses:')
//     // p2pNode.multiaddrs.forEach(addr => {
//     //     console.log(`${addr.toString()}/p2p/${p2pNode.peerId.toB58String()}`)
//     // })

//     // // When connection is established
//     // p2pNode.connectionManager.on('peer:connect', (connection) => {
//     //     console.log('Connection established to:', connection.remotePeer.toB58String())	// Emitted when a new connection has been created
//     // })

//     // // When a new peer is discovered
//     // p2pNode.on('peer:discovery', (peerId) => {
//     //     console.log('Discovered:', peerId.toB58String())
//     // })
// }

// mainForBrowser();