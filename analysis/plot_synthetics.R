rm(list=ls())


getDataFrame <- function(experiment.name, data_set_name, directory) {
  print(directory)
  pat <- paste(experiment.name, data_set_name, "\\d+.csv", sep="_")
  print(pat)
  files <- list.files(directory, pattern = pat, full.names = TRUE)
  for(file in files) {
    cat("Matched file:", file, "\n")
  }
  pattern <- paste(experiment.name, data_set_name, "\\d+.csv", sep="_")
  seeds <- unlist(lapply(files, function(x) { 
    m <- regexpr(pattern, x) 
    seed <- regmatches(x, m)
    print(seed)
    st <- regmatches(seed, regexpr("_(\\d+).csv", seed))
    return(regmatches(st, regexpr("\\d+", st)))
  }))
  dats <- lapply(files, read.csv)
  dats.labeled <- lapply(1:length(dats), function(i) {
    dats[[i]]$seed <- rep(seeds[i], nrow(dats[[i]])) 
    dats[[i]]$Generation <- 1:nrow(dats[[i]])
    return(dats[[i]])
  })
  df <- do.call("rbind", dats.labeled)
  return(df)
}

calcAvg <- function(dat) {
  return(aggregate(dat, by=list(gen = dat$Generation), FUN = mean))
}

DATA.SET <- 'min_approx'
DATA.SET.NAME <- 'minimum'
subtitle <- 'Approximating a Simple Minimum.'
EXP1.id <- "TruncationElite"
EXP2.id <- "TruncationEliteRT"
EXP3.id <- "TruncationEliteRTNOMUT"
EXP1.name <- "SR"
EXP2.name <- "SRRT"
EXP3.name <- "SRRTNM"
EXP1.SUB <- "No Range Terminals"
EXP2.SUB <- "Range Terminals"
EXP1.dir <- paste("~/rtresults_1000_100", DATA.SET, EXP1.id, "logs", sep = "/")
EXP2.dir <- paste("~/rtresults_1000_100", DATA.SET, EXP2.id, "logs", sep = "/")
EXP3.dir <- paste("~/rtresults_1000_100", DATA.SET, EXP3.id, "logs", sep = "/")
exp1 <- getDataFrame(EXP1.id, DATA.SET.NAME, EXP1.dir) 
exp2 <- getDataFrame(EXP2.id, DATA.SET.NAME, EXP2.dir)
exp3 <- getDataFrame(EXP3.id, DATA.SET.NAME, EXP3.dir)


library(cowplot)
XMAX <- max(exp1$Generation, exp2$Generation, exp3$Generation)
YMAX.fitness <- max(exp1$min_fitness, exp2$min_fitness, exp3$min_fitness) 
YMAX.size <- max(exp1$avg_size, exp2$avg_size, exp3$avg_size)

library(boot)
GENS <- c(350, 750)
calcstat <- function(x, d) { return(mean(x[d])) }
calcci <- function(dat, gen) {
  b = boot(dat$min_fitness[dat$Generation==gen], calcstat, R=1000)
  ci = boot.ci(boot.out = b, conf = 0.95, type = "basic")
  return(ci)
}
appendci <- function(dat) {
  cat('Calculating confidence intervals.\n')
  cis <- lapply(GENS, function(x) { calcci(dat, x) })
  cat('Appending lower and upper intervals.\n')
  N <- length(dat$Generation[dat$Generation==1])
  for(i in 1:length(GENS)) {
    dat$lower[dat$Generation==GENS[i]] <- rep(cis[[i]]$basic[4], N)
    dat$upper[dat$Generation==GENS[i]] <- rep(cis[[i]]$basic[5], N)
  }
  return(dat)
}
exp1 <- appendci(exp1)
exp2 <- appendci(exp2)
exp3 <- appendci(exp3)


#ggplot(exp1, aes(Generation, min_fitness, colour = seed)) + geom_line(show.legend = FALSE) +
#  labs(title = EXP1.name, subtitle = EXP1.SUB) +
#  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
#  ylim(0, YMAX.fitness) + xlim(0, XMAX)
#ggplot(exp2, aes(Generation, min_fitness, colour = seed)) + geom_line(show.legend = FALSE) +
#  labs(title = EXP2.name, subtitle = EXP2.SUB) +
#  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
#  ylim(0, YMAX.fitness) + xlim(0, XMAX)
#ggplot(exp1, aes(Generation, avg_size, colour = seed)) + geom_line(show.legend = FALSE) +
#  labs(title = EXP1.name, subtitle = EXP1.SUB) +
#  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
#  ylim(0, YMAX.size)
#ggplot(exp2, aes(Generation, avg_size, colour = seed)) + geom_line(show.legend = FALSE) +
#  labs(title = EXP2.name, subtitle = EXP2.SUB) +
#  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
#  ylim(0, YMAX.size)

exp1.avg <- calcAvg(exp1)
exp2.avg <- calcAvg(exp2)
exp3.avg <- calcAvg(exp3)
exp1.avg$Experiment <- EXP1.name
exp2.avg$Experiment <- EXP2.name
exp3.avg$Experiment <- EXP3.name
exps <- rbind(exp1.avg, exp2.avg, exp3.avg)
XMAX.avg <- max(exps$Generation)
YMAX.fitness.avg <- max(exps$min_fitness) 
YMIN.fitness.avg <- min(exps$min_fitness) 
YMAX.size.avg <- max(exps$avg_size)
plot.error <- ggplot(exps, aes(Generation, min_fitness, color = Experiment)) +
  geom_errorbar(aes(ymin=lower, ymax=upper), width=50) +
  geom_line() +
  labs(y = 'Average Minimum MSE') +
  #theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(YMIN.fitness.avg, YMAX.fitness.avg / 3) + xlim(0, XMAX.avg) #+ guides(fill=FALSE) 
plot.error
save_plot(paste('/home/cfusting/Dropbox/rtpaper/', DATA.SET, ".png", sep = ''), plot.error,
          base_aspect_ratio = 1.3 # make room for figure legend
)
#ggplot(exps, aes(Generation, avg_size, colour = experiment)) + geom_line() +
#  labs(title = "Average Size Averaged Over Seeds") +
#  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
#  ylim(0, YMAX.size.avg) + xlim(0, XMAX.avg) 


min(exp1.avg$min_fitness)
min(exp2.avg$min_fitness)
min(exp1.avg$avg_fitness)
min(exp2.avg$avg_fitness)

#ggplot(exps, aes(Generation, log(avg_fitness) / max(log(avg_fitness)), colour = experiment)) + 
#  geom_point() + labs(title = "Average Fitness Averaged Over Seeds") +
#  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
#  ylim(0, 1) + xlim(0, XMAX.avg)
#ggplot(exps, aes(Generation, avg_parametrized, colour = experiment)) + 
#  geom_line() + labs(title = "Average Parametrized Terminals Averaged Over Seeds") +
#  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
#  ylim(0, 1) + xlim(0, XMAX.avg)

sqrt(min(exp1$min_fitness))
sqrt(min(exp2$min_fitness))
min(exp1$min_fitness)
min(exp2$min_fitness)
