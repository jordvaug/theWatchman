# theWatchman
:snake:  Python Project used to scan web applications for security vulnerabilities, this tool is 
designed to make people take security more seriously!

## Uses
Currently designed for use on Windows OS to scan web applications for vulnerabilities. Uses nmap to find open ports and attempts to detect application
framework being used. If the application uses OpenAPI/Swagger theWatchman will attempt to scan swagger and use the endpoints it uncovers. It will also
pick up the CRUD methods available for each endpoint from swagger and will also attempt to fill in parameter queries with data it generates. All endpoints
found from Swagger will be added to *endpoints.txt*, building a bigger list of endpoints it can enumerate against. 

theWatchman will search for data exposed in APIs as well as missing and misconfigured headers and will then build a formatted html report with all of this 
information one directory up. This tool is designed for scanning your own applications to uncover security vulnerabilities, you should have permission before 
attempting to use this on any third part site. The more that the *endpoint.txt* file grows, the **more noise** you will make with your scanning :hear_no_evil:

## Setup
This tool requires the installation of nmap, which can be found here:
https://nmap.org/download.html

To ensure that you have all packages needed, run the setup script included: python setup.py
This will install everything you need, if you have problems with 'nmap module not found' ensure
that nmap is on your system Path variable.

Running the tool is as simple as: python thewatchman.py -H https://www.example.com

Command Line options:
  -h, --help                        Show this help message and exit
  -q, --quiet                       Silence command line output
  -H URL, --Host=URL                Specify target Host
  -t APPTYPE, --Type=APPTYPE        Specify target Application type (options: dotnet, wp)
  -s SSL, --SSL=SSL                 Specify whether to verify SSL certificates, default True
  -c Cert, --Cert=Cert              Specify path to a root certificate (use when a self-signed cert is being used and you have a copy of the public certificat the site uses)
  
  
  Only the Host option is required, if Type is not included then theWatchman will attempt to use nmap to uncover it. This will be noted in the report, and future releases will use this information for more targeted probing of the application.

  **SSL**
  This option is useful when a self-signed certificates are used on a site, if you get an error like "CERTIFICATE_VERIFY_FAILED", you can set *-s* to False. The default value is True. You can also optionally set the -c value to the location of the root certificate that the site uses. For example if my site uses a self-signed cert and I encounter the cert verify failure, I can download the certificate from the browser, place it in theWatchman directory and feed theWatchman that path (eg: -c './cert.crt'), in this case, it is unnecessary to adjust the -s option.
  
  Adding more endpoints to the *endpoints.txt* file will cause theWatchman to scan them, follow the format of the current links to add more (eg /cdn-cgi/login)
                        
                        
:rocket: Good luck with your research!
