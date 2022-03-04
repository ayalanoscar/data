

backloan <- read.csv("C:/R/R/backloan1.csv")

head(backloan)


boxplot(backloan$employ ~ backloan$default)


boxplot(backloan$income ~ backloan$default)

install.packages("InformationValue") 


library(InformationValue)


# Crear cortes
cortes = c(0,3,10, 33)
# categorizar la variable
cat_employ =cut(backloan$employ , cortes)

head(cat_employ)
# calculo de frecuencias
table(cat_employ)

#Calculo  del information value

IV(cat_employ, backloan$default)
WOETable(cat_employ, backloan$default)

table(backloan$default)


seguro <- read.csv("C:/R/R/SEGURO1.csv", sep = ";", header = T)


head(seguro)


# Dividir la data


set.seed(1111)

library(dplyr)



seguro_train <- sample_frac(seguro, 0.7)
seguro_test <- setdiff(seguro, seguro_train)

dim(seguro_test)




colSums(is.na(seguro_train))


str(seguro)

attach(seguro)

# Crear modelo
model1 <- glm(Ins ~  Checks +  , data = seguro_train, family = "binomial")
model2 <- glm(Ins ~  Checks + CC + CCBal + DDA +DDABal + Sav + SavBal + MM + MMBal, data = seguro_train, family = "binomial")

summary(model1)
summary(model2)

head(model1$fitted.values)


# Predecir tabla train

predicciones_train1=as.factor(ifelse(test = model1$fitted.values > 0.35, yes = 1, no = 0))
predicciones_train2=as.factor(ifelse(test = model2$fitted.values > 0.35, yes = 1, no = 0))


round(prop.table(table(seguro$Ins))*100,0)

# Matriz De confusion
table(predicciones_train2 , seguro_train$Ins)


length(predicciones_train1)
length(seguro_train$Ins)

# Predecir tabla test

predicciones_test1= as.factor(ifelse(test = (predict(model1, seguro_test, type = "response")) > 0.35, yes = 1, no = 0))
predicciones_test2= as.factor(ifelse(test = (predict(model2, seguro_test, type = "response")) > 0.35, yes = 1, no = 0))

# Matriz De confusion en el test
table(predicciones_test2 , seguro_test$Ins)


library(rpart)

arbol1 <- rpart(formula = Ins ~ . , data = seguro_train)
pred_arbol_test=as.factor(ifelse(test = (predict(arbol1, newdata = seguro_test, type = "vector")) > 0.35, yes = 1, no = 0))
# Matriz De confusion en el test con arboles de decision
table(pred_arbol_test , seguro_test$Ins)

