# API exposing MCP Protocol for Optimal IT

API consists of the following main integrations: 
- Postgres database of Sundea clients
- Google Calendar 
- Gmail 
- SMSAPI 

**Gmail and SMSAPI**  come together within one notification_service file,
where both are configured. 

**Google Calendar** comes with refresh_token file that gets contents of token.js file if exists, else**
creates new one based on google_credentials file that is downloaded from Google Cloud Platform 
within application OAuth scope.
User must log into Google account with the Sundea's Calendar in order to fetch and insert proper data. 

**Postgres database** access comes from custom read-only user for additional layer of safety in case of 
AI malfunction. 

For application to work properly one must fill *.env* file. 

1. **API_ACCESS_TOKEN** access token that ensures only desired access to the service passed inside headers
2. **GOOGLE_CREDENTIALS_FILE** and **GOOGLE_TOKEN_FILE** paths inside server for good configuration of GC access
3. **SERVICE_CALENDAR** ID of installation and service calendar within the main calendar
4. **FORMALITIES_CALENDAR** ID of subsidies and formals calendar within the main calendar
5. **PRODUCT_MEETING_CALENDAR** ID of product meeting (mostly with Boss) calendar within the main calendar
6. **GOOGLE_EMAIL_PASSWORD** unique password created inside Google application passwords scope for access to Gmail
7. **GOOGLE_EMAIL_USER** user for the Gmail whom account the password was created
8. **SMSAPI_TOKEN** access token to SMS API platform
9. **SUPABASE_HOST** host of the database
10. **SUPABASE_USER** user account name of the database host
11. **SUPABASE_PASSWORD** password to the db
12. **SUPABASE_DB** name of the database
13. **COMPANY_HEADQUARTERS** additional location of the company to not hard-code it inside the scripts

