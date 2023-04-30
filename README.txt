Multi-thread Web Server

Function: Able to process HTTP requests sent from different clients at the same time

Procedure: 

(1)	Establish connection between client and server.
(2)	Client sends HTTP request to server.
(3)	Server will parse the request to determine the HTTP request sent by client.
(4)	Server will create and send HTTP response message to client.

Guide:

(1)Ensure the modules below are installed:

socket
threading
os
datetime

(2) Open Command Prompt and type 'python server.py' in the terminal. Access to root page by pressing Ctrl+click the link or copy the link in the web browser.

(3) Disconnect server by closing the Command Prompt.


Note: Unzip the htdocs.zip before running the files. 
