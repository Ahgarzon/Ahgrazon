close all;
clear all;
clc;

xi = 15;
yi = 15;
xf = 75;
yf = 75;
Timesim = 10;
piI = 0.5*pi;
fismovil3 = readfis("alphafuzzy.fis");
mySim = sim("truckaso2.slx",Timesim);