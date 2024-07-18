function(doc) {
    if (doc.isActive === true && (doc.isDiscontinued === null ||  doc.isDiscontinued === false)){
        return true;
    }
    return false;
}