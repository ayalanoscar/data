
x= -5
v=6
z=x+v
z


# Remover objetos del global enviroment.
rm("x")
rm("y")
rm("z")
rm("v").

library(dplyr)

library(e1071)

library(arules)
install.packages("arules")

install.packages("rpart")

library(rpart.plot)



# Funciones

prob = c(0.5 , 0.3 , 0.2)
ganancias = c(-50 , 0 ,30)

sum(prob*ganancias)

ticket = c(30,25,28,33,45)

mean(ticket)
sd(ticket)
max(ticket)


summary(ticket)


# Cargar datos


getwd()
setwd("C:/Users/oscarayala/Documents/R")


seguro = read.csv("SEGURO1.csv", header = T , sep = ";")

head(seguro)
View(seguro)

str(seguro)

head(seguro$SavBal)


mean(seguro$SavBal)
sd(seguro$SavBal)
summary(seguro$SavBal)

# Graficos: Histograma de datos 


hist(seguro$SavBal, xlim = c(0,10000) , breaks = 500)

table(seguro$Sav)
prop.table(table(seguro$Sav))*100

savbal = seguro$SavBal

savbal = subset(savbal, savbal>0)


hist(savbal, xlim = c(0,20000) , breaks = 500)


boxplot(savbal, ylim = c(0,16000) )

boxplot(seguro$CRScore)


summary(seguro$CRScore)


#Videos

# https://youtu.be/MYPyTiKTjo8
# https://youtu.be/ocKu9GvUI1s
























