pragma solidity ^0.4.0;

//registers all the farmer contracts t track his work
contract FarmProduce {

    // Crop infomration data structure
    struct Crop {  
        string storageHashkey;
        string name;
        string pType; 
        string startDate;
        string endTime;
        uint quantity;  
		uint unitPrice;
		string unit;
        string log; 
        address seeder;//who supplied seeds
        string status;

        mapping (uint=> Investment) investments;
		uint numInvests;
    } 
   
	//For tracking the investments
    struct Investment {
        uint when;
        uint amount;
    }

    // just to restrict centralized crop registrations... 
    uint32 maxCropsAllowed = 5;

	// To maintain the number of Crops 
	uint totItems;

    // hold all the crops thats being produced/produced by a farmer  
    mapping (uint => Crop) crops;

	// Constructor
	function FarmProduce() {
		totItems = 0;
	}


	    // Farmer can create a new Crop when a new farming season begins
    function registerNewCrop(string hashkey, string pname, string protype, string sdate, string eTime, uint qty, string log, uint amount) returns (bool) {

        if ( totItems >= maxCropsAllowed) return false;

        //Crop nCrop;

		address seedPro = msg.sender;

        crops[totItems].storageHashkey = hashkey;
        crops[totItems].name = pname;
        crops[totItems].pType = protype;
        crops[totItems].startDate = sdate;
        crops[totItems].endTime = eTime;
        crops[totItems].quantity = qty;
		crops[totItems].unitPrice = 0;
        crops[totItems].log = log;
        crops[totItems].seeder = seedPro;
        crops[totItems].status = "created";

		// For Investments
		crops[totItems].numInvests = 0;
		uint nInvests = crops[totItems].numInvests;

        crops[totItems].investments[nInvests].when = now;
        crops[totItems].investments[nInvests].amount = amount; 
        crops[totItems].numInvests++;

		totItems += 1;

        return true;
    }

	// updates allowed crop information
    function updateCropInfo(string hashkey, string pname, string protype, string sdate, 
                            string eTime, uint qty, uint unitPrice, string unit, string log, uint amount, string status) returns (bool) {
        
		//Check whetherthat crop exists or not
        uint index = verifyCrop(hashkey);
        if ( index == 99) return false;
        
		address seedPro = msg.sender;

		// map the fields
        crops[index].name = pname;
        crops[index].pType = protype;
        crops[index].startDate = sdate;
        crops[index].endTime = eTime;
        crops[index].quantity = qty;
		crops[index].unitPrice = unitPrice;
		crops[index].unit = unit;
        crops[index].log = log;
        crops[index].seeder = seedPro;
        crops[index].status = status;

        return true;
    }

	//logs work info 
    function logWork(string hashkey, string log) returns (bool) {
         //Check whetherthat crop exists or not
        uint index = verifyCrop(hashkey);
        if ( index == 99) return false; 
        crops[index].log = log; 
        return true;
    }

    // requires to validate that this particular product actually produced or not
    function verifyCrop(string hashkey) returns (uint index) {
        for (uint i = 0; i < totItems; i++) {
			string sHashkey = crops[i].storageHashkey;
			int iEqs = compare(sHashkey, hashkey);
            //if (sha3(sHashkey) == sha3(hashkey)) {
			if (iEqs == 0) {
                return i;
            }
        } 
        return 99;
    }

	// To Compare two strings
	function compare(string _a, string _b) returns (int) {
        bytes memory a = bytes(_a);
        bytes memory b = bytes(_b);
        uint minLength = a.length;
        if (b.length < minLength) minLength = b.length;
        //@todo unroll the loop into increments of 32 and do full 32 byte comparisons
        for (uint i = 0; i < minLength; i ++)
            if (a[i] < b[i])
                return -1;
            else if (a[i] > b[i])
                return 1;
        if (a.length < b.length)
            return -1;
        else if (a.length > b.length)
            return 1;
        else
            return 0;
    }

	function getTotItems() returns (uint) {
		return totItems;
	}

}


