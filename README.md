# email-sched
 Schedule an email using flask. 

## App description
The applicant is to program a simple web application that is able to serve a POST endpoint. The main function of the endpoint is to store in the database an email for a particular group of recipients. The emails are then to be sent ​automatically​ at a later time. There are several features that needs to be completed:

1. The endpoint should be a POST endpoint with these specs: 
    -  It should be called ‘/save_emails
    -  It should take 4 parameters:
       - ▪ event_id (Integer): id of the event. E.g: 1, 2, 12, 24
       - ▪ email_subject (String): subject of the email. E.g: “Email Subject”.
       - ▪ email_content (String): body of the email. E.g: “Email Body”.
       - ▪ timestamp (Timestamp): date and time of which the email should be sent. To be stored as a timestamp object in the database that you are using. E.g: “15 Dec 2015 23:12”
    - Emails of the recipients should be saved in a database, for which you can come up with your own table schema
2. Emails saved should be executed according to the timestamp saved. Several hints on how you can do this:
   - A script that constantly check for the time and sends the necessary email 
   - Having a queue task that sends the necessary email (b​onus points for this approach will be given)​
3. You can assume the timestamp of the event is UTC+8 (Asia / Singapore).