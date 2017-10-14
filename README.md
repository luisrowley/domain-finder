# domain-finder

This is a very simple Python script that you can use to search for available domain names from the Terminal. It performs a series of DNS lookups based on the words you provide and then returns a list of the available domain names that can be registered. If there are not any domains available using your criteria, it suggests you new domain names based on synonyms of the words you originally entered.

It can perform one of these types of lookup: 

  1. Simple Lookup. Lets you enter a single word and check the availability for .com or .net TLD extensions.
  2. Advanced Search. In which you can enter multiple space-separated words. It makes all possible combinations between these words and then looks for the available .com or .net domain names using them. 
  
## Installation

The script doesn't need installation and automatically checks for any needed Python or system dependencies once first launched. 

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
  
  
  ## Script in action
  
  This is a very primitive version of the script that runs the main domain search engine at [Mixflare.net](http://www.mixflare.net). 
