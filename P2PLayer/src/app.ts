const Libp2p = require('libp2p')
const TCP = require('libp2p-tcp')
const { NOISE } = require('libp2p-noise')
const MPLEX = require('libp2p-mplex')


class Main {

    p2pNode: any

    async init() {
        this.p2pNode = await Libp2p.create({
            addressed: {
                // add a listen address (localhost) to accept TCP connections on a random port
                listen: ['/ip4/127.0.0.1/tcp/0']
            },
            modules: {
                transport: [TCP],
                connEncryption: [NOISE],
                streamMuxer: [MPLEX]
            }
        })
    }

    async start() {
        await this.init()

        this.p2pNode.start()
        console.log('libp2p has started')
      
        // print out listening addresses
        console.log('listening on addresses:')
        this.p2pNode.multiaddrs.forEach(addr => {
          console.log(`${addr.toString()}/p2p/${this.p2pNode.peerId.toB58String()}`)
        })
      
        // stop libp2p
        await this.p2pNode.stop()
    }
}

let main : Main = new Main()
main.start()
    .then(result => {
        console.log("Node is start")
    })
    .catch(error => {
        console.log(`Error on init peer: ${error}`)
    })
    .finally(() => {
        console.log(`Application closed`)
    })