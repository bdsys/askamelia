# askamelia
Alexa app for the bb

* Thanks to this article for help
    - https://medium.com/crowdbotics/how-to-build-a-custom-amazon-alexa-skill-step-by-step-my-favorite-chess-player-dcc0edae53fb

* Checkout the Alexa beta
	- https://skills-store.amazon.com/deeplink/tvt/fae75232cbfa4097303df85ecc596bf664e9c22dc15e7ec1a9f318f80ebed76ce185cb6ef0a22f1e7a540e4df84be133eacb1b175cbf83f84cbcc109976db0ef1c86b6845171dd211b49d137b664b9f924f3dbc743d4d14546cb4db102c0544970130614bdcae9a3cab586fa57778cdc

* Roadmap
    - Create a new CDK stack for infrastructure to allow for inputs and deletes from the DynamoDB table for anyone with a password (no login required, invite only).
    - Django powered web app to create a create/delete interface to a Dynamo DB table. The table will be moved out of the Alexa infra stack and put into the web app infra stack.
    - May end up moving the web app infra to its own pipeline eventually.
    - The web app will allow invitees to add properties to the partition key of "person". The person row will contain birthdate, color, dog, etc. all the good stuff.
    - The Alexa app will allow invitees to "Ask Amelia Cat" about people.