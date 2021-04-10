rm(list = ls())
# Clear console
library(ggplot2)
library(plyr)
setwd('C:\\Users\\novac\\Documents\\cvt\\covid-and-climate')
all_pm_data <- read.csv("MA_PM2.5_1998-2016.csv"); 
relevant_pm <- subset(all_pm_data, select = c("PM")); 
racial_data <- read.csv("mass_city_demographic_data.csv"); head(racial_data)
nonwhite_racial <- subset(racial_data, select = c("Proportion.Non.White.Population"))
pm_vector <- as.vector(relevant_pm)
race_vector <- as.vector(nonwhite_racial)
df <- data.frame(race_vector, pm_vector); head(df)
ggplot(data = df, aes(x = Proportion.Non.White.Population, y= PM, group=1)) +
geom_point(size = 1) + 
geom_smooth(method="auto", se=FALSE, fullrange=FALSE, level=0.95) + 
labs(x ="Proportion of Non-White Population", y = "PM Level", shape = "") + 
coord_cartesian(xlim=c(0,1), ylim = c(0, 12)) + 
ggtitle("Ratio of Non-White Population vs PM Particulate Matter Levels in Massachussets")
res <- cor(df)
print(as.vector(res)[2])
nonwhitenonasian_racial <- subset(racial_data, select = c("Proportion.Non.White.or.Asian.Population"))
race_vector <- as.vector(nonwhitenonasian_racial)
df <- data.frame(race_vector, pm_vector); head(df)
ggplot(data = df, aes(x = Proportion.Non.White.or.Asian.Population, y= PM, group=1)) +
  geom_point(size = 1) + 
  geom_smooth(method="auto", se=FALSE, fullrange=FALSE, level=0.95) + 
  labs(x ="Proportion Non-White and Non-Asian Population", y = "PM Level", shape = "") + 
  coord_cartesian(xlim=c(0,1), ylim = c(0, 12)) + 
  ggtitle("Ratio of Non-White and Non-Asian Population vs PM Particulate Matter Levels in Massachussets")
res <- cor(df)
print(as.vector(res)[2])

