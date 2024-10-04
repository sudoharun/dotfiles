const network = await Service.import("network");

// Objects
const Network = {
  primary: network.primary,
  icon () {
    return network[network.primary].icon_name;
  },
  tooltip () {

  },
};

print(Network.icon())
