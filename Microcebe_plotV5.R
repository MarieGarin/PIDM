                        #require(phytools); require(geiger); require(nlme); require(evomap); require(DataCombine); library(devtools); library(ggbiplot); library(caper)
                        #library(adegenet); library(ape); library(picante); library(stringr)
                        library(ape)
                        library(geiger)
                        library(caper)
                        library(evomap)
                        library(nlme)
                        filename_Tree <- "/home/cgarin/Documents/8_Multispecies/13_Atlas_project/Name_species.nwk"
                        
                        database <- read.csv("/home/cgarin/allvolume_mammals_latin_name_clean.csv", row.names = 1, header = TRUE)
                        database <- as.data.frame(database)
                        interactions <- read.csv("/home/cgarin/interactions.csv", header = TRUE)[,-1]
                        interactions <- as.data.frame(interactions)
                        
                        treebase <-  ape::read.tree(filename_Tree); phytools::read.newick(filename_Tree)
                        
                        #Align data and tree
                        treebase<-treedata(treebase, database, sort=TRUE, warnings=TRUE)$phy
                        database<-as.data.frame(treedata(treebase, database, sort=TRUE, warnings=TRUE)$data)
                        
                        #################################### with optimized lambda ########################################
                        
                        #Subset data and tree
                        d <- 100  #number of parameter
                        dif <- matrix (rep(NA, d*d), d, d)  #init matrix
                        slope <- matrix (rep(NA, d*d), d, d) 
                        intercept <- matrix (rep(NA, d*d), d, d) 
                        lambda <- matrix (rep(NA, d*d), d, d) 
                        
                        for (i in 1:d){
                          for (j in 1:d){
                            if (j != i){
                              dataset<-na.omit(database[, c(i, j)])
                              datadrop<-dataset[!(row.names(dataset) %in% c("Homo_sapiens","Pan_troglodytes", "Macaca_mulatta", "Chlorocebus_aethiops", "Microcebus_murinus")),]
                              if (dim(datadrop)[1] > 5){
                                tryCatch({
                                  dataset[, c(1)] <- as.numeric(dataset[, c(1)])
                                  dataset[, c(2)] <- as.numeric(dataset[, c(2)])
                                  if (interactions[i, j] == TRUE){
                                    dataset[,c(2)] <- dataset[,c(2)] - dataset[,c(1)]}
                                  if (interactions[j, i] == TRUE){
                                    dataset[,c(1)] <- dataset[,c(1)] - dataset[,c(2)]}
                                  dataset <- log(dataset)
                                  dataset <- as.data.frame(treedata(treebase, dataset, sort=TRUE, warnings=TRUE)$data)
                                  treeset <- treedata(treebase, dataset, sort=TRUE, warnings=TRUE)$phy
                                  data <- dataset
                                  tree <- treeset
                                  tree <- drop.tip(treeset, c("Homo_sapiens", "Pan_troglodytes", "Macaca_mulatta", "Chlorocebus_aethiops", "Microcebus_murinus"))
                                  data <- as.data.frame(treedata(tree, data, sort=TRUE, warnings=TRUE)$data)
                                  #Prep pgls
                                  data_pgls <- cbind(data, rownames(data))
                                  tree_pgls <- tree
                                  colnames(data_pgls)[which(colnames(data_pgls)=="rownames(data)")]<-"Species"
                                  data.pgls.NonGA <- comparative.data(tree_pgls, data_pgls, vcv=TRUE ,names.col=Species, vcv.dim=3)
                                  #Run pgls
                                  c1 <- colnames(data_pgls[1])
                                  c2 <- colnames(data_pgls[2])
                                  model_NonGA_lambda <- pgls(as.formula(paste(c1, c2, sep=" ~ ")), data=data.pgls.NonGA, lambda='ML')
                                  model_NonGA_lambda
                                  model <- model_NonGA_lambda
                                  #Prep data
                                  data <- dataset
                                  tree <- treeset
                                  tree <- drop.tip(treeset, c("Homo_sapiens", "Pan_troglodytes", "Macaca_mulatta", "Chlorocebus_aethiops", "Microcebus_murinus"))
                                  data <- as.data.frame(treedata(tree, data, sort=TRUE, warnings=TRUE)$data)
                                  X <- data[, c(2)]
                                  Y <- data[, c(1)]
                                  tree <- rescale(tree, "lambda", model$param[2])
                                  lambda[i, j] <- model$param[2]
                                  vcv_tree <- vcv(tree)
                                  k<-10
                                  model_pi <- gls.pi(Y, X, vcv_tree, k)
                                  n <- length(X)
                                  XX <- cbind(rep(1, n), X)
                                  Sigma <- vcv_tree
                                  tr <- sum(diag(Sigma))
                                  Sigma <- n*Sigma/tr
                                  invSigma <- solve(Sigma)
                                  C <- solve(t(XX)%*%invSigma%*%XX)
                                  w <- C%*%t(XX)%*%invSigma
                                  B <- w%*%Y
                                  Yhat <- XX%*%B
                                  Yresid = Y - Yhat
                                  x <- dataset[c("Microcebus_murinus"), 2]
                                  y <- dataset[c("Microcebus_murinus"), 1]
                                  ZZ <- cbind(rep(1, length(x)), x)
                                  par <- model_pi$model[, 1]
                                  intercept[i, j] <- par[1]
                                  slope[i, j] <- par[2]
                                  Yhat.x <- par[1] + par[2]*x
                                  SEYhat.x <- sqrt((diag(ZZ%*%C%*%t(ZZ))+c(1/k))%*%((t(Yresid)%*%invSigma%*%Yresid)/(n-2)))
                                  pu <- Yhat.x + qt(0.975, n)*SEYhat.x
                                  pl <- Yhat.x - qt(0.975, n)*SEYhat.x
                                  if (y - pu > pl - y){
                                    dif[i, j] <- max(0, y - pu)
                                  } else {
                                    dif[i, j] <- - max(0, pl - y)
                                  }
                                }, error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
                              } 
                            } 
                          } 
                        }
                        
                        
                        ####################################### plot matrix of differences ##########################
                        
                        library(reshape2)
                        library(ggplot2)
                        df <- data.frame(id=colnames(database[, 1:d]),dif)
                        gg <- melt(df, id="id")
                        ggplot(gg, aes(x=id,y=variable,fill=value))+
                          geom_tile()+
                          scale_fill_gradient(low="#FFFF88",high="#FF0000")+
                          coord_fixed()
                        
                        write.csv(df,"/home/cgarin/Matrix_Microcebe2.csv", row.names = FALSE)
                        
                        
                        
                        ####################################### plot matrix of differences ##########################
                        
                        library(reshape2)
                        library(ggplot2)
                        df <- data.frame(id=colnames(database[, 1:d]),lambda)
                        gg <- melt(df, id="id")
                        ggplot(gg, aes(x=id,y=variable,fill=value))+
                          geom_tile()+
                          scale_fill_gradient(low="#FFFF88",high="#FF0000")+
                          coord_fixed()
                        
                        write.csv(df,"/home/cgarin/Matrix_lambda_Microcebe.csv", row.names = FALSE)
                        
                        ####################################### plot matrix of differences ##########################
                        
                        library(reshape2)
                        library(ggplot2)
                        df <- data.frame(id=colnames(database[, 1:d]),slope)
                        gg <- melt(df, id="id")
                        ggplot(gg, aes(x=id,y=variable,fill=value))+
                          geom_tile()+
                          scale_fill_gradient(low="#FFFF88",high="#FF0000")+
                          coord_fixed()
                        
                        write.csv(df,"/home/cgarin/Matrix_slope_Microcebe.csv", row.names = FALSE)
                        
                        
                        ####################################### plot matrix of differences ##########################
                        
                        library(reshape2)
                        library(ggplot2)
                        df <- data.frame(id=colnames(database[, 1:d]),intercept)
                        gg <- melt(df, id="id")
                        ggplot(gg, aes(x=id,y=variable,fill=value))+
                          geom_tile()+
                          scale_fill_gradient(low="#FFFF88",high="#FF0000")+
                          coord_fixed()
                        
                        write.csv(df,"/home/cgarin/Matrix_intercept_Microcebe.csv", row.names = FALSE)
                        
                      
                        
                        
                        #################################### fixed lambda ############################################
                        
                        dif_fixed_lambda <- matrix (rep(NA, d*d), d, d) 
                        
                        for (i in 1:d){
                          for (j in 1:d){
                            if (j != i){
                              dataset<-na.omit(database[, c(i, j)])
                              datadrop<-dataset[!(row.names(dataset) %in% c("Homo_sapiens","Pan_troglodytes", "Macaca_mulatta", "Chlorocebus_aethiops", "Microcebus_murinus")),]
                              if (dim(datadrop)[1] > 5)
                                {tryCatch({
                                dataset[, c(1)] <- as.numeric(dataset[, c(1)])
                                dataset[, c(2)] <- as.numeric(dataset[, c(2)])
                                if (interactions[i, j] == TRUE){
                                  dataset[,c(2)] <- dataset[,c(2)] - dataset[,c(1)]}
                                if (interactions[j, i] == TRUE){
                                  dataset[,c(1)] <- dataset[,c(1)] - dataset[,c(2)]}
                                dataset <- log(dataset)
                                dataset <- as.data.frame(treedata(treebase, dataset, sort=TRUE, warnings=TRUE)$data)
                                treeset <- treedata(treebase, dataset, sort=TRUE, warnings=TRUE)$phy
                                data <- dataset
                                tree <- treeset
                                tree <- drop.tip(treeset, c("Homo_sapiens", "Pan_troglodytes", "Macaca_mulatta", "Chlorocebus_aethiops", "Microcebus_murinus"))
                                data <- as.data.frame(treedata(tree, data, sort=TRUE, warnings=TRUE)$data)
                                #Prep pgls
                                data_pgls <- cbind(data, rownames(data))
                                tree_pgls <- tree
                                colnames(data_pgls)[which(colnames(data_pgls)=="rownames(data)")]<-"Species"
                                data.pgls.NonGA <- comparative.data(tree_pgls, data_pgls, vcv=TRUE ,names.col=Species, vcv.dim=3)
                                #Run pgls
                                c1 <- colnames(data_pgls[1])
                                c2 <- colnames(data_pgls[2])
                                model_NonGA_fixed_lambda <- pgls(as.formula(paste(c1, c2, sep=" ~ ")), data=data.pgls.NonGA, lambda= 1.0)
                                model_NonGA_fixed_lambda
                                model <- model_NonGA_fixed_lambda
                                #Prep data
                                data <- dataset
                                tree <- treeset
                                tree <- drop.tip(treeset, c("Homo_sapiens", "Pan_troglodytes", "Macaca_mulatta", "Chlorocebus_aethiops", "Microcebus_murinus"))
                                data <- as.data.frame(treedata(tree, data, sort=TRUE, warnings=TRUE)$data)
                                X <- data[, c(2)]
                                Y <- data[, c(1)]
                                tree <- rescale(tree, "lambda", model$param[2])
                                vcv_tree <- vcv(tree)
                                k<-31
                                model_pi <- gls.pi(Y, X, vcv_tree, k)
                                n <- length(X)
                                XX <- cbind(rep(1, n), X)
                                Sigma <- vcv_tree
                                tr <- sum(diag(Sigma))
                                Sigma <- n*Sigma/tr
                                invSigma <- solve(Sigma)
                                C <- solve(t(XX)%*%invSigma%*%XX)
                                w <- C%*%t(XX)%*%invSigma
                                B <- w%*%Y
                                Yhat <- XX%*%B
                                Yresid = Y - Yhat
                                x <- dataset[c("Microcebus_murinus"), 2]
                                y <- dataset[c("Microcebus_murinus"), 1]
                                ZZ <- cbind(rep(1, length(x)), x)
                                par <- model_pi$model[, 1]
                                Yhat.x <- par[1] + par[2]*x
                                SEYhat.x <- sqrt((diag(ZZ%*%C%*%t(ZZ))+c(1/k))%*%((t(Yresid)%*%invSigma%*%Yresid)/(n-2)))
                                pu <- Yhat.x + qt(0.975, n)*SEYhat.x
                                pl <- Yhat.x - qt(0.975, n)*SEYhat.x
                                if (y - pu > pl - y){
                                  dif_fixed_lambda[i, j] <- max(0, y - pu)
                                } else {
                                  dif_fixed_lambda[i, j] <- - max(0, pl - y)
                                }  #end else
                              }, error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
                              }  
                            }
                          } 
                        } 
                        
                        
                        ####################################### plot matrix of differences ##########################
                        
                        library(reshape2)
                        library(ggplot2)
                        df <- data.frame(id=colnames(database[, 1:d]),dif_fixed_lambda)
                        gg <- melt(df, id="id")
                        ggplot(gg, aes(x=id,y=variable,fill=value))+
                          geom_tile()+
                          scale_fill_gradient(low="#FFFF88",high="#FF0000")+
                          coord_fixed()
                        write.csv(df,"/home/cgarin/Matrix_fixedlambda_Microcebe2_1_curent.csv", row.names = FALSE)
                        
                        
                        #################################### fixed lambda ############################################
                        
                        dif_fixed_lambda <- matrix (rep(NA, d*d), d, d) 
                        
                        for (i in 1:d){
                          for (j in 1:d){
                            if (j != i){
                              dataset<-na.omit(database[, c(i, j)])
                              datadrop<-dataset[!(row.names(dataset) %in% c("Homo_sapiens","Pan_troglodytes", "Macaca_mulatta", "Chlorocebus_aethiops", "Microcebus_murinus")),]
                              if (dim(datadrop)[1] > 5)
                                {tryCatch({
                                dataset[, c(1)] <- as.numeric(dataset[, c(1)])
                                dataset[, c(2)] <- as.numeric(dataset[, c(2)])
                                if (interactions[i, j] == TRUE){
                                  dataset[,c(2)] <- dataset[,c(2)] - dataset[,c(1)]}
                                if (interactions[j, i] == TRUE){
                                  dataset[,c(1)] <- dataset[,c(1)] - dataset[,c(2)]}
                                dataset <- log(dataset)
                                dataset <- as.data.frame(treedata(treebase, dataset, sort=TRUE, warnings=TRUE)$data)
                                treeset <- treedata(treebase, dataset, sort=TRUE, warnings=TRUE)$phy
                                data <- dataset
                                tree <- treeset
                                tree <- drop.tip(treeset, c("Homo_sapiens", "Pan_troglodytes", "Macaca_mulatta", "Chlorocebus_aethiops", "Microcebus_murinus"))
                                data <- as.data.frame(treedata(tree, data, sort=TRUE, warnings=TRUE)$data)
                                #Prep pgls
                                data_pgls <- cbind(data, rownames(data))
                                tree_pgls <- tree
                                colnames(data_pgls)[which(colnames(data_pgls)=="rownames(data)")]<-"Species"
                                data.pgls.NonGA <- comparative.data(tree_pgls, data_pgls, vcv=TRUE ,names.col=Species, vcv.dim=3)
                                #Run pgls
                                c1 <- colnames(data_pgls[1])
                                c2 <- colnames(data_pgls[2])
                                model_NonGA_fixed_lambda <- pgls(as.formula(paste(c1, c2, sep=" ~ ")), data=data.pgls.NonGA, lambda= 0.000001)
                                model_NonGA_fixed_lambda
                                model <- model_NonGA_fixed_lambda
                                #Prep data
                                data <- dataset
                                tree <- treeset
                                tree <- drop.tip(treeset, c("Homo_sapiens", "Pan_troglodytes", "Macaca_mulatta", "Chlorocebus_aethiops", "Microcebus_murinus"))
                                data <- as.data.frame(treedata(tree, data, sort=TRUE, warnings=TRUE)$data)
                                X <- data[, c(2)]
                                Y <- data[, c(1)]
                                tree <- rescale(tree, "lambda", model$param[2])
                                vcv_tree <- vcv(tree)
                                k<-31
                                model_pi <- gls.pi(Y, X, vcv_tree, k)
                                n <- length(X)
                                XX <- cbind(rep(1, n), X)
                                Sigma <- vcv_tree
                                tr <- sum(diag(Sigma))
                                Sigma <- n*Sigma/tr
                                invSigma <- solve(Sigma)
                                C <- solve(t(XX)%*%invSigma%*%XX)
                                w <- C%*%t(XX)%*%invSigma
                                B <- w%*%Y
                                Yhat <- XX%*%B
                                Yresid = Y - Yhat
                                x <- dataset[c("Microcebus_murinus"), 2]
                                y <- dataset[c("Microcebus_murinus"), 1]
                                ZZ <- cbind(rep(1, length(x)), x)
                                par <- model_pi$model[, 1]
                                Yhat.x <- par[1] + par[2]*x
                                SEYhat.x <- sqrt((diag(ZZ%*%C%*%t(ZZ))+c(1/k))%*%((t(Yresid)%*%invSigma%*%Yresid)/(n-2)))
                                pu <- Yhat.x + qt(0.975, n)*SEYhat.x
                                pl <- Yhat.x - qt(0.975, n)*SEYhat.x
                                if (y - pu > pl - y){
                                  dif_fixed_lambda[i, j] <- max(0, y - pu)
                                } else {
                                  dif_fixed_lambda[i, j] <- - max(0, pl - y)
                                }  #end else
                              }, error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
                              }  
                            }
                          } 
                        } 
                        
                        
                        ####################################### plot matrix of differences ##########################
                        
                        library(reshape2)
                        library(ggplot2)
                        df <- data.frame(id=colnames(database[, 1:d]),dif_fixed_lambda)
                        gg <- melt(df, id="id")
                        ggplot(gg, aes(x=id,y=variable,fill=value))+
                          geom_tile()+
                          scale_fill_gradient(low="#FFFF88",high="#FF0000")+
                          coord_fixed()
                        write.csv(df,"/home/cgarin/Matrix_fixedlambda_2_0_curent.csv", row.names = FALSE)