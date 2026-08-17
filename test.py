from beanie import PydanticObjectId


fakeOID = PydanticObjectId()
converted = str(fakeOID)

print(converted, type(converted))