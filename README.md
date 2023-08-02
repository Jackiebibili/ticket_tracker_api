# Ticketmaster Ticket Tracker API
![build badge](https://codebuild.us-east-2.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiRm1sYWFwSjhaSDA1SWVOR2ZLZlcxc2FoVlp6UUNQQ2pjdDNQYnVobkFnblR4WmdDSWwzaXdTL1JFRy9SUmQxWThCYkR6YUdtR04vN3grZmdlSWFMV2hNPSIsIml2UGFyYW1ldGVyU3BlYyI6IlZUSTJ2bWwvYWZDWWZqdHEiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)\
Serves as the back end of concert ticket price tracking based on Ticketmaster real-time best seats. 

### Installation
- Dev environment
  - To install Python dependencies, run `pipenv install`.
  - You must have preinstalled Node.js.
  - To install node dependencies, run `yarn -cwd ticketscraping/js`.
  - If __node-canvas__ in `node_modules` fails to install, please check if you have the correct prerequisite softwares installed on your machine. The detail can be found at https://github.com/Automattic/node-canvas/wiki#installation-guides based on your system.
- Prod environment
  - Use Dockerfile to build a container image.

### August 1, 2023 Update
Reese84 code stopped working as TicketMaster implement a new anti-bot mechanism as of Aug 1. We will try to get it fixed.
