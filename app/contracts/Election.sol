pragma solidity >=0.4.22 <0.9.0;

contract Election {

    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    bool public on_going;
    address public owner;

    mapping(address => bool) public has_voted;
    mapping(uint => Candidate) public candidates;

    uint public candidatesCount;
    uint public totalVote = 0;

    constructor () public {
        owner = msg.sender;
        on_going=true;
        add_candidate("Candidate 1");
        add_candidate("Candidate 2");
        add_candidate("Candidate 3");

    }
    modifier only_admin(){
        require(msg.sender == owner, "Requires admin permission");
        _;
    }
    function start() public only_admin {
        require(on_going == false, "Already started");
        on_going = true;
    }

    function add_candidate(string memory _name) private {
        candidatesCount ++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, 0);
    }

    function end() public only_admin {
        require(on_going == true, "Already ended");

        on_going = false;
    }
    // Getter function to get a candidate by ID
    function get_candidate(uint _id) public only_admin view returns (uint, string memory, uint) {
        Candidate memory candidate = candidates[_id];
        return (candidate.id, candidate.name, candidate.voteCount);
    }

    function vote_for(uint _candidateId) public {
        require(!has_voted[msg.sender], "Already voted");

        require(_candidateId >= 0 && _candidateId < candidatesCount, "Invalid candidate");

        require(on_going, "Election ended");

        has_voted[msg.sender] = true;

        candidates[_candidateId].voteCount ++;
        totalVote++;
    }
}