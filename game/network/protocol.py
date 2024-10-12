
class Protocol:
    """
    Class for defining the protocol along with its request and response constants.

    Client-server connection process:

        The interactions between the client and the server are not entirely API-based.
        Here are the interactions between the two in chronological order:

        - The client asks for recognition by the server, and the server sends a response
          back to the client - this ensures that the client is valid
        - The client requests the server's map data, and the server sends a response
          to indicate the start of the map's data. Then, the map data itself is sent, along
          with a response to indicate the end of the data stream
        - The client requests to join the server, the latter sending back a response, after
          which the client sends their local player's in-game name and listening for any
          potential errors from the server (name already taken, server full, etc).
        - The server requests the client's local player state to be added, and
          at which point the client sends the requested data - the server finally responds
          to confirm that the data was well received
        - The client then requests the global game state, which the server subsequently
          sends - this is to ensure the client-side knows about all the other players on
          the server

    Client-server update process:

        The update process between the client and server allows for the server's game state
        to be synchronised with the clients' throughout the lifespan of the connection.
        As mentioned prior to this section, the API-based architecture does not necessarily
        apply.
        The server will repeatedly send to all clients, at a strict defined rate, its
        current game state. Here are the different update tasks in order:

        - If the client requests to disconnect from the server, the server will receive
          the request and disconnect the client
        - The client will first request for the global game state, which the server will
          provide
        - The server will then requests right after the client's local game state, which
          the client will provide

        The client and server follow a strict delay in TPS (Ticks Per Second), allowing
        for only a limited amount of calls in a short time frame.

        The idea of client predictions and server reconciliation are convoluted features to
        implement, and though I am eager to explore those ideas further, the genre that
        this game falls under makes these particular features very complex to add.
        It's very fast-paced which requires sending thousands upon thousands of data
        packets, just to keep track of a single player's position and movements (as
        opposed to slower-paced games where player movement is limited).
        This means the API-based architecture cannot be completely applied.
        The aforementioned features may be implemented in the future, but for now it's
        no longer a priority.
    """

    BUFFER_SIZE = 64
    ENCODING = 'utf-8'

    RECOGNITION_REQ = 'TILEGAME'
    RECOGNITION_RES = 'GAMETILE'
    MAPDATA_REQ = 'MAPDATA'
    MAPDATA_RES = 'DATAMAP'
    MAPDATA_EOS = 'MAPREADY'
    PLAYERJOIN_REQ = 'IWANTTOJOIN'
    PLAYERJOIN_RES = 'OKGIVEMEYOURNAME'
    PLAYEROBJ_RES = 'HEREISPLAYER'
    LCGAME_REQ = 'CANISENDLOCALGAMESTATE'
    LCGAME_RES = 'YESSENDLOCALGAMESTATE'
    LCGAME_EOS = 'OKGOTLOCALGAMESTATE'
    GLGAME_REQ = 'CANISENDGLOBALGAMESTATE'
    GLGAME_RES = 'YESSENDGLOBALGAMESTATE'
    GLGAME_EOS = 'OKGOTGLOBALGAMESTATE'
    PACKETRECV_RES = 'PACKETRECEIVED'
    PACKET_EOS = 'PACKETEND'
    DISCONNECT_REQ = 'BYEBYE'

    NAMEALREXIST_ERR = 'USERNAMEALREADYEXISTS'
    MAXPLAYERS_ERR = 'REACHEDMAXPLAYERS'

    PACKET_MAGIC = 'GPKT'

    HIT_REQ = 'HIT'
    HIT_RES = 'GOTHIT'
