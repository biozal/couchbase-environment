function (doc, oldDoc, meta) {
    //warehouse documents are public - thus everyone has read access to them
    channel("*");

    // Prevent write access to warehouse -
    // can only be done via the web interface
    if (oldDoc || doc._deleted) {
        throw({forbidden: "Modifications are not allowed"});
    }
}
