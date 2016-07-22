ideaData = [{
        content: "asdfasdfasdf",
        authorID: "thisAuthor"
    },
    {
        content: "zxcvzxcvzxcv",
        authorID: "scaleAuthor"
    },
    {
        content: "12e412341234",
        authorID: "numberAuthor"
    },
    {
        content: "doremifasolatido",
        authorID: "scaleAuthor"
    }
            ];

if(Ideas.find().count() === 0){
    for(i = 0; i < ideaData.length; i++){
        Ideas.insert(ideaData[i]);
    }
}
            