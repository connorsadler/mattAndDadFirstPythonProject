
multiplayergame2
----------------

Update log:
	09/03/2018
		- to run from a different client, please run "gameclient different machine.py"
	08/03/2018
		- added text box to allows players to talk to each other
		- added Bombs! Press "b" to drop a box and watch it explode on your screen and other players screens
		- changed "auto move" key to TAB


Connors multiplayer game demo
Heavily enhanced version of the chat room server
Includes a pygame client which connects to this server
Also has a text based client to show what messages are being sent

To run:
1. Run the server file: game server.py
2. Run a game client with: gameclient.py
3. Run another game client: gameclient.py
4. Run a text client: Chat client.py

All 4 must be running concurrently, the server started first
You can move the little man (face) around with the arrow keys
It should show up on the other client also
The "other player" on each client is shown in grey

You can also press Tab to make each client automatically move around the edges of the screen
You can do this on both clients and see all the messages flying around

You can even run a third or fourth game client and see what happens


