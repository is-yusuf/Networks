import dns.name
import dns.message
import dns.query
import dns.rdatatype
import dns.resolver
import csv

input_file = 'websites.csv' 
output_file = 'websites2.csv'

carleton = '137.22.1.7'
google = '8.8.8.8'

carleton_resolver = dns.resolver.make_resolver_at(carleton)
google_respolver = dns.resolver.make_resolver_at(google)

answers = carleton_resolver.resolve('github.com', 'A')
for rdata in answers.rrset:
    print(rdata.address)

with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        if row:  
            name = row[1]
            
            answers = carleton_resolver.resolve(name, 'A')
            answers2 = google_respolver.resolve(name, 'A')

            for rdata in answers.rrset:
                response1 = rdata.address
            for rdata in answers2.rrset:
                response2 = rdata.address                        
                
            writer.writerow([name, response1, response2,answers.ttl,answers2.ttl])

top25 = ["nature.com",
"steamcommunity.com",
"businesswire.com",
"maxcdn.bootstrapcdn.com",
"walmart.com",
"azure.microsoft.com",
"buff.ly",
"cdnjs.cloudflare.com",
"zoom.us",
"s3-eu-west-1.amazonaws.com",
"hulu.com",
"motherboard.vice.com",
"windows.microsoft.com",
"s3.amazonaws.com",
"abc.net.au",
"yelp.com",
"mailchi.mp",
"marriott.com",
"business.facebook.com",
"gist.github.com",
"de.wikipedia.org",
"apps.apple.com",
"api.whatsapp.com",
"itunes.apple.com",
"i.redd.it"]


with open("output.txt", "w") as file:

    for name in top25:
        domain = dns.name.from_text(name)

        name_server = '137.22.1.7'

        request_type = dns.rdatatype.A

        my_query = dns.message.make_query(domain, request_type)


        response = dns.query.udp( my_query, name_server)

        print(response,file=file)
