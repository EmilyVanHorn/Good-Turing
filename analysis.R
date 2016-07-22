library(ggplot2)

good.turing = read.csv("/Users/jchan/Projects/Good-Turing/Data Output/Word2VecOnlyWithStemming_withlog.csv")
str(good.turing)

ggplot(good.turing, aes(x=timeSlice, y=GT_predict_log)) + 
  facet_grid(~dataset) + 
  geom_line(aes(color=method)) + 
  labs(x="Time slice", y="Pr(New Idea), log scale") + 
  #scale_x_continuous(breaks=c(10,20,30,40,50,60), limits=c(10,60)) +
  scale_color_discrete(name="Method") +
  theme(axis.title.x=element_text(face='bold',size=14,vjust=0.25),
        axis.text.x=element_text(size=10),
        axis.title.y=element_text(face='bold',size=14,vjust=0.45),
        axis.text.y=element_text(size=10))
ggsave(filename="/Users/jchan/Projects/Good-Turing/Data Output/experiment_output_log.png", height=4.15, width=15.34)

#trunc = subset(subsetgood.turing, method )
ggplot(subset(subset(good.turing, timeSlice > 9), method %in% c('word2vec_0.20', 'word2vec_0.40')), aes(x=timeSlice, y=GT_predict)) + 
  facet_grid(~dataset) + 
  geom_line(aes(color=method)) + 
  labs(x="Time slice", y="Pr(New Idea)") + 
  #scale_x_continuous(breaks=c(10,20,30,40,50,60), limits=c(10,60)) +
  scale_color_discrete(name="Method") +
  theme(axis.title.x=element_text(face='bold',size=14,vjust=0.25),
        axis.text.x=element_text(size=10),
        axis.title.y=element_text(face='bold',size=14,vjust=0.45),
        axis.text.y=element_text(size=10))
ggsave(filename="/Users/jchan/Projects/Good-Turing/Data Output/experiment_output_trunc.png", height=4.15, width=15.34)

good.turing.eval = read.csv("/Users/jchan/Projects/Good-Turing/Data Output/ParamSearch_Experiment_evaluation.csv")
str(good.turing.eval)

mean(good.turing.eval$corr_true)

gt.wedding.byPerson = read.csv("/Users/jchan/Projects/Good-Turing/Data Output/evaluate_ideas_wedding_with_ratings_results.csv.csv")
colnames(gt.wedding.byPerson)[colnames(gt.wedding.byPerson) == "dataset"] <- "userName"
gt.wedding.byPerson = merge(gt.wedding.byPerson, pInsp.full.ideas.liberal.final, by="userName", all.x=TRUE)