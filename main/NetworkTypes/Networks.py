from openstack import network

class Network:

    net                 = None
    subnet              = None
    networkName         = ""
    subnetName          = ""
    projectID           = ""
    tenantID            = ""
    ipv4GW              = ""
    ipv4Prefix          = ""
    isInternal          = False

    def __init__(self, networkName, subnetName, projectID, tenantID, ipv4GW, ipv4Prefix, isInternal ):
        self.networkName    = networkName
        self.projectID      = projectID
        self.subnetName     = subnetName
        self.tenantID       = tenantID
        self.isInternal     = isInternal
        self.ipv4GW         = ipv4GW
        self.ipv4Prefix     = ipv4Prefix
        self.isInternal     = isInternal
        self.net            = None
        self.subnet         = None

    def createNetwork(self, conn):

        self.net     = conn.network.create_network(name=self.networkName, tenant_id=self.tenantID)
        self.subnet  = conn.network.create_subnet(name=self.subnetName,
                                                  tenant_id=self.tenantID,
                                                  ip_version=4, # allow to be 6 TODO
                                                  gateway_ip=self.ipv4GW,
                                                  cidr=self.ipv4Prefix,
                                                  network_id=self.net.id)


