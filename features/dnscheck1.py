import dns.resolver

resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = ["8.8.8.8"]
answer = resolver.resolve("8.8.8.8", "PTR")
print("The nameservers are:")
for rr in answer:
    print(rr.target)