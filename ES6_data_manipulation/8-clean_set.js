function cleanSet(set, startString) {
    if (typeof startString !== 'string' || startString.length === 0) {
        return '';
    }

    const retrn = [];

    set.forEach((value) => {
        if (typeof value === 'string' && value.startsWith(startString)) {
            retrn.push(value.slice(startString.length));
        }
    });

    return retrn.join('-');
}

export default cleanSet;
