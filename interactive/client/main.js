/*function Controller(){
    this.List1Author = "";
    this.List2Author = "";
    this.List = "List1";
    this.dep = Deps.Dependency;
    
    this.setList1Author = function(authorID){
        this.List1Author = authorID;
        
    }
    this.setList2Author = function(authorID){
        this.List2Author = authorID;   
    } 
    this.setList = function(list){
        List = list;   
    }
    this.getList1Author = function(){
        return this.List1Author;   
    }
    this.getList2Author = function(){
        return this.List2Author;   
    }
    this.getList = function(){
        return this.List;   
    }
}

var control = new Controller();*/
Session.set("CurrentList", "List1");
Session.set("List1Author", "SomeAuthor1");
Session.set("List2Author", "SomeAuthor2");
Session.set("sortDir", 1);
Session.set("sortField", "authorID");
Session.set("Dataset", "fabricInput");

//SESSION VARIABLES!!!
//List1Author
//List2Author
//CurrentList

Template.main.helpers({
    authorIDList1: function(){
        return Session.get("List1Author");
    },
    authorIDList2: function(){
        return Session.get("List2Author");
    }/*,
    clicked1: function(){
        if(Session.get("CurrentList") == "List1"){
            return "*";
        }  
    },
    clicked2: function(){
        if(Session.get("CurrentList") == "List2"){
            return "*";   
        }
    }*/
});

Template.main.events({
    'click #List1 h1': function(e){
        Session.set("CurrentList", "List1");
        
    },
    'click #List2 h1': function(e){
        Session.set("CurrentList", "List2");
        
    }
              
});

Template.ideasList1.helpers({
    idea: function(){
        return Ideas.find({authorID: Session.get("List1Author")});   
    }
});

Template.ideasList1.events({
});

Template.ideasList2.helpers({
    idea: function(){
        return Ideas.find({authorID: Session.get("List2Author")});   
    }
});

Template.authorsList.helpers({
    author: function(){
        if(Session.get("Dataset") == "fabricAuthor"){
            if(Session.get("sortField") == "authorID"){
                return Authors.find({dataset: "fabricInput"}, {sort: {authorID: Session.get("sortDir")}});  
            } 
            else if(Session.get("sortField") == "GT"){
                return Authors.find({dataset: "fabricInput"}, {sort: {GT_predict: Session.get("sortDir")}});   
            }    
        }
        else if(Session.get("Dataset") == "test"){
            if(Session.get("sortField") == "authorID"){
                return Authors.find({dataset: "test"}, {sort: {authorID: Session.get("sortDir")}});  
            } 
            else if(Session.get("sortField") == "GT"){
                return Authors.find({dataset: "test"}, {sort: {GT_predict: Session.get("sortDir")}});   
            }  
        }
        
        
        
        
        if(Session.get("sortField") == "authorID"){
            return Authors.find({}, {sort: {authorID: Session.get("sortDir")}});  
        } 
        else if(Session.get("sortField") == "GT"){
            return Authors.find({}, {sort: {GT_predict: Session.get("sortDir")}});   
        }
    }
});

Template.authorsList.events({
    'click .author': function(e){
        var author;
        if(e.target.tagName == "DIV"){
            //e.target.style.backgroundColor = "red";  
            author = e.target.firstElementChild.textContent;
        }
        else if(e.target.tagName == "P"){
            // e.target.parentElement.style.backgroundColor = "red";  
             author = e.target.textContent;
        }
        else if(e.target.tagName == "INPUT"){
            author = e.target.value;
        }
        
        if(Session.get("CurrentList") == "List1"){
            Session.set("List1Author", author);
            
        }
        else if(Session.get("CurrentList") == "List2"){
            Session.set("List2Author", author);
        }
    }
});



Template.DatasetList.events({
    'click #fabric-Author': function(e){
        Session.set("Dataset", "fabricInput");   
    },
    'click #test': function(e){
        Session.set("Dataset", "test");   
    }
});

Template.MethodList.helpers({
    method: function(){
        return [{
            name: 'yellow'
        },
        {
            name: 'blue'            
        },
        {
            name: 'purple'
        }];
    }
});

Template.Sort.events({
    'click #ascending': function(e){
        Session.set("sortDir", 1);   
    },
    'click #descending': function(e){
        Session.set("sortDir", -1);   
    },
    'click #authorID': function(e){
        Session.set("sortField", "authorID");   
    },
    'click #GT': function(e){
        Session.set("sortField", "GT");
        
    }
});