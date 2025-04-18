![preview](preview.jpg)

# Server-Health-and-Memory-Space-Check

This is a python script I wrote that runs every hour on my server (triggered by a cron job).  It updates an HTML page that I can view anytime to see the status of my server.  In addition once a day in the morning it sends the output of the HTML page to my Telegram messaging account.  This keeps me updated on the status of various aspects of the server, including: 
- CPU usage
- Memory usage
- CPU temperature
- Fan speed
- Free hard drive space
- Hard drive SMART check results

Advantages:
- It is automated
- All relevant information in one place
- Always available
- Results are sent to me daily negating me remembering to check
