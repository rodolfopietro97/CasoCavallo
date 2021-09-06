const Libp2p = require('libp2p')
const TCP = require('libp2p-tcp')
const { NOISE } = require('libp2p-noise')
const MPLEX = require('libp2p-mplex')
const Gossipsub = require('libp2p-gossipsub')
const Bootstrap = require('libp2p-bootstrap')
const PubsubPeerDiscovery = require('libp2p-pubsub-peer-discovery')
const KadDHT = require('libp2p-kad-dht')

const multiaddr = require('multiaddr')

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
    },

    // Modules to use
    modules: {
      transport: [TCP],
      connEncryption: [NOISE],
      streamMuxer: [MPLEX],
      pubsub: Gossipsub,
      peerDiscovery: [Bootstrap],
      dht: KadDHT
    },

    // Modules configuration
    config: {
      peerDiscovery: {
        autoDial: true,

        [Bootstrap.tag]: {
          enabled: true,
          list: [
            '/ip4/104.131.131.82/tcp/4001/p2p/QmaCpDMGvV2BGHeYERUEnRQAwe3N8SzbUtfsmvsqQLuvuJ',
            '/dnsaddr/bootstrap.libp2p.io/p2p/QmNnooDu7bfjPFoTZYxMNLWUQJyrVwtbZg5gBMjTezGAJN',
            '/dnsaddr/bootstrap.libp2p.io/p2p/QmbLHAnMoJPWSCR5Zhtx6BHJX9KiKNN6tpvbUcqanj75Nb',
            '/dnsaddr/bootstrap.libp2p.io/p2p/QmZa1sAxajnQjVM8WjWXoMbmPd7NsWhfKsPkErzpm9wGkp',
            '/dnsaddr/bootstrap.libp2p.io/p2p/QmQCU2EcMqAqQPR2i9bChDtGNJchTbq5TbXJJ16u19uLTa',
            '/dnsaddr/bootstrap.libp2p.io/p2p/QmcZf59bWwK5XFi76CZX8cbJ4BhTzzA3gU1ZjYZcYW3dwt'
          ]
        }
      },
      dht: {                        // The DHT options (and defaults) can be found in its documentation
        kBucketSize: 20,
        enabled: true,
        randomWalk: {
          enabled: true,            // Allows to disable discovery (enabled by default)
          interval: 300e3,
          timeout: 10e3
        }
      }
    }
  });

  // Return the p2p node
  return p2pNode
}