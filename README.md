# PyKamina
![Kamina_Logo](./kamina_logo.svg)  
A Kamina backend using python and IPFS
<br>
## What is Kamina?
IPFS-based decentralized social networking platform

## What is this repo then?
This is an implementation of Kamina(just the backend) written in Python using Flask

## How does this work
This is the way I think Kamina should work (according to spaguettiman's initial idea). I'll try to explain myself as good as I can

#### The backend
Kamina will be a web application that will communicate with a backend with GET/POST requests. So... the backend will be an api and the web application will use it.
Also, the api should be available to anyone (except for certain parts of the page)

#### How will we store data
Since this is ipfs-based, we will be using IPFS (lol).  
We will use .json files for each post/thread/reply and for the user info.  
One problem with ipfs is its inmutability, one can't really delete a file or something once we create it, a way to "circumvent" this issue is to use the files api ipfs has, it emulates a filesystem from which we can delete files and add them n' shit. The thing is that we really aren't deleting them, those files still exist, we can use this functionality as a history feature.  

#### The users problem
Since all files are public once we add them to the network [proof](https://ipfs.io/ipfs/QmTKwydPody1deWXxQo7TZEpuZhFFzDkWpcYyeFyB9WdAb)(some testing I was making), users information will be available to anyone that has the hash of that json file, that means they will have access to the password hash we create. **We need to fix this somehow if we want users functionality**

#### The frontend issue
Since we don't have a frontend (yet) one can use curl in order to test the backend
```sh
# Create a thread
curl -d "title=Why is C++ the best language&body=and why you can't argue with me" http://127.0.0.1:1337/api/make_thread
# Get all threads
curl http://127.0.0.1:1337/api/get_threads
```

#### Further reading
[python-ipfs api documentation](https://ipfs.io/ipns/QmZ86ow1byeyhNRJEatWxGPJKcnQKG7s51MtbHdxxUddTH/Software/Python/ipfsapi/)

## API Documentation
----
### /api/make_thread 
Make a new thread  

__Arguments:__
* title: Thread title
* body: Thread body/content/text
* image (optional and TODO): A list that contains the URL for an image and its thumbnail

__Returns:__  
Nothing

----
### /api/get_threads
Get all threads

__Arguments:__
* None (for now, probably)

__Returns:__  
A JSON-formatted list containing all the existing threads

----
### /api/upload_image
Upload an image to the IPFS node, and create a thumbnail of it

__Arguments:__  
* file (multipart/form-data)he file you want to upload

__Returns:__  
A JSON-formatted list containing IPFS hashes of both the file and its thumbnail
