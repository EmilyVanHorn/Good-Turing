/*authorData = [
    {
        authorID: "thisAuthor"
    },
    {
        authorID: "scaleAuthor"
    },
    {
        authorID: "numberAuthor"
    }
];*/

/*if(Authors.find().count() === 0){
    for(i = 0; i < authorData.length; i++){
        Authors.insert(authorData[i]);
    }
}*/

if(Authors.find().count() === 0){
    Authors.insert({
        authorID: "thisAuthor",
        GT: 3.5
    });

    Authors.insert({
        authorID: "scaleAuthor",
        GT: 17.6
    });

    Authors.insert({
        authorID: "anotherAuthor",
        GT: 33.33
    });
}



