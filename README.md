# domain-finder

This is a very simple Python script that you can use to search for available domain names from the Terminal. It automatically checks for any needed Python or system dependencies once first launched.

## Usage

```
python domain-finder.py [-h] [-i] [-l] [-c] [-n] [--version]
```
<b>Where: </b>

 -h, --help          show help message and exit
 
  -i, --input         Simple Lookup. Searches for availability of the
                      specified domain name. (.com and .net top-level domains
                      supported)
                      
  -l, --list-domains  Advanced search. This option takes in a list of comma
                      separated strings, generates all possible (and best)
                      combinations between them, and then checks their
                      avalability as domain names via DNS lookup.
                      
  -c, --com           Filter results by .com domains only.
  
  -n, --net           Filter results by .net domains only.
  
  --version           show program's version number and exit
