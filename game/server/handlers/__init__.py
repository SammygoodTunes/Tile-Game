"""
Handlers package.

Handlers are classes that manages different objects on the server-side.
For instance, they can be responsible for updating the player when a local player packet is sent by the client.
The handler will then recuperate that packet and extract its contents to update the server-side player.
(Yes, I know this makes the server less authoritative and prone to cheating, but I don't know about the idea of
sending millions of packets to a server whenever a player moves, and then some algorithm that predicts the player's
movement whilst the packets are being processed on the server-side (a.k.a. client predictions)).
"""