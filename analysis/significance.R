rm(list=ls())
#control <- read.csv('~/efsscores/energy_lagged/control/scores.txt')
#experiment <- read.csv('~/efsscores/energy_lagged/rt/scores.txt')
#colnames(control)[3] <- 'error'
#colnames(experiment)[3] <- 'error'
#control[20,] <- NA
#experiment[40,] <- NA
control <- read.csv('~/rtresults_1000_100/TruncationEliteRTNOMUT_energy_lagged.csv')
experiment <- read.csv('~/rtresults_1000_100/TruncationEliteRT_energy_lagged.csv')
colnames(control)[2] <- 'error'
colnames(experiment)[2] <- 'error'
NUM_SAMPLES <- min(length(experiment$error), length(control$error))
control <- data.frame(control[-(NUM_SAMPLES:nrow(control)+1), ])
control[is.infinite(control$error),] <- NA
experiment <- data.frame(experiment[-(NUM_SAMPLES:nrow(experiment)+1), ])
experiment[is.infinite(experiment$Ensemble1),] <- NA
summary(control)
summary(experiment)
wilcox.test(control$error, experiment$error, 
            conf.level = 0.95, conf.int = TRUE)

#library(cowplot)
#experiment.error <- data.frame(MSE = experiment$error, Experiment='SRRT')
#control.error <- data.frame(MSE = control$error, Experiment='SR')
#both <- rbind(experiment.error, control.error)
#plot.error <- ggplot(both, aes(Experiment, MSE, fill=Experiment)) + 
#  geom_boxplot() + guides(fill=FALSE)
#plot.error
#
#save_plot(paste('/home/cfusting/Dropbox/rtpaper/', 'whiskers', ".pdf", sep = ''), plot.error,
#          base_aspect_ratio = 1.3 # make room for figure legend
#)