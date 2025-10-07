from arnmap_class import arnmap

# DEBUG: list attributes, methods, and classes in module
# print(dir(arnmap))

arnmap = arnmap()

output = arnmap.scan("arn:aws:glue:us-east-1:123456789012:job/test")
print(output)
