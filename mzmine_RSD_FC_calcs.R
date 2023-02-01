library(tibble)
library(stringr)
library(dplyr)

calcs("BC01_Zt_AcF_E3", "20230113_BC01_Zt_AcF_E3", 1)

strain <- "GAF05_OM"
batch <- "20230125_GAF05_OM"
fcg_num <- 1

calcs <- function(strain, batch, fcg_num){

setwd(paste0("C:/Users/bacto/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Mass_spec_data/", batch, "/MzMine2"))

#read in mzmine2 output
mzmine <- read.csv(paste0(strain, ".csv"))

#get all the sample names in the dataset
samples <- colnames(mzmine)[7:ncol(mzmine)]

print(samples)
sort(samples)

#extract the different sample names for each triplicate
groups <- unlist(str_split(samples, "_rep"))
groups <- groups[-(grep("mzXML", groups))]
groups <- unique(groups)

print(groups)

#reorder the columns by alphabetical order
intensities <- mzmine[,7:ncol(mzmine)]
intensities <- intensities %>% select(order(colnames(intensities)))

#get the peak ID info in a separate df
peak_info <- mzmine[,1:6]

#seed a table for modifying in the loop and join the peak info and reordered intensity info
mzmine2 <- cbind(peak_info, intensities)

#loop through group names to calculate average/stdev/rsd for each group
for(g in groups){
  
  #extract all intensity cols for the group(g)
  g_cols <- grep(g, colnames(mzmine))
  
  if(length(g_cols) < 3){ print(paste0("WARNING ", g, " group has less than three replicates, ", "total = ", length(g_cols)))}
  if(length(g_cols) > 3){ print(paste0("WARNING ", g, " group has more than three replicates, ", "total = ", length(g_cols)))}
  
  g_mzs <- mzmine[,g_cols]
  
  #seed vectors or result storage
  average_col <- numeric()
  sd_col <- numeric()
  rsd_col <- numeric()
  print(g)
  
  for (i in 1:length(g_mzs[,1])) {
    
       average <- mean(as.numeric(g_mzs[i,]))
       average_col <- c(average_col, average)
    
       stdev <- sd(as.numeric(g_mzs[i,]))
       sd_col <- c(sd_col, stdev)
    
       rsd <- ((stdev/average)*100)
       rsd_col <- c(rsd_col, rsd)
       #print(i)
    
     }

  new_cols <- cbind(average_col, sd_col, rsd_col)
  colnames(new_cols) <- c(paste0("Avg_height_", g), paste0("StDev_", g), paste0("RSD_", g))
  mzmine2 <- cbind(mzmine2, new_cols)
  print("succesful iteration")
  
}



#if there is a media group to allow fc analysis
if(is.element(T, grepl("media", groups, ignore.case = T)) == T){
  
  #assign the media group
  media <- groups[grep("media", groups, ignore.case = T)]
  #assign the other groups
  groups <- groups[-(grep("media", groups, ignore.case = T))]
  #Select the avg peak intensity column from the cols with media in the title
  #THIS LINE WILL ONLY WORK IF THE MEDIA IS IN TRIPLICATE
  media_col <- mzmine2[,(grep(media, colnames(mzmine2), ignore.case = T)[4])]
  
  for (g in groups) {
    
    #Take the sample column avg peak height
    #THIS LINE WILL ONLY WORK IF THE SAMPLE IS IN TRIPLICATE
    smp_col <- mzmine2[,(grep(g, colnames(mzmine2))[4])]
    #calculate FC
    FC <- smp_col/media_col
    mzmine2 <- cbind(mzmine2, FC)
    colnames(mzmine2)[ncol(mzmine2)] <- paste0("FC_", g)
    
  }
  
}

#reorder columns again here to get the FC and media info before all the sample intensity data
#remove the sample intensity columns
    for (s in samples) {
  
      mzmine2 <- mzmine2[,-(grep(s, colnames(mzmine2)))]

    }

#re-add the sample intensity columns at the end.
    for (s in samples) {
  
      mzmine2 <- cbind(mzmine2, mzmine[grep(s, colnames(mzmine))])
  
    }



#create vectors to prepare to split the name and cosine score from a single col to 2 cols
name <- character()
cosine <- numeric()

#loop through complete result table row by row
for (i in 1:length(mzmine2$row.ID)) {
  
  #string split to separate name and cosine score
  match <- unlist(str_split(mzmine2$row.identity..main.ID.[i], "cos="))
  
  #if match is empty as there was no match then add NA and skip
  if(length(match) == 1){
    
    name <- c(name, mzmine2$row.identity..main.ID.[i])
    cosine <- c(cosine, "NA")
    next
    
  }else{
    
    #if match score was present split and add info to the relevant new vectors
    d <- unlist(str_split(mzmine2$row.identity..main.ID.[i], "cos="))
    #add the name to the vector
    name <- c(name, as.character(d[1]))
    #add the match score to the vector
    cosine <- c(cosine, as.numeric(d[2]))
    
  }
  
}

#remove the singular column the two new columns are replacing
mzmine2 <- mzmine2[,-4]

mzmine2 <- add_column(mzmine2, name, .before = colnames(mzmine2)[4])
mzmine2 <- add_column(mzmine2, as.numeric(cosine), .before = colnames(mzmine2)[5])

#rename the cosine score column
colnames(mzmine2)[5] <- "MS2 cosine similarity score"

#write to csv
write.csv(mzmine2, paste0(strain, "_RSD.csv"), row.names = F)

#filter by RSD and FC in the different groups
mzmine2_filt_final <- data.frame()
filt_row_nums <- numeric()

#extract the different sample names for each triplicate
groups2 <- unlist(str_split(samples, "_rep"))
groups2 <- groups2[-(grep("mzXML", groups2))]
groups2 <- unique(groups2)



for (g in groups) {
  
  #select all columns from one group
  g_cols <- grep(g, colnames(mzmine2))
  
  #take the row IDs
  mzmine_filt <- mzmine2[,g_cols]
  
  #bind the row ids and group cols
  mzmine_filt <- cbind(mzmine2[,1], mzmine_filt)
  
      if(is.element(T, grepl("media", groups2, ignore.case = T)) == F){
        
      print("Filtering just on RSD as no media sample is present")
      #THIS LINE ONLY WORKS IF THE GROUP IS A TRIPLICATE
      mzmine_filt <- subset(mzmine_filt, mzmine_filt[,4] <= 30)
  
      }else{
  
  print("Filtering on RSD and FC, media sample is present")      
  mzmine_filt <- subset(mzmine_filt, mzmine_filt[,4] <= 30 &
                          mzmine_filt[,5] >= 5)
  
  
  #add this groups filt row ids to the total vector 
  filt_row_nums <- c(filt_row_nums, mzmine_filt[,1])
  print(paste0("number of rows meeting criteria now is...", length(filt_row_nums)))
  
}}

#remove the duplicate row indexes
filt_row_nums2 <- unique(filt_row_nums)

#filter the table by the row.ID column for rows where the filter criteria were met
mzmine2_filt_final <- mzmine2[match(filt_row_nums2, mzmine2$row.ID),]

#convert the row ids to a data frame
filt_row_nums <- as.data.frame(filt_row_nums)

#count the number of occurrences of each row id
filt_row_nums3 <- table(filt_row_nums)
filt_row_nums3 <- as.data.frame(filt_row_nums3)

if(fcg_num >= 2){

     #filter the row ids based on a frequency of at least 2
     filt_row_nums3 <- filt_row_nums3[filt_row_nums3$Freq >= fcg_num,]

     #convert the data so the right values are used when filtering
     filt_row_nums3 <- as.numeric(as.character(filt_row_nums3$filt_row_nums))

     #filter the original table by the filtered row ids
     mzmine2_hard_filt_final <- mzmine2[match(filt_row_nums3, mzmine2$row.ID),]

     #write the csv
     write.csv(mzmine2_filt_final, paste0(strain, "_filtered.csv"), row.names = F)
     write.csv(mzmine2_hard_filt_final, paste0(strain, "_filtered_", fcg_num, "groupFC.csv"), row.names = F)


     }else{

     #convert the data so the right values are used when filtering
     filt_row_nums3 <- as.numeric(as.character(filt_row_nums3$filt_row_nums))

     #filter the original table by the filtered row ids
     mzmine2_hard_filt_final <- mzmine2[match(filt_row_nums3, mzmine2$row.ID),]

     #write the csv
     write.csv(mzmine2_filt_final, paste0(strain, "_filtered.csv"), row.names = F)

     }

}


