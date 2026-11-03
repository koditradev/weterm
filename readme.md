# WETERM 🌐💻

WETERM is a lightweight, web-based terminal interface designed to let you SSH/drop into your VM environment directly through a standard web browser. It helps bypass strict network firewalls where outbound native SSH (Port 22) connections are locked down or fully blocked.

By tunneling terminal streams through standard web sockets (Port 8765 or multiplexed behind 80/443), your terminal traffic looks like standard web browsing to network firewalls.

---

## 🏛️ Special Dedication
```text
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

WETERM ©2026
Made by Aashvik Goel. (https://github.com/koditra)
```

---

## ✨ Features
- **Firewall Evasion:** Connects over standard WebSockets to punch through port-restricted local proxies.
- **Immediate Shell Spawn:** Directly maps a native `/bin/bash` terminal instance to your browser interface upon socket connection using Python's `pty` utilities.
- **Rich Terminal UI:** Utilizes `xterm.js` to render full, beautiful text interactions and ANSI styling on the front-end layout.

---

## 🛠️ Installation & Setup

### Prerequisites
Make sure you have `git` and `python3` installed on your target Linux/macOS machine.

### Quick Start (One Command)
Run this inside your terminal to download and start the application instantly:
```bash
git clone https://github.com && cd weterm && pip install websockets && python server.py
```

### Manual Steps
1. **Clone the Repo:**
   ```bash
   git clone https://github.com
   cd weterm
   ```
2. **Install WebSockets:**
   ```bash
   pip install websockets
   ```
3. **Run the Backend Daemon:**
   ```bash
   python server.py
   ```
4. **Open the Interface:**
   Launch the `index.html` file inside your preferred modern web browser to interact with Orpheus and start running commands.

---

## 🔒 Security Best Practices
Because WETERM opens an interactive shell path via network ports, remember to enforce these production guardrails if exposing this to the public internet:
1. **Enable TLS/SSL (HTTPS):** Wrap your server behind a reverse proxy (like Nginx/Caddy) to enforce `wss://` protocol so keyboard events/passwords aren't visible in plain text.
2. **Web Authentication Layer:** Put basic auth or a token validation mechanism in front of the connection route to ensure unauthorized users cannot spawn shell environments.
