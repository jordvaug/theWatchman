# theWatchman
:snake:  Python Project used to scan web applications for security vulnerabilities.

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
https://nmap.org/book/inst-windows.html

Running the tool is as simple as: python thewatchman.py -H https://www.example.com

Command Line options:
  -h, --help                        Show this help message and exit
  -q, --quiet                       Silence command line output
  -H URL, --Host=URL                Specify target Host
  -t APPTYPE, --Type=APPTYPE        Specify target Application type (options: dotnet, wp)
  
  
  Only the Host option is required, if Type is not included then theWatchman will attempt to use nmap to uncover it. This will be noted in the report,
  and future releases will use this information for more targeted probing of the application.
  
  Adding more endpoints to the *endpoints.txt* file will cause theWatchman to scan them, follow the format of the current links to add more (eg /cdn-cgi/login)
                        
                        
:rocket: Good luck with your research!
