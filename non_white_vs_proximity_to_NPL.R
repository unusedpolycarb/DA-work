rm(list = ls())
library(ggplot2)
library(plyr)
setwd('C:\\Users\\novac\\Documents\\cvt\\covid-and-climate')
df <- read.csv("proximity_to_NPL_sites_demographics.csv"); head(data)
pm_data <- read.csv("proximity_to_NPL_sites_pm.csv")
non_white <- subset(df, select = c("Distance", "Proportion.Non.White.Population")) 
non_white_non_asian <- subset(df, select = c("Distance", "Proportion.Non.White.or.Non.Asian.Population"))
ggplot(data = df, aes(x = Distance, y = Proportion.Non.White.Population, group = 1)) + 
geom_point(size = 5) + 
geom_smooth(method="auto", se=FALSE, fullrange=FALSE, level=0.95) + 
labs(y ="Proportion of Non-White Population", x = "Distance from NPL Site (kilometers)", shape = "") + 
coord_cartesian(xlim=c(0,30), ylim = c(0, 1)) + 
ggtitle("Distance from NPL Site in Kilometers and its racial makeup")
res <- cor(df)
print(as.vector(res[2]))
ggplot(data = df, aes(x = Distance, y = Proportion.Non.White.Population, group = 1)) + 
geom_point(size = 5) + 
geom_smooth(method="auto", se=FALSE, fullrange=FALSE, level=0.95) + 
labs(y ="Proportion of Non-White and Non-Asian Population", x = "Distance from NPL Site (kilometers)", shape = "") + 
coord_cartesian(xlim=c(0,30), ylim = c(0, 1)) + 
ggtitle("Distance from NPL Site in Kilometers and its racial makeup")
res <- cor(df)
print(as.vector(res[3]))

ggplot(data = pm_data, aes(x = Distance, y = PM, group = 1)) + 
geom_point(size = 5) + 
geom_smooth(method="auto", se=FALSE, fullrange=FALSE, level=0.95) + 
labs(y ="PM", x = "Distance from NPL Site (kilometers)", shape = "") + 
coord_cartesian(xlim=c(0,30), ylim = c(0, 12)) + 
ggtitle("Distance from NPL Site in Kilometers and its average PM levels")
res <- cor(pm_data)
print(as.vector(res[2]))
