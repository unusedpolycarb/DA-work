rm(list = ls())
library(gtrendsR)
setwd('C:\\Users\\novac\\Documents\\cvt\\covid19spread')
businesses = read.csv("Businesses_Output.csv")
start_date <- as.Date("2020-01-01")
state <- "Maryland"
region <- "US-MD"
state_businesses <- subset(businesses, businesses$State == state)
name <- businesses$Business.Name[1]
res <- gtrends(name, geo = region)
data <- res$interest_over_time 
relevant_time <- subset(data, as.Date(data$date) >= start_date)
list_columns <- relevant_time$date
empty <- data.frame(matrix(0, 1, length(list_columns)))
colnames(empty) <- list_columns

total <- data.frame()
for(row in 1:5){
  name <- businesses$Business.Name[row]
  res <- gtrends(name, geo = region)
  data <- res$interest_over_time 
  if(is.null(data) | length(data) == 0){
    master <- empty
  }
  else{
    list_hits <- t(as.matrix(relevant_time$hits))
    master = data.frame(list_hits)
    colnames(master) <- list_columns
  }
  total <- rbind(total, master)
}
write.csv(total, "C:\\Users\\novac\\Documents\\cvt\\covid19spread\\Maryland_hits.csv")
