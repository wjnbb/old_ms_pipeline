library(ggplot2)

strain <- "GAF05_OM"
batch <- "20230125_GAF05_OM"

RSD_Plot("20230125_GAI13_NM", "GAI13_NM")

RSD_Plot <- function(batch, strain){

setwd(paste0("C:/Users/bacto/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Mass_spec_data/", batch, "/MzMine2"))

mzmine2 <- read.csv(paste0(strain, "_RSD.csv"))

#get all the sample names in the dataset
samples <- colnames(mzmine2)[8:ncol(mzmine2)]

#extract the different sample names for each triplicate
groups <- unlist(str_split(samples, "_rep"))
groups <- groups[-(grep("mzXML", groups))]
groups <- groups[grep("RSD", groups)]

print(groups)

RSD_table <- data.frame()

for(g in groups){
  
  Sample <- rep(g, length(mzmine2$row.ID))
  RT <- mzmine2[,3]
  RSD <- mzmine2[,g]
  
  RSDs <- as.data.frame(cbind(Sample, RT, RSD))
  RSD_table <- rbind(RSD_table, RSDs)
  
}

RSD_table$Sample <- as.factor(RSD_table$Sample)
RSD_table$RSD <- as.numeric(RSD_table$RSD)
RSD_table$RT <- as.numeric(RSD_table$RT)

write.csv(RSD_table, "RSD_table.csv", row.names = F)

ggplot(RSD_table, aes(x=RT, y=RSD, color=Sample)) + geom_point() +
  theme(legend.position="bottom")+
  labs(title=strain, x="RT (mins)", y = "RSD (%)")+
  theme(plot.title = element_text(hjust = 0.5))

ggsave("RSD_plot.png",
       plot = last_plot(),
       device = "png",
       scale = 1,
       width = 10,
       height = 6,
       units = c("in", "cm", "mm", "px"),
       dpi = 300,
       limitsize = TRUE,
       bg = NULL,)

total_features <- length(mzmine2[,1])
print(paste0("total features = ", total_features))

MS2_matches <- length(subset(mzmine2, mzmine2$MS2.cosine.similarity.score >= 0.7)[,1])
print(paste0("MS2 matches = ", MS2_matches))

RSD_20 <- length(subset(RSD_table, RSD_table$RSD <=20)[,1])
print(paste0("Number of features w/ RSD <= 20 is ", RSD_20))

RSD_60 <- length(subset(RSD_table, RSD_table$RSD >=60)[,1])
print(paste0("Number of features w/ RSD >= 60 is ", RSD_60))
  
}


