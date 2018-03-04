import json

class Player():
    def __init__(self, playerId, name):
        self.playerId = playerId
        self.name = name
        self.location = [0, 0]
    
    def setLocation(self, x, y):
        self.location = [x, y]
        
    def toJSONDict(self, myEncoder):
        jsonDict = { "playerId" : self.playerId, "location" : str(self.location) } 
        return jsonDict
    
    @staticmethod
    def fromJSONDict(jsonDict):
        return Player("XXX", "YYY")

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        # For each custom class, return a dictionary if it's attributes and include a special
        # attribute telling the decoder what "type" it is
        if isinstance(o, Player):
            playerDict = o.toJSONDict(self)
            playerDict["__MyEncoder_class__"] = "Player"
            return playerDict
        
        print("***")
        print("*** MyEncoder.default found unsupported object: " + str(o))
        print("***")
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, o) 
        
# Object
myPlayer = Player("player1", "First Player")
myList = [ myPlayer, "anotheritem", "a third item" ]

# Encode to JSON
jsonString = json.dumps(myList, cls=MyEncoder, sort_keys=True, indent=4)
print("Object encoded to json:")
print(jsonString)



class MyDecoder(json.JSONDecoder):
    def __init__(self):
        # Explicitly call super constructor
        # AND Override object_hook
        json.JSONDecoder.__init__(self, object_hook = self.decodeObjectHook)
    
    def decodeObjectHook(self, decoded):
        print("decodeObjectHook: " + str(decoded))
        if isinstance(decoded, dict):
            if "__MyEncoder_class__" in decoded:
                targetType = decoded["__MyEncoder_class__"]
                if targetType == "Player":
                    return Player.fromJSONDict(decoded)
        return decoded
    
# Decode from JSON
decodedObject = json.loads(jsonString, cls=MyDecoder)
print("Object decoded from json:")
print(decodedObject) 
print("Test resulting dict still works:")
print("get location: " + decodedObject[0].location)

