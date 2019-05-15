from inmanta.plugins import plugin, netaddr

@plugin
def calc_site_network(site: "appinfra::Site") -> "ip::cidr":
    address_space = netaddr.IPNetwork(site.app_service.network_address)

    if site.app_service.networks_per_site % 2 != 0:
        raise Exception("networks_per_site should be a multiple of 2")

    bits_per_site = int(math.log(8,2))
    site_prefix_length = site.app_service.prefix_length - bits_per_site
    
    subnets = list(address_space.subnet(site_prefix_length))

    if len(subnets) < site.site_index:
        raise Exception("The app service address space is not big enough to allocate a network "
                        "for site with index %d" % site.site_index)

    return str(subnets[site.site_index])

@plugin
def calc_tier_network(site:"appinfra::Site", net_index: "number") -> "ip::cidr":
    address_space = netaddr.IPNetwork(site.network_address)
    subnets = list(address_space.subnet(site.app_service.prefix_length))

    if len(subnets) < net.index:
        raise Exception("A %dth network does not fit in the network of site %s" %
                        (net_index, site.name))

    return str(subnets[net_index])