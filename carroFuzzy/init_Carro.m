close all; clear all; clc;%#ok

xi = 10;
yi = 10;
xf = 75;
yf = 75;
Tsim = 10;
piI = 0.5*pi;
fismovil3 = readfis("fismovil3.fis")
mySim = sim("simCarro.sl x",Tsim);