import os
import pty
import select
import asyncio
import websockets

# Your custom WETERM Orpheus splash screen
WELCOME_MESSAGE = """\r
                 Say hi to Orph!                  
                                                  
                     :^^^~~^.                     
                  .!^.      ~7                    
                .JY    .^~:  :Y                   
               .P5@5  .GG#5.  ^?                  
                Y:..   .. 7.   G.                 
                .J.      ~?    ~7                 
          ...7^   !^~7~^^:      P                 
         Y!.^!5     ^J          5.                
     .7. 5    :?.   7~          ~7                
    ^7  ?~      !!  G            P                
    57^~:        ^?~?            J:               
  .!:7?^.         :G             .5               
   .:. .^~^.       .J        ^    J^         ^B:  
           ^~~^     .       ?^     #7      :7^#   
             ?J:          .J.      #?    .7^ .G   
             5           ~?        #J  .!!   J:   
             5           P        !!5:!!    ~7    
             J:          5        P ??     :Y     
             ~7         .G^:^^:. !7 :J    :J      
             .5         ^?~:. .~B5   P   ~7       
              Y.           .^^^^.    5.^7:        
              !5.         :         ^B!:          
      .:^^^^^:.          J^      !^~?             
   .!Y~.           ^.   J^       G!^              
   B~.^!        .~!:.^^G!       Y.                
    !^ .Y    .^!^     ?.       ?^                 
     .~^?!~?!:.     :P!::.    ?^                  
         .::        !!:...^!:?^                   
                      .^^^:~G:                    
                                                  
Say hi to orpheus, our god!!!

WETERM \u00a92026
Made by Aashvik Goel. (https://github.com/koditra)\r\n\n"""

async def terminal_handler(websocket):
    # Fork a pseudo-terminal (pty) master/slave pair
    master_fd, slave_fd = pty.openpty()
    
    # Spawn bash connected to the pty slave
    pid = os.fork()
    if pid == 0:
        # Child process: override standard streams and drop into shell
        os.setsid()
        os.dup2(slave_fd, 0)
        os.dup2(slave_fd, 1)
        os.dup2(slave_fd, 2)
        os.close(slave_fd)
        os.close(master_fd)
        os.execv('/bin/bash', ['/bin/bash'])
    
    # Parent process: Close slave file descriptor, keep master open
    os.close(slave_fd)

    # Immediately transmit the Orpheus ASCII banner to the client terminal
    await websocket.send(WELCOME_MESSAGE)

    loop = asyncio.get_running_loop()

    # Task to handle reading shell output and sending it down the socket
    async def shell_to_web():
        try:
            while True:
                # Use select to see if the pty has data waiting non-blockingly
                r, _, _ = select.select([master_fd], [], [], 0.1)
                if master_fd in r:
                    data = os.read(master_fd, 4096)
                    if not data:
                        break
                    # Send bytes decoded as text or direct string format
                    await websocket.send(data.decode('utf-8', errors='ignore'))
                await asyncio.sleep(0.01)
        except (websockets.exceptions.ConnectionClosed, OSError):
            pass

    # Task to handle receiving browser keystrokes and injecting into shell
    async def web_to_shell():
        try:
            async for message in websocket:
                os.write(master_fd, message.encode('utf-8'))
        except (websockets.exceptions.ConnectionClosed, OSError):
            pass

    # Gather tasks and run concurrently
    await asyncio.gather(shell_to_web(), web_to_shell())
    
    # Cleanup process when the user closes their browser connection
    try:
        os.close(master_fd)
        os.kill(pid, 9)
    except OSError:
        pass

async def main():
    async with websockets.serve(terminal_handler, "0.0.0.0", 8765):
        print("WETERM Server Initialized on ws://localhost:8765")
        await asyncio.future() # Keep running indefinitely

if __name__ == "__main__":
    asyncio.run(main())
