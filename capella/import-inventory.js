function(doc) {
    if (doc.isActive === true && (doc.isArchived === null || doc.isArchived === false)){
        return true;
    }
    return false;
}