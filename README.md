# PyKamina
![Kamina_Logo](kamina_logo.svg)  
A Kamina backend using python and IPFS

## What is Kamina?
IPFS-based decentralized social networking platform

## What is this repo then?
This is an implementation of Kamina(just the backend) written in Python using Flask

## Needed features before v1.0
* Get the information of a single thread
* Create a response
* "Delete" a thread/response
* Handle thread/response creation by a particular user

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

#### Further reading
[IPFS's api python implementation's documentation](https://ipfs.io/ipns/QmZ86ow1byeyhNRJEatWxGPJKcnQKG7s51MtbHdxxUddTH/Software/Python/ipfsapi/)

## Installation

There are some prerequisites in order to start tinkering with the backend:
* python (version 3)
* pip (for python 3)
* ipfs (see https://ipfs.io/docs/install/)  
* The frontend repository cloned (https://github.com/ImplyingProgramming/kamina-frontend)
* If you know how to, use a virtualenv

1. Clone the repo and cd into the directory
```sh
git clone https://github.com/ImplyingProgramming/kamina-backend.git
cd kamina-backend
```

2. Install your python dependencies with:
```
pip3 install -r requirements.txt
```
3. Open up a seperate terminal run the ipfs daemon. This can be done with:
```
ipfs daemon
```
4. Run the application with:
```
python3 app.py
```
5. Run the [frontend](https://github.com/ImplyingProgramming/kamina-frontend) repository. See the README there.


## API Documentation
Some parts of the backend require heavily on some features of the
frontend(like id generation), and would make interacting with the backend
through the terminal kinda impossible. Caveat emptor.

----
### /api/make_thread
Make a new thread, you might need to use first the upload_image call

__Arguments:__
* thread_title: Thread's title
* thread_content: Thread's body/content/text
* post_id: a uuidv4 formatted string
* thread_image_hashes (TODO - make this optional): A json object that contains
the URL for an image and its thumbnail
* thread_image_info: A json object containing the size, dimensions, and filename
of the thread's image

__Returns:__  
The response_id of the newly created thread

----
### /api/get_threads
Get all threads

__Arguments:__
* None (for now, probably)

__Returns:__  
A JSON-formatted list containing all the existing threads' details

----
### /api/get_thread
Gets a thread based on a provided thread\_id

__Arguments:__
* post\_id: the uuid of an existing post

__Returns:__  
A JSON-formatted object containing the details of a thread

_or_

A JSON-formatted object containing an entry _err_, if there was an error in processing the request

----
### /api/upload_image
Upload an image to the IPFS node, and create a thumbnail of it

__Arguments:__  
* file (multipart/form-data): the file you want to upload
* post_id: a uuid4 formatted string

__Returns:__  
A JSON-formatted list containing IPFS hashes of both the file and its thumbnail,
and the information of the original image (size, dimensions, filename)

----
In memory of Miguel Vesga
