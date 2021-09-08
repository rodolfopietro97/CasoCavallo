const Libp2p = require('libp2p')
// @ts-ignore - no types
const TCP = require('libp2p-tcp')
const { NOISE } = require('libp2p-noise')
// @ts-ignore - no types
const MPLEX = require('libp2p-mplex')
const Gossipsub = require('libp2p-gossipsub')
const Bootstrap = require('libp2p-bootstrap')
const PubsubPeerDiscovery = require('libp2p-pubsub-peer-discovery')
const KadDHT = require('libp2p-kad-dht')
// @ts-ignore - no types
const WS = require('libp2p-websockets')
// @ts-ignore - no types
const MulticastDNS = require('libp2p-mdns')
const os = require('os')

/**
 * Generate a P2P node
 * 
 * @param ipAddresses Ip address of listening
 * @returns A P2P node instance
 */
export async function createNode(ipAddresses: Array<string>) {
  /**
   * Init p2p node
   */
  let p2pNode = await Libp2p.create({
    // Listen addresses
    addresses: {
      listen: ipAddresses
      // swarm: [
      //   '/ip4/0.0.0.0/tcp/4002',
      //   '/ip4/127.0.0.1/tcp/4003/ws'
      // ],
      // // snnounce: [],
      // // noAnnounce: [],
      // API: '/ip4/127.0.0.1/tcp/5002',
      // gateway: '/ip4/127.0.0.1/tcp/9090',
      // RPC: '/ip4/127.0.0.1/tcp/5003',
      // delegates: [
      //   '/dns4/node0.delegate.ipfs.io/tcp/443/https',
      //   '/dns4/node1.delegate.ipfs.io/tcp/443/https',
      //   '/dns4/node2.delegate.ipfs.io/tcp/443/https',
      //   '/dns4/node3.delegate.ipfs.io/tcp/443/https'
      // ]
    },

    dialer: {
      maxParallelDials: 150, // 150 total parallel multiaddr dials
      maxDialsPerPeer: 4, // Allow 4 multiaddrs to be dialed per peer in parallel
      dialTimeout: 10e3 // 10 second dial timeout per peer dial
    },

    // Modules to use
    modules: {
      transport: [TCP, WS],
      connEncryption: [NOISE],
      streamMuxer: [MPLEX],
      pubsub: Gossipsub,
      peerDiscovery: [Bootstrap, MulticastDNS],
      dht: KadDHT
    },

    // Modules configuration
    config: {
      peerDiscovery: {
        autoDial: true,
        [MulticastDNS.tag]: {
          enabled: true,
        },

        [Bootstrap.tag]: {
          enabled: true,
          list: [
            '/ip4/104.131.131.82/tcp/4001/p2p/QmaCpDMGvV2BGHeYERUEnRQAwe3N8SzbUtfsmvsqQLuvuJ',
            '/dnsaddr/bootstrap.libp2p.io/p2p/QmNnooDu7bfjPFoTZYxMNLWUQJyrVwtbZg5gBMjTezGAJN',
            '/dnsaddr/bootstrap.libp2p.io/p2p/QmbLHAnMoJPWSCR5Zhtx6BHJX9KiKNN6tpvbUcqanj75Nb',
            '/dnsaddr/bootstrap.libp2p.io/p2p/QmZa1sAxajnQjVM8WjWXoMbmPd7NsWhfKsPkErzpm9wGkp',
            '/dnsaddr/bootstrap.libp2p.io/p2p/QmQCU2EcMqAqQPR2i9bChDtGNJchTbq5TbXJJ16u19uLTa',
            '/dnsaddr/bootstrap.libp2p.io/p2p/QmcZf59bWwK5XFi76CZX8cbJ4BhTzzA3gU1ZjYZcYW3dwt',
            '/dns4/node0.preload.ipfs.io/tcp/443/wss/p2p/QmZMxNdpMkewiVZLMRxaNxUeZpDUb34pWjZ1kZvsd16Zic',
            '/dns4/node1.preload.ipfs.io/tcp/443/wss/p2p/Qmbut9Ywz9YEDrz8ySBSgWyJk41Uvm2QJPhwDJzJyGFsD6',
            '/dns4/node2.preload.ipfs.io/tcp/443/wss/p2p/QmV7gnbW5VTcJ3oyM2Xk1rdFBJ3kTkvxc87UFGsun29STS',
            '/dns4/node3.preload.ipfs.io/tcp/443/wss/p2p/QmY7JB6MQXhxHvq7dBDh4HpbH29v4yE9JRadAVpndvzySN'
          ]
          // list: [
          //   '/ip4/104.131.131.82/tcp/4001/p2p/QmaCpDMGvV2BGHeYERUEnRQAwe3N8SzbUtfsmvsqQLuvuJ',
          //   '/dnsaddr/bootstrap.libp2p.io/p2p/QmNnooDu7bfjPFoTZYxMNLWUQJyrVwtbZg5gBMjTezGAJN',
          //   '/dnsaddr/bootstrap.libp2p.io/p2p/QmbLHAnMoJPWSCR5Zhtx6BHJX9KiKNN6tpvbUcqanj75Nb',
          //   '/dnsaddr/bootstrap.libp2p.io/p2p/QmZa1sAxajnQjVM8WjWXoMbmPd7NsWhfKsPkErzpm9wGkp',
          //   '/dnsaddr/bootstrap.libp2p.io/p2p/QmQCU2EcMqAqQPR2i9bChDtGNJchTbq5TbXJJ16u19uLTa',
          //   '/dnsaddr/bootstrap.libp2p.io/p2p/QmcZf59bWwK5XFi76CZX8cbJ4BhTzzA3gU1ZjYZcYW3dwt'
          // ]
        }
      },
      dht: {                        // The DHT options (and defaults) can be found in its documentation
        kBucketSize: 20,
        enabled: true,
        randomWalk: {
          enabled: true,            // Allows to disable discovery (enabled by default)
        }
      },

      pubsub: {                     // The pubsub options (and defaults) can be found in the pubsub router documentation
        enabled: true,
        emitSelf: true,             // whether the node should emit to self on publish
      },

      nat: {
        enabled: true,
        description: `ipfs@${os.hostname()}`
      }
    },

    metrics: {
      enabled: true
    },

    peerStore: {
      persistence: true
    }
  });

  // Return the p2p node
  return p2pNode
}


