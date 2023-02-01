library(dplyr)

filename <- "G-AZ22_PA14_P1FrB5"
threshold <- 0.01

#test_masses <- read.csv(paste0("C:/Users/WilliamNash/Baccuico Dropbox/Baccuico/LAB Work/Lab Work - Will/Mass_spec_data/DB_Matching/", filename, "GAG22P3Fr11-13.csv"))
test_masses <- read.csv(paste0("C:/Users/bacto/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Mass_spec_data/DB_matching/", filename, ".csv"))
#bbdb <- read.csv("C:/Users/WilliamNash/Baccuico Dropbox/Baccuico/LAB Work/Lab Work - Will/Database Work/Metabolite_Database_v5.2.csv")
bbdb <- read.csv("C:/Users/bacto/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Database Work/Metabolite_Database_v5.2.csv")

colnames(bbdb)[6] <- "exact_mass"
colnames(bbdb)[5] <- "real_exact_mass"
colnames(test_masses)[11] <- "Masses"

#search each of the masses using ppm accuracy threshold and or a specific dalton window
matches <- data.frame()

for (m in 1:length(test_masses$Masses)) {
  
  cn <- as.data.frame(test_masses$Component.Name[m])
  mx <- as.numeric(test_masses$Masses[m])+threshold
  #print(mx)
  mn <- as.numeric(test_masses$Masses[m])-threshold
  #print(mn)
  
  for (b in 1:length(bbdb$exact_mass)) {
    
    #print(paste0(b, "wahoo"))
    
    if(as.numeric(bbdb$exact_mass[b]) <= mx & as.numeric(bbdb$exact_mass[b]) >= mn){
      
      new_match <- bbdb[b,]
      ppm_error <- (((as.numeric(test_masses$Masses[m])) - (as.numeric(bbdb$exact_mass[b])))/(as.numeric(bbdb$exact_mass[b])))*1000000
      new_match <- cbind(cn, new_match, ppm_error)
      print(new_match)
      matches <- rbind(matches, new_match)
      
    }
    
  }
  
}


colnames(matches)[c(1, 6, 7)] <- c("Component Name", "exact_mass", "[M+H]+")

#relocate the ppm error column
matches <- relocate(matches, ppm_error, .before =  PubChemID)

write.csv(matches, paste0("C:/Users/bacto/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Mass_spec_data/DB_Matching/", filename, "_BBDB_matches_+-", threshold, "Da.csv"), row.names = F)
#write.csv(matches, paste0("C:/Users/WilliamNash/Baccuico Dropbox/Baccuico/LAB Work/Lab Work - Will/Mass_spec_data/DB_Matching/", filename, "_BBDB_matches_+-", threshold, "0.002Da.csv"), row.names = F)
