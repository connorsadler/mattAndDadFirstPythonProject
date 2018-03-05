import json

# Object
myDict = { '4': "Four", 
           '6': "Six",
           "Matthew": "My Son"
         }

# Encode to JSON
jsonString = json.dumps(myDict, sort_keys=True, indent=4)
print("Object encoded to json:")
print(jsonString)

# Decode from JSON
decodedObject = json.loads(jsonString)
print("Object decoded from json:")
print(decodedObject) 
print("Test resulting dict still works:")
print("get by key: " + decodedObject["4"])