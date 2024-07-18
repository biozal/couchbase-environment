function (doc, oldDoc, meta) {
    try {
        console.log("********Processing Inventory Docs");
        validateNotEmpty("teams", doc.teams);
        //get the teams from the document
        var teams = getTeams();

        //set the channel for the document based on the teams set
        teams.forEach(function(team) {
            //if the document is to be deleted, make sure the user has the proper role
            requireRole(team);

            //if the document isn't being deleted add to proper channels
            if (!isDelete()) {
                var channelId = "channel." + team;
                console.log("********Setting Inventory Channel to " + channelId);
                channel(channelId);
                access("role:" + team, "channel." + team);
            }
        });
    } catch (e) {
        console.log("***************Error Processing Inventory Docs: " + e);
    }

    function getTeams() {
        return isDelete() ? oldDoc.teams : doc.teams;
    }

    function isDelete() {
        return doc._deleted == true;
    }

    function validateNotEmpty(key, value) {
        if (!value) {
            throw {forbidden: key + " is not provided."};
        }
    }
}
