#####################################
#
#         Neutron_Router.py
#
#####################################

import Networks

class Neutron_Router():

    ######   Object Handles   #######
    neutronRouterPointer = None
    network              = None
    port                 = None
    conn                 = None

    ####### Router Properties #######
    name      = ""
    router_id = ""
    tenant_id = ""

    def __init__(self, conn, name, router_id, tenant_id):
        self.neutronRouterPointer = None

        # The connection should never be null, if it is, something very wrong slipped through the cracks
        if conn is None:
            raise AssertionError("Connection object reference is nullptr")

        self.conn      = conn
        self.name      = name
        self.tenant_id = tenant_id
        self.router_id = router_id

    def createNewNeutronRouter(self):
        try:
            self.neutronRouterPointer = self.conn.network.create_router(name=self.name,
                                                                        router_id=self.router_id,
                                                                        tenant_id=self.tenant_id)
        except:
            print "uh oh"

        return self.neutronRouterPointer


    def deleteNeutronRouter(self):
        try:
            self.neutronRouterPointer = self.conn.network.delete_router(self.neutronRouterPointer, ignore_missing=True)
        except:
            print "uh oh"

        return

    def getNeutronRouter(self, routerName):
        try:
            self.neutronRouterPointer = self.conn.network.find_router(routerName)
        except:
            print "uh oh"
        return self.neutronRouterPointer

    def createRouterInterface(self, networkName, subnetName, portName, projectID, tenantID, ipv4GW, ipv4Prefix, isInternal):
        self.network = None
        self.port    = None
        self.network = Networks.Network(networkName,
                                   subnetName,
                                   projectID,
                                   tenantID,
                                   ipv4GW,
                                   ipv4Prefix,
                                   isInternal)



        self.network.createNetwork(self.conn)
        self.port = self.conn.network.create_port(name=portName, network_id=self.network.net.id)
        self.neutronRouterPointer = self.conn.network.add_interface_to_router(self.neutronRouterPointer,
                                                                              subnet_id=self.network.net.id,
                                                                              port_id=self.port.id)

        return



