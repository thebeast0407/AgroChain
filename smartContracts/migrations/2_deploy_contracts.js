//var ConvertLib = artifacts.require("./ConvertLib.sol");
//var MetaCoin = artifacts.require("./MetaCoin.sol");
var FarmProduce = artifacts.require("./FarmProduce.sol");

module.exports = function(deployer) {
  //deployer.deploy(ConvertLib);
  //deployer.link(ConvertLib, MetaCoin);
  deployer.deploy(FarmProduce);
};
