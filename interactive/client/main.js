
Session.set("CurrentList", "List1");
Session.set("List1Author", "SomeAuthor1");
Session.set("List2Author", "SomeAuthor2");
Session.set("sortDir", 1);
Session.set("sortField", "authorID");
Session.set("Dataset", "fabricInput");
Session.set("Method", "all");
Session.set("Version", "author");

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
//        var dataset = Session.get("Dataset");
//        var method = Session.get("Method");
//        var version = Session.get("Version");
//        var sortField = Session.get("sortField");
//        var sortDir = Session.get("sortDir");
        alert("Dataset: " + Session.get("Dataset"));
        alert("Method: " + Session.get("Method"));
        alert("Version: " + Session.get("Version"));
        
        if(Session.get("Method") == "all"){
            if(Session.get("Version") == "author"){
                if(Session.get("sortField") == "authorID"){
                    return Authors.find(
                        {dataset: Session.get("Dataset")}, 
                        {sort: {authorID: Session.get("sortDir")}});
                }
                else if(Session.get("sortField") == "corr_true"){
                    return Authors.find(
                        {dataset: Session.get("Dataset")}, 
                        {sort: {corr_true: Session.get("sortDir")}});
                }
                else if(Session.get("sortField") == "decline_slope"){
                    return Authors.find(
                        {dataset: Session.get("Dataset")}, 
                        {sort: {decline_slope: Session.get("sortDir")}});
                }
                else if(Session.get("sortField") == "exp_slope"){
                    return Authors.find(
                        {dataset: Session.get("Dataset")}, 
                        {sort: {exp_slope: Session.get("sortDir")}});
                }
                else if(Session.get("sortField") == "method"){
                    return Authors.find(
                        {dataset: Session.get("Dataset")}, 
                        {sort: {run: Session.get("sortDir")}});
                }
            }//Version: author





            else if(Session.get("Version") == "theme"){
                if(Session.get("sortField") == "theme"){
                    return Themes.find(
                        {dataset: Session.get("Dataset")}, 
                        {sort: {theme: Session.get("sortDir")}});
                }
                else if(Session.get("sortField") == "corr_true"){
                    return Themes.find(
                        {dataset: Session.get("Dataset")}, 
                        {sort: {corr_true: Session.get("sortDir")}});
                }
                else if(Session.get("sortField") == "decline_slope"){
                    return Themes.find(
                        {dataset: Session.get("Dataset")}, 
                        {sort: {decline_slope: Session.get("sortDir")}});
                }
                else if(Session.get("sortField") == "exp_slope"){
                    return Themes.find(
                        {dataset: Session.get("Dataset")}, 
                        {sort: {exp_slope: Session.get("sortDir")}});
                }
                else if(Session.get("sortField") == "method"){
                    return Themes.find(
                        {dataset: Session.get("Dataset")}, 
                        {sort: {run: Session.get("sortDir")}});
                }
            }//Version: theme
        }//MethodAll
        else{
            if(Session.get("Version") == "author"){
                if(Session.get("sortField") == "authorID"){
                    return Authors.find(
                        {dataset: Session.get("Dataset"), run: Session.get("Method")}, 
                        {sort: {authorID: Session.get("sortDir")}});
                }
                else if(Session.get("sortField") == "corr_true"){
                    return Authors.find(
                        {dataset: Session.get("Dataset"), run: Session.get("Method")}, 
                        {sort: {corr_true: Session.get("sortDir")}});
                }
                else if(Session.get("sortField") == "decline_slope"){
                    return Authors.find(
                        {dataset: Session.get("Dataset"), run: Session.get("Method")}, 
                        {sort: {decline_slope: Session.get("sortDir")}});
                }
                else if(Session.get("sortField") == "exp_slope"){
                    return Authors.find(
                        {dataset: Session.get("Dataset"), run: Session.get("Method")}, 
                        {sort: {exp_slope: Session.get("sortDir")}});
                }
                else if(Session.get("sortField") == "method"){
                    return Authors.find(
                        {dataset: Session.get("Dataset"), run: Session.get("Method")}, 
                        {sort: {run: Session.get("sortDir")}});
                }
            }//Version: author





            else if(Session.get("Version") == "theme"){
                if(Session.get("sortField") == "theme"){
                    return Themes.find(
                        {dataset: Session.get("Dataset"), run: Session.get("Method")}, 
                        {sort: {theme: Session.get("sortDir")}});
                }
                else if(Session.get("sortField") == "corr_true"){
                    return Themes.find(
                        {dataset: Session.get("Dataset"), run: Session.get("Method")}, 
                        {sort: {corr_true: Session.get("sortDir")}});
                }
                else if(Session.get("sortField") == "decline_slope"){
                    return Themes.find(
                        {dataset: Session.get("Dataset"), run: Session.get("Method")}, 
                        {sort: {decline_slope: Session.get("sortDir")}});
                }
                else if(Session.get("sortField") == "exp_slope"){
                    return Themes.find(
                        {dataset: Session.get("Dataset"), run: Session.get("Method")}, 
                        {sort: {exp_slope: Session.get("sortDir")}});
                }
                else if(Session.get("sortField") == "method"){
                    return Themes.find(
                        {dataset: Session.get("Dataset"), run: Session.get("Method")}, 
                        {sort: {run: Session.get("sortDir")}});
                }
            }//Version: theme
    
        }//MethodOthers
    
    
    
    }//"author"
});//template
        
        
        
//        if(Session.get("Dataset") == "fabricAuthor"){
//            if(Session.get("sortField") == "authorID"){
//                return Authors.find({dataset: "fabricInput"}, {sort: {authorID: Session.get("sortDir")}});  
//            } 
//            else if(Session.get("sortField") == "corr_true"){
//                return Authors.find({dataset: "fabricInput"}, {sort: {GT_predict: Session.get("sortDir")}});   
//            }    
//        }
//        else if(Session.get("Dataset") == "test"){
//            if(Session.get("sortField") == "authorID"){
//                return Authors.find({dataset: "test"}, {sort: {authorID: Session.get("sortDir")}});  
//            } 
//            else if(Session.get("sortField") == "GT"){
//                return Authors.find({dataset: "test"}, {sort: {GT_predict: Session.get("sortDir")}});   
//            }  
//        }
        
        
        
//});

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

Template.authorItem.helpers({
    thing: function(){
        if(Session.get("Version") == "author"){
            return true;
        }
        else if(Session.get("Version") == "theme"){
            return false;
        }
    }
});

Template.DatasetList.events({
    'click #fabric-Author': function(e){
        Session.set("Dataset", "fabricInput"); 
        Session.set("Version", "author");
        Session.set("sortField", "author");
    },
    'click #fabric-Theme': function(e){
        Session.set("Dataset", "fabricInput");  
        Session.set("Version", "theme");
        Session.set("sortField", "theme");
    },
    'click #names-Author': function(e){
        Session.set("Dataset", "namesInput");  
        Session.set("Version", "author");
        Session.set("sortField", "theme");
    },
    'click #names-Theme': function(e){
        Session.set("Dataset", "namesInput"); 
        Session.set("Version", "theme");
        Session.set("sortField", "theme");
    },
    'click #wedding-Author': function(e){
        Session.set("Dataset", "weddingInput");  
        Session.set("Version", "author");
        Session.set("sortField", "theme");
    },
    'click #test': function(e){
        Session.set("Dataset", "test");   
    }
});

Template.MethodList.events({
    'click #two': function(e){
        Session.set("Method", "word2vec_0.20");   
    },
    'click #three': function(e){
        Session.set("Method", "word2vec_0.30");   
    },
    'click #four': function(e){
        Session.set("Method", "word2vec_0.40");   
    },
    'click #five': function(e){
        Session.set("Method", "word2vec_0.50");   
    },
    'click #six': function(e){
        Session.set("Method", "word2vec_0.60");   
    },
    'click #seven': function(e){
        Session.set("Method", "word2vec_0.70");   
    },
    'click #eight': function(e){
        Session.set("Method", "word2vec_0.80"); 
    },
    'click #nine': function(e){
        Session.set("Method", "word2vec_0.90");   
    },
    'click #all': function(e){
        Session.set("Method", "all");   
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
    'click #theme': function(e){
        Session.set("sortField", "theme");   
    },
    'click #corr_true': function(e){
        Session.set("sortField", "corr_true");
    },
    'click #dataset': function(e){
        Session.set("sortField", "dataset");
    },
    'click #decline_slope': function(e){
        Session.set("sortField", "decline_slope");
    },
    'click #exp_slope': function(e){
        Session.set("sortField", "exp_slope");
    },
    'click #method': function(e){
        Session.set("sortField", "method");
    },
    'click #threshold': function(e){
        Session.set("sortField", "threshold");
    }
});