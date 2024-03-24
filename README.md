
# Monee Share
MoneeShare revolutionizes financial accessibility with a seamless text-based banking platform designed for everyone, aimed at financial inclusion especially for those in rural areas, and to breach connectivity constraints.

**Frontend repo**: https://github.com/itcentralng/monee-share-front

**Backend repo**: https://github.com/itcentralng/monee-share-api

## Tools used
1. SignalWire
2. Convex
3. Safe Haven Micro Finance Bank API
4. Fast API
5. React JS

***Note: due to some unknown issue we could not receive replies when we sent SMS to our SignalWire number, so we used react to create an interface to showcase how our app would work.***

## How to run the Front end
1. Clone the repo
2. run `npm install`
3. In the convex dashboard create an environmental variable `API_URL` and set it to your servers URL.
4. Run `npx convex dev`
5. Run `npm run dev:client`
6. Go to the address in your terminal

## How to run the Backend
1. Clone the repo
2. Create a virtual environment `python -m venv venv`
3. Activate the virtual environment `source \venv\Scripts\activate` for Mac/Linux/git bash and `.\venv\Scripts\activate` for windows
4. run `pip install -r requirements.txt`
5. Register on the various platforms and provide the required variables in the .env file
6. run `uvicorn main:app` to start the server


