# DigiBar aka BierVsVirus

Your virtual online bar. Initially built at the [WirVsVirus Hackathon](https://wirvsvirushackathon.org/).

## Inspiration
People get bored and lonely while local bar and coffee shop owners will have huge financial losses through the coronavirus. Let´s help them! #biervsvirus

## The idea
Gives bar and coffeeshop owners the opportunity to create a digital copy of their bar. They can share it with the people living in their city. Visitors can meet with their friends, get to know new people or talk to the barkeeper/regulars. Features include live video chat and events like a pub quiz or live concerts. In order to support the local owners, visitors are enabled to buy online drinks. These drinks can be connected to special offers by the owner (vouchers, raffles, event participation). The goal is to create income for the bar and coffee shop owners while giving people a virtual space to escape their homes.

## How we built it

* `frontend`: Web application with Vue.js, three.js for 3D rendering, PeerJS simplifies WebRTC for video calls
* `backend`: Python Flask API server with a Redis backend.

Run the backend server (via Docker compose or locally with a Redis instance) and specify the URL in the frontend's `src/main.js` config file.

## Challenges we ran into
A lot of different technologies we had to master

## Accomplishments that we're proud of
A lot of the features work already!

## What we learned
No sleep is also an option ;-)

## What's next for BierVsVirus
User Tests! What do users want? Which features should be further developed? Do bar owners want to use this?...