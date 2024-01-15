// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LogisticsContract {
    // Owner of the contract (TechnoLogix Solutions)
    address public owner;

    // Structure to hold shipment details
    struct Shipment {
        string trackingNumber;
        address payable sender;
        address payable receiver;
        uint amount;
        bool isPaid;
        string status;
    }

    // Mapping from tracking number to shipment details
    mapping(string => Shipment) public shipments;

    // Event to be emitted when a shipment is created
    event ShipmentCreated(string trackingNumber, address sender, address receiver, uint amount);

    // Event to be emitted when shipment status is updated
    event ShipmentStatusUpdated(string trackingNumber, string status);

    // Event to be emitted when a shipment is paid
    event ShipmentPaid(string trackingNumber, uint amount);

    // Constructor sets the contract deployer as the owner
    constructor() {
        owner = msg.sender;
    }

    // Modifier to restrict functions to the contract owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can perform this action");
        _;
    }

    // Create a new shipment
    function createShipment(string memory trackingNumber, address payable receiver, uint amount) public {
        require(shipments[trackingNumber].sender == address(0), "Shipment already exists");

        shipments[trackingNumber] = Shipment({
            trackingNumber: trackingNumber,
            sender: payable(msg.sender),
            receiver: receiver,
            amount: amount,
            isPaid: false,
            status: "Created"
        });

        emit ShipmentCreated(trackingNumber, msg.sender, receiver, amount);
    }

    // Update shipment status
    function updateShipmentStatus(string memory trackingNumber, string memory status) public onlyOwner {
        require(shipments[trackingNumber].sender != address(0), "Shipment does not exist");

        shipments[trackingNumber].status = status;
        emit ShipmentStatusUpdated(trackingNumber, status);
    }

    // Pay for a shipment
    function payShipment(string memory trackingNumber) public payable {
        Shipment storage shipment = shipments[trackingNumber];
        require(msg.sender == shipment.sender, "Only sender can pay for the shipment");
        require(!shipment.isPaid, "Shipment is already paid");

        shipment.isPaid = true;
        shipment.receiver.transfer(msg.value);

        emit ShipmentPaid(trackingNumber, msg.value);
    }

    // Get shipment details
    function getShipmentDetails(string memory trackingNumber) public view returns (Shipment memory) {
        return shipments[trackingNumber];
    }
}
