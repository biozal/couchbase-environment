function (doc, oldDoc, meta) {
    console.log("********Processing User Profile Doc. Is oldDoc == null? " + (oldDoc == null));

    // Validate the presence of email field.  This is the "username"
    validateNotEmpty("email", doc.email);

    // Validate that the documentId _id is prefixed by owner
    var expectedDocId = "user" + "::" + doc.email;

    if (expectedDocId != doc._id) {
        // reject document
        throw({forbidden: "UserProfile doc Id must be of form user::email"});
    }
    var username = getEmail();
    var channelId = "channel."+ username;
    try {
        // Assign the document to a public channel to allow everyone to read it
        channel('!');

        // Check if this is an import processing (done with admin credentials)
        requireAdmin();
        if (!isDelete()) {
            // Add doc to the user's channel.
            channel(channelId);

            // Give user access to document
            access(username, channelId);
        }
    } catch (error) {
        console.log("UserProfile - This is not a doc import " + error);
        // If non admin client replication
        if (!isDelete()) {
            // Check if document is being created / added for first time
            // We allow any user to create the document
            if (isCreate()) {
                // Add doc to the user's channel.
                channel(channelId);

                // Give user access to document
                access(username, channelId);

            } else {
                // This is an update
                // Validate that the email hasn't changed.
                validateReadOnly("email", doc.email, oldDoc.email);
                requireUser(oldDoc.email);
            }
        }
    }

    // get email Id property
    function getEmail() {
        return (isDelete() ? oldDoc.email : doc.email);
    }

    // Check if document is being created/added for first time
    function isCreate() {
        // Checking false for the Admin UI to work
        return ((oldDoc == false) || (oldDoc == null || oldDoc._deleted) && !isDelete());
    }

    // Check if this is a document delete
    function isDelete() {
        return (doc._deleted == true);
    }

    // Verify that specified property exists
    function validateNotEmpty(key, value) {
        if (!value) {
            throw({forbidden: key + " is not provided."});
        }
    }

    // Verify that specified property value has not changed during update
    function validateReadOnly(name, value, oldValue) {
        if (value != oldValue) {
            throw({forbidden: name + " is read-only."});
        }
    }
}