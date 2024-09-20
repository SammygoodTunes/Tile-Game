
class Protocol:
    """
    TODO: Update this docstring
    Class for defining the protocol along with its request and response constants.

    Client-server connection process:

        The interactions between the client and the server are fairly API-based.
        Here are the interactions between the two in chronological order:

        - The client asks for recognition by the server, and the server sends a response
          back to the client - this ensures that the client is valid
        - The client requests the server's map data, and the server sends a response
          to indicate the start of the map's data, then the map data itself, and finally
          a response to indicate the end of the data stream
        - The client requests the current players online and their state, and the server
          sends a response for the start of the data stream, then the data itself, then
          a response for the end of the data stream
        - The client requests its local player state to be updated on the server, and
          the server responds with a response to indicate that it is ready - the client
          then sends its player state to the server, then a response to indicate the end
          of the data stream - this is mainly used to track the player as it won't exist
          upon joining the server

    Client-server update process:

        The update process between the client and server allows for the server's game state
        to be synchronised with the clients' throughout the lifespan of the connection.
        Here is where the API-based architecture does not necessarily apply.
        The server will repeatedly send to all clients, at a strict defined rate, its
        current game state. Here are the different update tasks in order:

        - If the client requests to disconnect from the server, the server will receive
          the request and disconnect the client
        - The client requests its local player state to be updated on the server, and
          the server responds with a response to indicate that it is ready - the client
          then sends its player state to the server, then a response to indicate the end
          of the data stream
        - The server sends its game state to the client, containing the state of all other
          players, map data, etc
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

    PACKET_MAGIC = 'GPKT'

    HIT_REQ = 'HIT'
    HIT_RES = 'GOTHIT'
