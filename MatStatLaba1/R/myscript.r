#R version 3.3.2 

zero = c(85.3, 85.3, 86.5, 89.6, 92.3, 95.4, 96.11, 96.3, 99.9, 101.6, 102.44, 103.5, 106.3, 106.3, 112.9, 113.9, 115.5, 123.9, 124.89, 130.2, 132.3, 135.6, 135.99, 136.8, 137.1, 137.1, 137.6, 152.4, 153.9, 154.1, 160.6, 177.2, 185.5, 313, 382.6, 401.5, 401.5, 571.3)

hist(zero)
h1 = hist(zero)
lines(h1$counts ~ h1$mids, col="red")
rug(zero)

ones = c(79.54, 90, 91.4, 105.2, 121.17, 143.7, 163.6, 172, 251.4, 326.7, 620.325)
h2 = hist(ones)
lines(h2$counts ~ h2$mids, col="red")
rug(ones)

n1 = length(zero)
plot(sort(zero), (1:n1)/n1, type="S", col="seagreen", main="Zeros", xlab="", ylab="")
x = seq(0, 6, by=0.25)

n2 = length(ones)
plot(sort(ones), (1:n2)/n2, type="S", col="seagreen", main="Ones", xlab="", ylab="")
y = seq(0, 6, by=0.25)

boxplot(zero, outchar=T, main="Zeros", ylab="")
boxplot(ones, outchar=T, main="Ones", ylab="")
