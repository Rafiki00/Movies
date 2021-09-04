# Movies

This is a script that scrapes the website of my nearest cinema to get the film titles and the show times. Then it uses a function to send the titles to an API and get the film's plot and rating. Once it has done this, it sends an email with all the information that has been gathered.

I have set up a cron job that executes this script on fridays so that I will get an email with the films that I can go see that weekend if I feel like it. I normally don't think of going to the cinema but if this script keeps me up to date I might find a film that I want to watch some weekend !

It has been challenging to set up the cron job because I am using pipenv and am executing python through it, its where I have installed the necessary modules. In the end, I wrote a bash file (with some help from the internet of course) that works. It was much simpler than I thought.

