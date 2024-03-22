import requests


# Path to file as input, reads the file, splits using newlines and returns the list.
def file2list(file_path):
    with open(file_path, "r") as f:
        output_list = f.read().split('\n')
    return output_list


# Takes a list and a file path, joins the list elements with newlines and writes to a file at file path.
def list2file(input_list, write_path):
    with open(write_path, "w") as f:
        f.write('\n'.join(input_list) + '\n')
    print("Output written to: " + write_path)


# Takes a list of domains, makes a get request for each domain, returns a list of responsive domains.
def try_domains(domain_list):
    UA = {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0."}
    responsive_domains = []
    for domain in domain_list:
        url = "http://" + domain
        print(domain)
        try:
            # Alternatively requests.head or requests.options for a quicker request
            # (nope, problem is hanging on unresponsive domains, not slow responses)
            requests.get(url, timeout=5, headers=UA)
            responsive_domains.append(domain)
            print("Bingo!")
        except requests.exceptions.RequestException as e:
            print(e)
    return responsive_domains


# Takes a list of domains and a path to a directory, for each domain opens a file in specified directory
# and dumps the response from each domain into the file.
def save_domain_text(domain_list, write_directory):
    UA = {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0."}
    for domain in domain_list:
        url = "http://" + domain
        try:
            request = requests.get(url, headers=UA)
            with open(write_directory + domain, "w") as f:
                f.write(request.text)
        except requests.exceptions.RequestException as error:
            print(error)
    print("Domain text files dumped in:", write_directory)


# Takes a list of subdomains and a domain, prepends the subdomain to the domain and returns a list of
# subdomains that didn't give a 404 response.
def try_subdomains(subdomain_list, domain):
    subdomains = []
    for subdomain in subdomain_list:
        # Annoyingly there are atleast one subdomain in the subdomains file that ends with a "."
        # Making a simple check for "." at the start and end of subdomain to skip if found
        if subdomain[0] == "." or subdomain[-1] == ".":
            continue
        else:
            url = "http://" + subdomain + "." + domain
        try:
            request = requests.get(url, timeout=5)
            if request.status_code != 404:
                subdomains.append(subdomain)
                print(subdomain)
        except requests.exceptions.RequestException:
            continue
    return subdomains


def main():
    # Simple test of the requests module
#    try:
#        domain = "dr.dk"
#        url = "http://" + domain
#        r = requests.get(url)
#        print(r.status_code)
#        print(r.url)
#        print(r.headers)
#    except requests.exceptions.RequestException as error:
#        print("Not up. Error:")
#        print(error)

    # Assuming the files are in the same directory as the python script
    domains_path = "list-domains.txt"
    subdomains_path = "subdomains-10000.txt"
    subdomains_write_path = "responsive-subdomains.txt"
    write_path = "responsive-domains.txt"
    write_directory = "domain_text/" # Pre-existing directory for simplicity


    ### Test of file input/output
    #list2file(file2list(domains_path), write_path)


    ### Making requests and saving responsive domains
    #domains_list = file2list(domains_path)
    #responsive_domains_list = try_domains(domains_list)
    #list2file(responsive_domains_list, write_path)

    # Oneliner
    list2file(try_domains(file2list(domains_path)), write_path)


    ### Saving the response text of active domains
    #responsive_domains_list = file2list(write_path)
    #save_domain_text(responsive_domains_list, write_directory)

    # Oneliner
    #save_domain_text(file2list(write_path), write_directory)


    ### Making a requests and saving responsive subdomains
    #domain = 'frist.dk'
    #subdomains_list = file2list(subdomains_path)
    #responsive_subdomains_list = try_subdomains(subdomains_list, domain)
    #list2file(responsive_subdomains_list, subdomains_write_path)

    # Oneliner
    #list2file(try_subdomains(file2list(subdomains_path), 'frist.dk'), subdomains_write_path)


if __name__ == "__main__":
    main()

